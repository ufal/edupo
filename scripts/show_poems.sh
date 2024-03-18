#!/bin/bash

echo 'Content-Type: text/html; charset=utf-8'
echo

echo '<ul>'
cd ccv-new-summary-gpt4
for f in *
do
    echo '<li>'$f
    echo '<a href="show_poem.sh?ccv-new-summary/'$f'">Mixtral</a>'
    echo '<a href="show_poem.sh?ccv-new-summary-gpt4/'$f'">GPT4</a>'
done
echo '</ul>'


