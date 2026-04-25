import re

def process_classes(class_str, tag_full):
    classes = class_str.split()
    new_classes = []

    is_button_or_indigo_bg = 'bg-indigo-' in tag_full or 'btn' in tag_full.lower()

    for c in classes:
        if re.match(r'^text-indigo-\d+$', c) or c.startswith('text-white'):
            if is_button_or_indigo_bg and c.startswith('text-white'):
                new_classes.append(c)
            elif 'bg-green-' in tag_full and c.startswith('text-white'):
                new_classes.append(c)
            elif 'bg-slate-800 text-white' in tag_full and 'hover:bg-slate-700' in tag_full:
                # e.g., pagination buttons
                new_classes.append(c)
            elif 'btn' in tag_full or '<button' in tag_full and c == 'text-white':
                new_classes.append(c) # standard button text
            else:
                # Slate 200 or 400
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
            elif 'btn' in tag_full or '<button' in tag_full and c.startswith('hover:text-white'):
                new_classes.append(c)
            else:
                new_classes.append('hover:text-slate-200')
        else:
            new_classes.append(c)

    return 'class="' + ' '.join(new_classes) + '"'


def rewrite(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def html_tag_replacer(match):
        tag_full = match.group(0)

        def class_attr_replacer(class_match):
            return process_classes(class_match.group(1), tag_full)

        tag_full = re.sub(r'class="([^"]*)"', class_attr_replacer, tag_full)
        return tag_full

    # We need to not break <?php ?> tags while parsing HTML
    # So we can replace class="..." attributes directly instead of full tags, but we need the tag context.
    # Alternatively, find all class="..." and check the tag it belongs to.

    # Simple regex for finding `<tag ... class="..." ... >`
    new_content = re.sub(r'<[a-zA-Z0-9]+[^>]*class="[^"]*"[^>]*>', html_tag_replacer, content)

    # Handly PHP inline string arrays/ternaries
    def php_inline_replace(match):
        php_code = match.group(0)
        php_code = re.sub(r"'text-indigo-\d+'", "'text-slate-400'", php_code)
        php_code = re.sub(r"'hover:text-white'", "'hover:text-slate-200'", php_code)
        # also handle case where text-white-400 or similar might be in PHP
        php_code = re.sub(r"'text-white(-\d+)?'", "'text-slate-200'", php_code)
        return php_code

    new_content = re.sub(r'<\?=.*?\?>', php_inline_replace, new_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for filename in ['index.php', 'host.php']:
    rewrite(filename)
