import re
import sys

def analyze(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all class="..." occurrences
    classes = re.findall(r'class="([^"]*)"', content)
    # Also find inline class in php tags like class='...' or class=<?= ... ?>
    # It's better to just regex text-[a-zA-Z0-9_-]+

    colors = set()
    for match in re.finditer(r'text-[a-zA-Z]+-\d+', content):
        colors.add(match.group(0))

    for match in re.finditer(r'text-white', content):
        colors.add(match.group(0))

    print(f"--- {file_path} ---")
    for c in sorted(colors):
        print(c)

analyze('index.php')
analyze('host.php')
