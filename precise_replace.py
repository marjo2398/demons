import re

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out = []

    for line in lines:
        if 'text-' not in line and 'text-white' not in line:
            out.append(line)
            continue

        # Check if line contains a button or we should keep text-white
        keep_white = False
        if 'bg-indigo-' in line or '<button' in line or 'btn' in line or 'bg-green-' in line:
            keep_white = True
        if 'bg-slate-800' in line and 'hover:bg-slate-700' in line:
            keep_white = True

        is_main = False
        if any(h in line for h in ['<h1', '<h2', '<h3', '<h4', '<h5', '<h6', 'text-2xl', 'text-xl', 'text-lg', 'text-1xl']):
            is_main = True
        if not is_main and 'font-bold' in line and '<td' not in line and '<th' not in line and 'text-xs' not in line and 'text-sm' not in line:
            is_main = True
        if 'font-bold' in line and ('item-name' in line or 'truncate' in line or 'text-indigo-500' in line or 'text-white' in line):
            is_main = True

        def repl(m):
            c = m.group(0)
            if 'hover:' in c:
                if keep_white and 'white' in c:
                    return c
                return 'hover:text-slate-200'
            else:
                if keep_white and 'white' in c:
                    return c
                return 'text-slate-200' if is_main else 'text-slate-400'

        # This will replace inline class names correctly without regexing across lines
        new_line = re.sub(r'\b(?:hover:)?text-indigo-\d+\b|\b(?:hover:)?text-white(?:-\d+)?\b', repl, line)

        # PHP special replacements if any in this line
        new_line = re.sub(r"'text-indigo-\d+'", "'text-slate-400'", new_line)
        new_line = re.sub(r"'hover:text-indigo-\d+'", "'hover:text-slate-200'", new_line)
        new_line = re.sub(r"'text-white(?:-\d+)?'", "'text-slate-200'", new_line)
        new_line = re.sub(r"'hover:text-white'", "'hover:text-slate-200'", new_line)

        # JS in host.php
        if "btnElement.classList.remove('text-indigo-400');" in new_line:
            new_line = new_line.replace("'text-indigo-400'", "'text-slate-400'")

        out.append(new_line)

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(out)

process_file('index.php')
process_file('host.php')
