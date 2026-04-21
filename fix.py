import re

def rewrite(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer(match):
        tag_full = match.group(0)

        is_button_or_indigo_bg = 'bg-indigo-' in tag_full or 'btn' in tag_full.lower()

        def class_replacer(class_match):
            class_str = class_match.group(1)
            classes = class_str.split()
            new_classes = []

            for c in classes:
                if re.match(r'^text-indigo-\d+$', c) or c.startswith('text-white'):
                    if is_button_or_indigo_bg and c.startswith('text-white'):
                        # Do not change text-white on buttons/indigo background
                        new_classes.append(c)
                    elif 'bg-green-' in tag_full and c.startswith('text-white'):
                        new_classes.append(c)
                    else:
                        # Decide slate-200 vs slate-400
                        # 200 for headers / important
                        # 400 for minor
                        if any(h in classes for h in ['text-2xl', 'text-xl', 'text-lg', 'text-1xl']):
                            new_classes.append('text-slate-200')
                        elif re.match(r'^<h[1-6]', tag_full):
                            new_classes.append('text-slate-200')
                        elif 'font-bold' in classes and 'text-xs' not in classes and 'text-sm' not in classes and not tag_full.startswith('<th') and not tag_full.startswith('<td'):
                            new_classes.append('text-slate-200')
                        elif 'font-medium' in classes and 'text-1xl' in classes:
                            new_classes.append('text-slate-200')
                        elif tag_full.startswith('<span') and 'font-bold' in classes and ('truncate' in classes or 'item-name' in classes or 'block' in classes):
                            new_classes.append('text-slate-200')
                        else:
                            new_classes.append('text-slate-400')
                elif re.match(r'^hover:text-indigo-\d+$', c) or c.startswith('hover:text-white'):
                    if is_button_or_indigo_bg and c.startswith('hover:text-white'):
                        new_classes.append(c)
                    else:
                        new_classes.append('hover:text-slate-200')
                else:
                    new_classes.append(c)

            return 'class="' + ' '.join(new_classes) + '"'

        tag_full = re.sub(r'class="([^"]*)"', class_replacer, tag_full)

        # Handly PHP inline strings containing classes like <?= $lang=='en'?'text-indigo-400':'text-gray-400 hover:text-white' ?>
        # We'll just regex replace inside PHP blocks

        return tag_full

    new_content = re.sub(r'<[^>]+>', replacer, content)

    # PHP inline replace
    def php_inline_replace(match):
        php_code = match.group(0)
        # text-indigo-* -> text-slate-400 (for lang links, these are minor)
        php_code = re.sub(r"'text-indigo-\d+'", "'text-slate-400'", php_code)
        # hover:text-white -> hover:text-slate-200
        php_code = re.sub(r"'hover:text-white'", "'hover:text-slate-200'", php_code)
        return php_code

    new_content = re.sub(r'<\?=(.*?)\?>', php_inline_replace, new_content)

    with open(f"{file_path}", 'w', encoding='utf-8') as f:
        f.write(new_content)

for filename in ['index.php', 'host.php']:
    rewrite(filename)
