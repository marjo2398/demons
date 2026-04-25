import re

content = '<?php if($row['position'] == 1 && !$isBanned && !$isExcluded): ?><span class="w-2 h-2 rounded-full bg-green-500 shrink-0"></span><span class="text-white font-bold"><?= htmlspecialchars($row['nick']) ?></span>'

def process(content):
    def class_sub(match):
        tag_full = match.group(0)

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

    return re.sub(r'<[^>]*>', class_sub, content)

print(process(content))
