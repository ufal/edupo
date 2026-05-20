import os
import re
import sys

# cesta k vstupnímu souboru
input_file = sys.argv[1]
output_dir = sys.argv[2]

# vytvoření složky pro výstupy
os.makedirs(output_dir, exist_ok=True)

# načtení souboru
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# rozdělení podle <|begin_of_text|>
sections = [s.strip() for s in text.split("<|begin_of_text|>") if s.strip()]

for i, section in enumerate(sections, start=1):
    lines = section.splitlines()
    processed_lines = []
    previous_blank = False  # sleduje, zda už byl prázdný řádek

    for line in lines:
        stripped = line.strip()

        if not stripped:  # prázdný řádek
            if not previous_blank and processed_lines:
                processed_lines.append("")  # zachovej max 1 prázdný
                previous_blank = True
            continue

        if line.count("#") == 4:
            # vyber text za posledním #
            match = re.search(r"#([^#]+)$", line)
            if match:
                processed_lines.append(match.group(1).strip())
                previous_blank = False

    # přeskoč sekce bez obsahu
    if processed_lines:
        cleaned_text = "\n".join(processed_lines).strip()

        # zápis do souboru
        output_path = os.path.join(output_dir, f"poem_{i:03d}.txt")
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(cleaned_text)

