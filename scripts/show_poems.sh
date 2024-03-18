#!/bin/bash

echo 'Content-Type: text/html; charset=utf-8'
echo

echo '<ul>'
cd ccv-new-summary-gpt4
for f in *
do
    echo '<li>'
    echo '<a href="show_poem2.sh?ccv-new-summary/'$f':ccv-new-summary-gpt4/'$f'">'$f'</a>'
done
echo '</ul>'


