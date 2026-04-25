import re

def rewrite(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out_lines = []

    # Define regexes for classes to replace
    # Target colors: text-indigo-[0-9]+, text-white, text-white-400
    color_pattern = re.compile(r'\b(text-indigo-\d+|text-white(?:-\d+)?)\b')

    for i, line in enumerate(lines):
        if color_pattern.search(line) and 'text-white' in line and 'bg-indigo' in line:
            # "nie ruszaj klas przycisków (bg-indigo-600)"
            # we should skip text-white if it's on a button with bg-indigo-600
            # Let's be careful. Actually, it's easier to manually inspect and replace, but let's automate the obvious ones.
            pass

    # Since there are many nuances, let's write a smarter regex.
