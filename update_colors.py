import re
import sys

def replace_colors(content):
    # Let's split by tags to process class attributes more safely

    def replacer(match):
        tag_full = match.group(0)

        # Check if it's a button or has bg-indigo-*, if so, we might want to preserve text-white
        is_button = 'bg-indigo-' in tag_full or '<button' in tag_full or 'btn' in tag_full.lower()
        if is_button and 'text-white' in tag_full:
            # We preserve text-white for indigo buttons as per instruction: "nie ruszaj klas przycisków (bg-indigo-600)"
            # However, we still need to check if there are indigo texts to replace.
            pass

        # Determine if it's a main header/title
        is_header = bool(re.search(r'<h[1-6]|text-xl|text-2xl|text-lg|font-bold', tag_full))
        # But some table headers have font-bold, some normal text has font-bold.
        # User said: "Główne nagłówki i ważne nazwy (np. tytuły paneli): Zamień na text-slate-200"
        # "Pomniejsze teksty (np. nagłówki kolumn w tabeli, zwykły tekst): Zamień na text-slate-400"

        # Classes to find: text-indigo-[0-9]+, text-white, text-white-400
        # What about text-gray-200, text-gray-300? User only said "klasy tekstowe bazujące na kolorze indigo ... oraz inne jaskrawe napisy" -> text-white is jaskrawe (bright).

        def class_replacer(class_match):
            class_str = class_match.group(1)
            classes = class_str.split()
            new_classes = []

            for c in classes:
                if re.match(r'text-indigo-\d+', c) or c in ['text-white', 'text-white-400']:
                    # Determine replacement
                    if is_button and c == 'text-white':
                        new_classes.append(c) # keep text-white on buttons
                    else:
                        # If it's a header or large text -> slate-200, else slate-400
                        if 'text-2xl' in classes or 'text-xl' in classes or 'text-lg' in classes or tag_full.startswith('<h'):
                            new_classes.append('text-slate-200')
                        elif 'font-bold' in classes and not tag_full.startswith('<td') and not tag_full.startswith('<th') and 'text-xs' not in classes and 'text-sm' not in classes:
                            # Important names might be font-bold without large text, let's say slate-200
                            new_classes.append('text-slate-200')
                        else:
                            new_classes.append('text-slate-400')
                else:
                    new_classes.append(c)
            return 'class="' + ' '.join(new_classes) + '"'

        tag_full = re.sub(r'class="([^"]*)"', class_replacer, tag_full)
        return tag_full

    # Process all HTML tags
    new_content = re.sub(r'<[^>]+>', replacer, content)
    return new_content

for filename in ['index.php', 'host.php']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = replace_colors(content)

    with open(f"new_{filename}", 'w', encoding='utf-8') as f:
        f.write(new_content)
