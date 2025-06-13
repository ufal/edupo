#!/bin/bash

# tts --list_models
# tts_models/cs/cv/vits

tts --text "$(cat text.txt)" --model_name tts_models/cs/cv/vits --out_path new-coqui.wav

# espeak -g 12 -p 80  -v cs -f text.txt -w espeak.wav
