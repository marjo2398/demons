import re

def modify_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out = []

    # We will process line by line, doing string replacements.
    # We want to change text-indigo-* to text-slate-200 or text-slate-400
    # text-white, text-white-400 -> text-slate-200 or text-slate-400
    # EXCEPT for buttons. "nie ruszaj klas przycisków (bg-indigo-600)"

    for line in lines:
        if 'text-' not in line and 'text-white' not in line:
            out.append(line)
            continue

        # Is it a button or bg-indigo? We can just do a heuristic.
        is_button = 'bg-indigo-' in line or '<button' in line or 'btn' in line.lower()
        if 'btnElement.classList' in line:
            # JS line: btnElement.classList.remove('text-indigo-400');
            line = line.replace("'text-indigo-400'", "'text-slate-400'")
            line = line.replace("'text-white'", "'text-slate-200'")
            out.append(line)
            continue

        def repl(match):
            color_class = match.group(0) # text-indigo-400 or text-white
            # We want to know if it's main or minor.
            # Just search the whole line for h1, h2, h3, font-bold, text-xl, etc.
            is_main = any(x in line for x in ['<h1', '<h2', '<h3', 'text-2xl', 'text-xl', 'text-lg', 'text-1xl'])
            if not is_main and 'font-bold' in line and 'text-xs' not in line and 'text-sm' not in line and '<td' not in line and '<th' not in line:
                is_main = True
            if 'font-bold' in line and ('item-name' in line or 'truncate' in line or 'font-medium' in line):
                is_main = True

            if is_button and 'text-white' in color_class:
                return color_class
            if 'bg-green-' in line and 'text-white' in color_class:
                return color_class
            if 'bg-slate-800' in line and 'hover:bg-slate-700' in line and 'text-white' in color_class:
                return color_class

            if 'hover:' in color_class:
                return 'hover:text-slate-200'
            else:
                return 'text-slate-200' if is_main else 'text-slate-400'

        # Regex for text-indigo-[0-9]+, hover:text-indigo-[0-9]+, text-white(-\d+)?, hover:text-white
        # Make sure not to match inside words
        line = re.sub(r'\b(?:hover:)?text-indigo-\d+\b|\b(?:hover:)?text-white(?:-\d+)?\b', repl, line)
        out.append(line)

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(out)

modify_file('index.php')
modify_file('host.php')
