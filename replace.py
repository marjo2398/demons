import re

def process_line(line):
    # If the line contains a button with bg-indigo, we should be careful not to change its text-white
    # But wait, the instruction says "Zmień wyłącznie klasy text-... w tych dwóch plikach" -> "Znajdź wszystkie klasy tekstowe bazujące na kolorze indigo ... oraz inne jaskrawe napisy"
    # "nie ruszaj klas przycisków (bg-indigo-600) ani struktury HTML. Zmień wyłącznie klasy text-... w tych dwóch plikach."

    # We need to distinguish between main headers (h1, h2, h3, important names) and minor text.

    # Let's define important tags: <h1, <h2, <h3, <span class="block ... font-bold text-lg", <span class="font-bold ... truncate"
    # Let's parse classes properly.
    pass
