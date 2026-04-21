import re
import sys

def modify_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the file into HTML elements and everything else
    # We will match PHP tags <?php ... ?> or <?= ... ?> so we don't mess up inside them initially
    # But wait, class="..." can contain PHP. E.g. class="<?= $var ? 'text-white' : '' ?>"
    # We should replace those explicitly later.

    def tag_replacer(match):
        tag_full = match.group(0)

        # Don't touch script tags or style tags
        if tag_full.startswith('<?'):
            return tag_full

        # check if it's a button
        is_btn = ('bg-indigo-' in tag_full or
                  'bg-green-' in tag_full or
                  'btn' in tag_full or
                  '<button' in tag_full or
                  ('bg-slate-800' in tag_full and 'hover:bg-slate-700' in tag_full))

        # check if it's main header/text
        is_main = any(x in tag_full for x in ['<h1', '<h2', '<h3', '<h4', '<h5', '<h6', 'text-2xl', 'text-xl', 'text-lg', 'text-1xl'])
        if not is_main and 'font-bold' in tag_full:
            # check if it is NOT a small table cell or minor text
            if 'text-xs' not in tag_full and 'text-sm' not in tag_full and not tag_full.startswith('<td') and not tag_full.startswith('<th'):
                is_main = True

        # specific cases like important item names or player names
        if 'font-bold' in tag_full and ('item-name' in tag_full or 'truncate' in tag_full or 'text-white' in tag_full or 'text-indigo-500' in tag_full):
            # for host.php players lists etc
            is_main = True

        def class_replacer(m_cls):
            classes_str = m_cls.group(1)
            # handle inline php in classes? Wait, splitting by space might break PHP.
            # but we can just use regex replace inside the string.

            def single_repl(m_col):
                c = m_col.group(0)
                if 'hover:' in c:
                    if is_btn and 'white' in c:
                        return c
                    return 'hover:text-slate-200'
                else:
                    if is_btn and 'white' in c:
                        return c
                    return 'text-slate-200' if is_main else 'text-slate-400'

            new_classes_str = re.sub(r'\b(?:hover:)?text-indigo-\d+\b|\b(?:hover:)?text-white(?:-\d+)?\b', single_repl, classes_str)
            return 'class="' + new_classes_str + '"'

        return re.sub(r'class="([^"]*)"', class_replacer, tag_full)

    # We do a simpler split: we only match `< ... >` but NOT `<? ... ?>`
    # HTML tag regex
    new_content = re.sub(r'<(?!\?)[^>]+>', tag_replacer, content)

    # Now handle PHP inline strings
    def php_replacer(match):
        php_str = match.group(0)
        php_str = re.sub(r"'text-indigo-\d+'", "'text-slate-400'", php_str)
        php_str = re.sub(r"'hover:text-indigo-\d+'", "'hover:text-slate-200'", php_str)
        php_str = re.sub(r"'text-white(?:-\d+)?'", "'text-slate-200'", php_str)
        php_str = re.sub(r"'hover:text-white'", "'hover:text-slate-200'", php_str)
        return php_str

    new_content = re.sub(r'<\?=(.*?)\?>', php_replacer, new_content)

    # JS lines
    new_content = new_content.replace("'text-indigo-400'", "'text-slate-400'")
    new_content = new_content.replace("'text-white'", "'text-slate-200'")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

for f in ['index.php', 'host.php']:
    modify_file(f)
