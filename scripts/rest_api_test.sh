#!/bin/bash

# text/plain, text/html, application/json
curl --header "Accept: text/plain" https://quest.ms.mff.cuni.cz/edupo-api/gen

echo
echo

curl --data "poemid=78467" --header "Accept: text/plain" https://quest.ms.mff.cuni.cz/edupo-api/show

echo
echo

curl --data "poemid=78467&accept=txt" https://quest.ms.mff.cuni.cz/edupo-api/genmotives

echo
echo

curl -X POST --data "rhyme_scheme=ABBA" --data "metre=J" --header "Accept: application/json" https://quest.ms.mff.cuni.cz/edupo-api/gen \
    | python3 -m json.tool --no-ensure-ascii
