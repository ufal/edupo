#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

# ufal page does not want to be embedded from outside ufal server, so this
# best works at the ufal server at:
# https://ufal.mff.cuni.cz/~rosa/edupo_dashboard.html


print("Content-Type: text/html; charset=utf-8")
print()

print(f"""
<!DOCTYPE html>
<html>

   <head>
      <title>EduPo Dashboard</title>
   </head>
	
   <frameset cols = "30%,40%,30%">
        <frameset rows = "50%,30%,20%">
            <frame name="slack" src="https://ufallab.ms.mff.cuni.cz/cgi-bin/rosa/edupo/slack.sh" />
            <frame name="gdrive" src="https://drive.google.com/embeddedfolderview?id=1HmhDCfEumzPW86_8awlCk9pmj4OzBq6j" />   
            <frame name="kalendar" src="https://calendar.google.com/calendar/embed?src=d59de8c7405c7445b7d7e959fc35be3fc6f9ca8f15c1c7cd9a35863aa44ff8f3%40group.calendar.google.com&ctz=Europe%2FPrague&mode=AGENDA">
        </frameset>
        <frame name="web" src="https://ufal.mff.cuni.cz/grants/edupo" />
        <frameset rows = "60%,20%,20%">
            <frame name="zotero" src="https://widgets.sociablekit.com/rss-feed/iframe/251731">
            <frame name="commits" src="https://tylerlh.github.io/github-latest-commits-widget/?username=ufal&repo=edupo&limit=10" />
            <frame name="kontakty" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSk8kjmuJ0u48FQSoPheQFAyPkYWm8V-2TU-hjQIROsHvKKrUIzSP4GrfUGEWwecT7OPPDNFiOoOrAQ/pubhtml?gid=0&single=true">
        </frameset>
   </frameset>
   
</html>
""")

