import re
import os
import sys

# Nastavení cest
#input_file = "/home/musil/EduPo/tomas/generated/v33_plain"      # vstupní soubor s básněmi
#output_folder = "poems/v33"       # složka, kam se uloží výsledky
input_file = sys.argv[1]
output_folder = sys.argv[2]

# Vytvoření složky, pokud neexistuje
os.makedirs(output_folder, exist_ok=True)

# Načtení celého souboru
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Najdi všechny bloky mezi <poem>...</poem>
poems = re.findall(r"<poem>(.*?)</poem>", text, re.DOTALL)

# Zpracování jednotlivých básní
for i, poem in enumerate(poems, start=1):
    # Rozděl na řádky
    lines = poem.strip().splitlines()

    # Vynech první 3 řádky
    content = "\n".join(lines[3:]).strip()

    # Ulož do souboru
    filename = os.path.join(output_folder, f"poem_{i}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Uloženo: {filename} (vynechány první tři řádky)")

print(f"\nHotovo! Zpracováno {len(poems)} básní.")

