import re

content = '<a href="index.php" class="block text-center text-gray-500 text-xs mt-6 hover:text-white underline">Back</a>'

def class_sub(match):
    tag_full = match.group(0)
    print("tag full:", tag_full)

    is_btn = 'bg-indigo-' in tag_full or 'bg-green-' in tag_full or 'btn' in tag_full or ('bg-slate-800' in tag_full and 'hover:bg-slate-700' in tag_full)
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

new_content = re.sub(r'<[^>]*>', class_sub, content)
print(new_content)
