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

    # Rozdel na nazev s autorem (prvni 3 radky) a samotny text
    header = "\n".join(lines[0:3]).strip()
    content = "\n".join(lines[3:]).strip()

    # Ulož do souboru
    filename = os.path.join(output_folder, f"header_{i:03d}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)
    
        filename = os.path.join(output_folder, f"poem_{i:03d}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Uloženo: {filename}")

print(f"\nHotovo! Zpracováno {len(poems)} básní.")

