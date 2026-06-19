#!/bin/bash

# U=https://quest.ms.mff.cuni.cz/edupo-api
U=https://edupo.cz/api

curl --header "Accept: text/plain" $U/prdel

curl -X POST --header "Accept: text/plain" $U/prdel


# text/plain, text/html, application/json
curl --header "Accept: text/plain" $U/gen

echo
echo

curl --data "poemid=78467" --header "Accept: text/plain" $U/show

echo
echo

curl --data "poemid=78467&accept=txt" $U/genmotives

echo
echo

curl -X POST --data "rhyme_scheme=ABBA" --data "metre=J" --header "Accept: application/json" $U/gen \
    | python3 -m json.tool --no-ensure-ascii
