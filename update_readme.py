import datetime
import requests
import os
from collections import defaultdict
import concurrent.futures

# GitHub username and token for authentication
GITHUB_USERNAME = "Kaden-G"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("PAT_TOKEN")  # Ensure your PAT_TOKEN is set as an environment variable

if not GITHUB_TOKEN:
    print("Error: PAT_TOKEN environment variable is not set.")
    exit(1)

# Headers for GitHub API authentication
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_all_repos(username, headers):
    repos = []
    page = 1
    per_page = 100
    while True:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(repos_url, headers=headers)
        if response.status_code == 200:
            page_repos = response.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
        else:
            print(f"Failed to fetch repository data. Status code: {response.status_code}")
            break
    return repos

def fetch_languages(repo_name, headers):
    languages_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
    lang_response = requests.get(languages_url, headers=headers)
    if lang_response.status_code == 200:
        return lang_response.json()
    else:
        print(f"Failed to fetch languages for repository {repo_name}. Status code: {lang_response.status_code}")
        return {}

def main():
    # Check API rate limits (optional)
    rate_limit_url = "https://api.github.com/rate_limit"
    rate_response = requests.get(rate_limit_url, headers=headers)
    if rate_response.status_code == 200:
        rate_data = rate_response.json()
        remaining = rate_data['resources']['core']['remaining']
        reset_time = datetime.datetime.fromtimestamp(rate_data['resources']['core']['reset'])
        print(f"API Rate Limit: {remaining} requests remaining. Resets at {reset_time}.")
        if remaining < 10:
            print("Warning: Approaching API rate limit.")
    else:
        print("Failed to fetch API rate limit information.")

    # Fetch repositories
    repos_data = fetch_all_repos(GITHUB_USERNAME, headers)
    total_repos = len(repos_data)
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)

    # Gather language data
    language_data = defaultdict(int)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_repo = {executor.submit(fetch_languages, repo['name'], headers): repo for repo in repos_data}
        for future in concurrent.futures.as_completed(future_to_repo):
            lang_data = future.result()
            for language, size in lang_data.items():
                language_data[language] += size

    total_bytes = sum(language_data.values())
    language_percentages = {
        language: (size / total_bytes) * 100 if total_bytes > 0 else 0
        for language, size in language_data.items()
    }

    # Build language summary table
    language_summary = "| Language   | Percentage |\n|------------|-----------:|\n"
    for language, percentage in language_percentages.items():
        language_summary += f"| {language} | {percentage:.2f}% |\n"

    # Timestamp for the last update
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
