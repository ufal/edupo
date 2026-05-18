#!/usr/bin/env python3
#coding: utf-8

import sys
import sqlite3
import requests
import json

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

# DBFILE='/net/projects/EduPo/data/new.db'
DBFILE='/net/projects/EduPo/rur/new_withmood.db'

logging.info(DBFILE)

db = sqlite3.connect(DBFILE, detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row
#db.enable_load_extension(True)
#db.load_extension("./regex0")

sel_books = {
    "Mácha, Karel Hynek": [
      "Máj (in Básně a dramatické zlomky, in Spisy Karla Hynka Máchy, svazek 1)",
    ],
    "Erben, Karel Jaromír": [
      "Kytice z básní",
    ],
    "Neruda, Jan": [
      "Balady a romance",
      "Písně kosmické",
    ],
    "Hálek, Vítězslav": [
      "Večerní písně",
    ],
    "Březina, Otokar": [
      "Tajemné dálky",
      "Svítání na západě",
      "Větry od pólů",
      "Stavitelé chrámu",
      "Ruce",
    ],
    "Karásek ze Lvovic, Jiří": [
      "Zazděná okna",
      "Kniha aristokratická",
      "Sexus necans",
      "Sodoma (in Spisy Jiřího Karáska ze Lvovic, svazek 5)",
    ],
    "Hlaváček, Karel": [
      "Mstivá kantiléna",
      "Pozdě k ránu",
    ],
    "Gellner, František": [
      "Po nás ať přijde potopa!",
      "Radosti života",
    ],
    "Wolker, Jiří": [
      "Těžká hodina",
      "Host do domu",
    ],
    "Nezval, Vítězslav": [
      "Žena v množném čísle",
      "Absolutní hrobař",
      "Praha s prsty deště",
    ],
    "Seifert, Jaroslav": [
      "Město v slzách",
      "Samá láska",
    ],
    "Biebl, Konstantin": [
      "Zlatými řetězy",
      "S lodí, jež dováží čaj a kávu",
    ],
    "Holan, Vladimír": [
      "Příběhy",
      "Noc s Hamletem",
    ],
    "Bondy, Egon": [
      "Básnické spisy I",
    ],
    "Reynek, Bohuslav": [
      "Podzimní motýli",
      "Podzimní motýli; Sníh na zápraží; Mráz v okně",
      "Žízně",
      "Rty a zuby",
      "Odlet vlaštovek",
      "Pieta",
      "Smutek země",
      "Setba samot",
    ],
    "Diviš, Ivan": [
      "První hudba bratřím",
      "Balada z regálu",
    ],
    "Krchovský, J. H.": [
      "Já už chci domů",
      "Poslední list",
    ],
    "Hruška, Petr": [
      "Obývací nepokoje",
      "Vždycky se ty dveře zavíraly",
      "Auta vjíždějí do lodí",
    ],
    "Správcová, Božena": [
      "Guláš z modrý krávy",
      "Východ",
      "Večeře",
      "Samomluvy",
      "Strašnice",
      "Požární kniha",
    ],
    "Stehlíková, Olga": [
      "Vykřičník jak stožár",
      "0 čem mluví Matka, když mlčí",
      "Týdny",
    ],
    "Rudčenková, Kateřina": [
      "Ludwig",
      "Není nutné, abyste mě navštěvoval",
      "Chůze po dunách",
    ],
    "Malý, Radek": [
      "Lunovis",
      "Vraní zpěvy",
      "Světloplaší",
      "Malá tma",
      "Větrní",
      "Všehomír",
      "Atlas bytostí",
    ],
    "Borkovec, Petr": [
      "Polní práce",
      "Prostírání do tichého",
      "Mezi oknem, stolem a postelí",
      "Poustevna, věštírna, loutkárna",
      "Ochoz",
    ],
    "Iljašenko, Marie": [
      "Osip míří na jih",
      "Sv. Outdoor",
    ],
    "Těsnohlídek, Jan": [
      "Rakovina",
      "Hranice a zdi",
      "Hlavně zachraň sebe",
      "Násilí bez předsudků",
      "Ještě je co ztratit",
    ],
    "Jirous, Ivan Martin": [
      "Úloža",
      "Okuje",
      "Rattus norvegicus",
      "Ubíječ labutí",
      "Rok krysy",
    ],
    "Wernisch, Ivan": [
      "Don Čičo má v klopě orchidej",
      "Z dalekých žofínů",
      "Růžovejch květů sladká vůně",
      "Pekařova noční nůše",
      "Na břehu",
      "Ó kdežpak",
      "Bez kufru se tak pěkně skáče po stromech neboli Nún",
      "Lunojasno, když kolovrátky",
      "Dřevěný dort",
      "Zeleně bliká Hilversum",
      "Ztroskotanec na břehu atlantském",
      "Frc",
      "S brokovnicí pod kabátem",
      "Penthesilea",
      "Nikam",
      "Zlatomodrý konec stařičkého léta",
      "Proslýchá se",
      "Hlava na stole",
    ],
    "Fischerová, Viola": [
      "Domek na vinici",
      "Matečná samota",
      "Odrostlá blízkost",
      "Jak pápěří",
      "Divoká dráha domovů",
      "Babí hodina",
      "Zádušní mše za Pavla Buksu",
      "Nyní",
      "Předkonec",
      "Písečné dítě",
    ],
    "Hrabě, Václav": [
      "Blues pro bláznivou holku",
    ],
}

db.execute("ALTER TABLE poems ADD COLUMN selected INT;")

for author in sel_books:
    for coll in sel_books[author]:
        # print(f'\n=== {author} ===')
        sql = 'SELECT id FROM books WHERE author=? AND title=?'
        result = db.execute(sql, (author,coll))
        for row in result.fetchall():
            print(row['id'])
            # print(f'      "{row[0]}",')
            if not row['id'] in (2968, 3905, 3925):
                sql = f"UPDATE poems SET selected = 1 WHERE book_id={row['id']};"
                db.execute(sql)

db.commit()
db.close()

