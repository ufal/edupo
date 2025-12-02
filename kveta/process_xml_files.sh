#!/usr/bin/env bash

INPUT_DIR="/net/projects/EduPo/data/KCV_ROBERT_listopad_2025"
OUTPUT_DIR="/net/projects/EduPo/data/KCV_ROBERT_okvetovano"

for file in "$INPUT_DIR"/*.xml; do
    echo "Processing $file..."
    basename=$(basename "$file" .xml)
    python3 okvetuj_xml.py "$file" $OUTPUT_DIR/${basename// /_}
done
