    # New README content readme_content = f"""
# KADEN GODINEZ

**Location:** Bay Area, CA  
**DevOps | Cloud | Java & Python Enthusiast**

_Last Updated: {current_time}_

---

## 🎮 Blackjack Game
[![Play My Blackjack Game](https://img.shields.io/badge/Play-Blackjack%20Now-brightgreen?style=for-the-badge)](https://Kaden-G.github.io)

A fun, interactive Blackjack game built with JavaScript. Test your luck against the dealer!

---

## 🔥 Skills & Tech
- 🐍 Python
- ☕ Java
- 🌐 HTML/CSS
- 🏗️ Terraform
- 🐳 Docker
- ☁️ AWS

---

## 📈 GitHub Stats
**Repositories:** {total_repos}  
**Stars Received:** {total_stars}

### Languages Used
{language_summary}

---

## 📬 Contact
- **Email:** [k.anthony.godinez@gmail.com](mailto:k.anthony.godinez@gmail.com)  
- **LinkedIn:** [linkedin.com/in/kadengodinez](https://www.linkedin.com/in/kadengodinez/)
"""

    # Write the updated content to README.md
    try:
        with open("README.md", "w") as f:
            f.write(readme_content.strip())
        print("README.md has been updated successfully.")
    except Exception as e:
        print(f"Failed to write to README.md: {e}")
        exit(1)

if __name__ == "__main__":
    main()
