import re

def rewrite(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The simplest logic, as requested:
    # "Znajdź wszystkie klasy tekstowe bazujące na kolorze indigo ... oraz inne jaskrawe napisy i zamień je"
    # Główne nagłówki i ważne nazwy (np. tytuły paneli): text-slate-200
    # Pomniejsze teksty (np. nagłówki kolumn w tabeli, zwykły tekst): text-slate-400

    # Just replacing ALL occurrences globally using a simple Python script that uses regex:
    # Instead of parsing HTML properly, just use re.sub on classes:

    def class_sub(match):
        class_content = match.group(1)
        classes = class_content.split()

        # We need to know if it's a button
        # This requires matching the tag first.
        return match.group(0)

    # Let's do it tag by tag:
    def tag_replacer(match):
        tag = match.group(0)

        # Is it a button or bg-indigo?
        is_button = 'bg-indigo-' in tag or 'btn' in tag.lower() or '<button' in tag

        # Is it a header or important?
        is_important = any(x in tag for x in ['<h1', '<h2', '<h3', 'text-2xl', 'text-xl', 'text-lg', 'text-1xl'])
        # if not explicitly header, maybe font-bold + not td/th/text-xs/text-sm
        if not is_important and 'font-bold' in tag and 'text-xs' not in tag and 'text-sm' not in tag and '<td' not in tag and '<th' not in tag:
            is_important = True
        # For important names like item names or player names
        if 'font-bold' in tag and ('item-name' in tag or 'truncate' in tag):
             is_important = True
             if 'text-sm' in tag and not 'truncate' in tag:
                 # Actually item names in host.php are text-sm, so let's keep them important
                 is_important = True

        def class_replacer(c_match):
            cls_str = c_match.group(1)
            cls_list = cls_str.split()
            new_cls = []
            for c in cls_list:
                if re.match(r'^text-indigo-\d+$', c) or c.startswith('text-white'):
                    if is_button and c.startswith('text-white'):
                        new_cls.append(c)
                    elif 'bg-green-' in tag and c.startswith('text-white'):
                        new_cls.append(c)
                    elif 'bg-slate-800' in tag and 'hover:bg-slate-700' in tag and c.startswith('text-white'):
                        new_cls.append(c) # pagination buttons
                    else:
                        new_cls.append('text-slate-200' if is_important else 'text-slate-400')
                elif re.match(r'^hover:text-indigo-\d+$', c) or c.startswith('hover:text-white'):
                    if is_button and c.startswith('hover:text-white'):
                        new_cls.append(c)
                    else:
                        new_cls.append('hover:text-slate-200')
                else:
                    new_cls.append(c)
            return 'class="' + ' '.join(new_cls) + '"'

        return re.sub(r'class="([^"]*)"', class_replacer, tag)

    new_content = re.sub(r'<[a-zA-Z0-9]+[^>]*>', tag_replacer, content)

    # For inline PHP strings e.g., 'text-indigo-400'
    def php_replacer(match):
        php_str = match.group(0)
        php_str = re.sub(r"'text-indigo-\d+'", "'text-slate-400'", php_str)
        php_str = re.sub(r"'hover:text-indigo-\d+'", "'hover:text-slate-200'", php_str)
        php_str = re.sub(r"'text-white(-\d+)?'", "'text-slate-200'", php_str) # mostly important in PHP variables
        php_str = re.sub(r"'hover:text-white'", "'hover:text-slate-200'", php_str)
        return php_str

    new_content = re.sub(r'<\?php.*?\?>|<\?=.*?\?>', php_replacer, new_content, flags=re.DOTALL)

    # Also handle JS text replacements inside <script>
    new_content = re.sub(r"'text-indigo-400'", "'text-slate-400'", new_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for filename in ['index.php', 'host.php']:
    rewrite(filename)
