import requests
import re

USERNAME = "anasfaiq" 
API_URL = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=3"

# Ambil data dari GitHub API
response = requests.get(API_URL)
repos = response.json()

# Format hasilnya jadi list Markdown
project_list = "\n"
for repo in repos:
    # Handle error kalau API kena rate limit atau repo kosong
    if isinstance(repo, dict) and 'name' in repo:
        desc = repo.get('description') or 'Project tanpa deskripsi'
        project_list += f"- [**{repo['name']}**]({repo['html_url']}) - {desc}\n"
project_list += "\n"

# Baca file README saat ini
with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()

# Timpa bagian di antara tag penanda dengan list project baru
marker_start = ""
marker_end = ""
pattern = rf"{marker_start}.*?{marker_end}"
new_readme = re.sub(pattern, f"{marker_start}{project_list}{marker_end}", readme, flags=re.DOTALL)

# Tulis ulang file README
with open("README.md", "w", encoding="utf-8") as file:
    file.write(new_readme)
