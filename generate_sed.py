import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to target:
    # 1. text-indigo-100, text-indigo-200, text-indigo-300, text-indigo-400, text-indigo-500
    # 2. Other bright texts? (text-white, text-white-400) - user said: "Znajdź wszystkie klasy tekstowe bazujące na kolorze indigo (np. text-indigo-400, text-indigo-300) oraz inne jaskrawe napisy i zamień je według tego klucza:"
    #
    # Główne nagłówki i ważne nazwy (np. tytuły paneli): Zamień na text-slate-200 (jasny, wyrazisty srebrny).
    # Pomniejsze teksty (np. nagłówki kolumn w tabeli, zwykły tekst): Zamień na text-slate-400 (zgaszony szary).
    #
    # The user also mentions:
    # "Nie zmieniaj tła (bg-slate-950/900), nie ruszaj klas przycisków (bg-indigo-600) ani struktury HTML. Zmień wyłącznie klasy text-... w tych dwóch plikach."

    lines = content.split('\n')

    print(f"\n--- {file_path} ---")

    for i, line in enumerate(lines):
        if re.search(r'text-indigo-\d+|text-white', line):
            print(f"Line {i+1}: {line.strip()}")

process_file('index.php')
process_file('host.php')
