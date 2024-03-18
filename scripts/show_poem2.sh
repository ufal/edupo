#!/bin/bash

echo 'Content-Type: text/html; charset=utf-8'
echo
echo '<frameset cols = "50%,50%"> <frame src="show_poem.sh?'${1%:*}'" /> <frame src="show_poem.sh?'${1#*:}'" /> </frameset>'

