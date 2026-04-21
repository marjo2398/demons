import re

def rewrite(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to replace all text-indigo-[0-9]+ and text-white (and text-white-400, etc)
    # EXCEPT:
    # - If it's a button (e.g., bg-indigo-600 with text-white)
    #
    # Logic for replacement:
    # 1. Split content by HTML tags and text.
    # 2. In HTML tags, find class="..."
    # 3. Inside class="...", find text classes.
    # 4. If the tag contains bg-indigo-600, DO NOT replace text-white.
    # 5. Decide text-slate-200 vs text-slate-400 based on tag type and classes.
    #    - text-slate-200: h1, h2, h3, h4, h5, h6, text-xl, text-2xl, text-lg, important panels. Let's say if 'font-bold' is present AND it's not a small text (like text-xs, text-sm) AND not inside a table cell (unless it's a prominent header).
    #    Actually, the instruction says:
    #    "Główne nagłówki i ważne nazwy (np. tytuły paneli): Zamień na text-slate-200"
    #    "Pomniejsze teksty (np. nagłówki kolumn w tabeli, zwykły tekst): Zamień na text-slate-400"

    def replacer(match):
        tag_full = match.group(0)

        is_button = 'bg-indigo-' in tag_full or 'btn' in tag_full.lower()

        # We need a function to replace classes within the class attribute
        def class_replacer(class_match):
            class_str = class_match.group(1)
            classes = class_str.split()
            new_classes = []

            for c in classes:
                # Find if c is text-indigo-* or text-white*
                if re.match(r'^text-indigo-\d+$', c) or c.startswith('text-white'):
                    if is_button and c.startswith('text-white'):
                        # Do not change text-white on buttons
                        new_classes.append(c)
                    elif c == 'text-white' and 'bg-green-' in tag_full:
                         # e.g., <button ... class="bg-green-600 text-white">
                         new_classes.append(c)
                    else:
                        # Decide slate-200 vs slate-400
                        if any(header_class in classes for header_class in ['text-2xl', 'text-xl', 'text-lg']) or re.match(r'^<h[1-6]', tag_full):
                            new_classes.append('text-slate-200')
                        elif 'font-bold' in classes and 'text-xs' not in classes and 'text-sm' not in classes and not tag_full.startswith('<td') and not tag_full.startswith('<th'):
                            new_classes.append('text-slate-200')
                        elif 'font-bold' in classes and tag_full.startswith('<th') and 'table-header' not in tag_full:
                            new_classes.append('text-slate-400')
                        elif tag_full.startswith('<span') and 'font-bold' in classes and ('truncate' in classes or 'item-name' in classes or 'text-indigo-100' in classes or 'text-indigo-400' in classes or 'text-indigo-500' in classes or 'text-white' in classes):
                             # To keep "ważne nazwy" (item names, player names) bright
                             if 'text-sm' in classes and not ('truncate' in classes or 'item-name' in classes):
                                 new_classes.append('text-slate-400')
                             else:
                                 new_classes.append('text-slate-200')
                        else:
                            new_classes.append('text-slate-400')
                # we also check hover:text-indigo-* and hover:text-white
                elif re.match(r'^hover:text-indigo-\d+$', c) or c.startswith('hover:text-white'):
                    if is_button and c.startswith('hover:text-white'):
                        new_classes.append(c)
                    else:
                        new_classes.append('hover:text-slate-200') # Or just leave it? "Zmień wyłącznie klasy text-..." -> means we should change hover:text-... too.
                else:
                    new_classes.append(c)

            return 'class="' + ' '.join(new_classes) + '"'

        tag_full = re.sub(r'class="([^"]*)"', class_replacer, tag_full)

        # Handle inline PHP classes if any like class="<?= ... ?>"
        # We will handle PHP logic manually or with regex if possible
        def php_class_replacer(php_match):
            php_code = php_match.group(0)
            php_code = re.sub(r"'text-indigo-\d+'", "'text-slate-400'", php_code)
            php_code = re.sub(r"'text-white'", "'text-slate-200'", php_code)
            php_code = re.sub(r"'hover:text-white'", "'hover:text-slate-200'", php_code)
            php_code = re.sub(r"'text-white-400'", "'text-slate-400'", php_code)
            return php_code

        tag_full = re.sub(r'<\?php.*?\?>|<\?=.*?\?>', php_class_replacer, tag_full)

        return tag_full

    new_content = re.sub(r'<[^>]+>', replacer, content)

    with open(f"new2_{file_path}", 'w', encoding='utf-8') as f:
        f.write(new_content)

for filename in ['index.php', 'host.php']:
    rewrite(filename)
