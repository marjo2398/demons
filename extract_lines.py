import re

def extract(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"--- {file_path} ---")
    for i, line in enumerate(lines):
        if re.search(r'text-indigo-\d+', line) or re.search(r'text-white', line):
            print(f"{i+1}: {line.strip()}")

extract('index.php')
extract('host.php')
