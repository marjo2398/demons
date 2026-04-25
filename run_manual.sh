# We will do simple string replace using python
python3 -c "
import sys, re
for f in ['index.php', 'host.php']:
    with open(f, 'r') as file:
        content = file.read()

    # We replace any occurrences of text-indigo-* or text-white with text-slate-200 or text-slate-400
    # EXCEPT for bg-indigo-*, bg-green-* which are buttons.
    # We will do this by parsing class attributes.
    def class_sub(match):
        tag_full = match.group(0)

        is_btn = 'bg-indigo-' in tag_full or 'bg-green-' in tag_full or 'btn' in tag_full or 'bg-slate-800' in tag_full and 'hover:bg-slate-700' in tag_full
        is_main = any(x in tag_full for x in ['<h1', '<h2', '<h3', 'text-2xl', 'text-xl', 'text-lg', 'text-1xl'])
        if not is_main and 'font-bold' in tag_full and 'text-xs' not in tag_full and 'text-sm' not in tag_full and '<td' not in tag_full and '<th' not in tag_full:
            is_main = True
        if 'font-bold' in tag_full and ('item-name' in tag_full or 'truncate' in tag_full):
            is_main = True

        def cl_sub(m2):
            classes = m2.group(1).split()
            new_classes = []
            for c in classes:
                if 'text-indigo-' in c or 'text-white' in c:
                    if is_btn and 'text-white' in c:
                        new_classes.append(c)
                    else:
                        new_classes.append('text-slate-200' if is_main else 'text-slate-400')
                elif 'hover:text-indigo-' in c or 'hover:text-white' in c:
                    if is_btn and 'hover:text-white' in c:
                        new_classes.append(c)
                    else:
                        new_classes.append('hover:text-slate-200')
                else:
                    new_classes.append(c)
            return 'class=\"' + ' '.join(new_classes) + '\"'

        return re.sub(r'class=\"([^\"]*)\"', cl_sub, tag_full)

    # Replace in tags
    new_c = re.sub(r'<[^>]*>', class_sub, content)

    # replace in inline php
    def php_sub(match):
        s = match.group(0)
        s = re.sub(r\"'text-indigo-\d+'\", \"'text-slate-400'\", s)
        s = re.sub(r\"'hover:text-white'\", \"'hover:text-slate-200'\", s)
        s = re.sub(r\"'text-white(?:-\d+)?'\", \"'text-slate-200'\", s)
        return s

    new_c = re.sub(r'<\?=.*?\?>', php_sub, new_c)

    with open(f, 'w') as file:
        file.write(new_c)
"
