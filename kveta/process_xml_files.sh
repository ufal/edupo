#!/usr/bin/env bash

#INPUT_DIR="/net/projects/EduPo/data/KCV_ROBERT_listopad_2025"
#OUTPUT_DIR="/net/projects/EduPo/data/KCV_ROBERT_okvetovano"
INPUT_DIR="/net/projects/EduPo/data/KSP_od_Karla/XML_brezen_2022"
OUTPUT_DIR="/net/projects/EduPo/data/KSP_od_Karla_okvetovano/XML_brezen_2022"

from_file="Bondy_Basnicke_spisy_I_2014_IV"
kvetuj=true

for file in "$INPUT_DIR"/*.xml; do
    echo "Processing $file..."
    basename=$(basename "$file" .xml)
    if [[ "$basename" == "$from_file" ]]; then
        kvetuj=true
    fi
    if $kvetuj; then
        python3 okvetuj_xml.py "$file" $OUTPUT_DIR/${basename// /_}
    fi
done
