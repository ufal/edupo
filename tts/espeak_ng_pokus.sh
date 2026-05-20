#!/bin/bash

espeak-ng -v cs -f text.txt -w espeakng-basic.wav
espeak-ng -g 12 -p 80  -v cs -f text.txt -w espeakng.wav
