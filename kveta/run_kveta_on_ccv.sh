#!/bin/bash

INPUT_DIR=/net/projects/EduPo/data/KCV_komplet/ccv
OUTPUT_DIR=/net/projects/EduPo/data/KCV_analyzed
RUN_FILE=run_temp.sh
        
INTRO="#!/bin/bash\n#SBATCH -J kveta\n#SBATCH -p cpu-troja\n\nsource ~/troja/virtualenv/edupo/bin/activate\n"

echo -e $INTRO > $RUN_FILE

counter=0
for input_file in $INPUT_DIR/*.json
do  
    basename=$(basename ${input_file});
    echo "python kveta.py $input_file $OUTPUT_DIR/$basename" >> $RUN_FILE;
    counter=$((counter+1));
    if [ $counter -eq 1000 ]; then
        sbatch $RUN_FILE;
        echo -e $INTRO > $RUN_FILE;
        counter=0;
    fi
done
sbatch $RUN_FILE
