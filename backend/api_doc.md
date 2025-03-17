# API

Tento dokument: [https://bit.ly/edupo-api-doc](https://bit.ly/edupo-api-doc) 

**TODO: REST API se přesunulo na endpoint [https://quest.ms.mff.cuni.cz/edupo-api/](https://quest.ms.mff.cuni.cz/edupo-api/) \!\!\!**

- použití viz např. [https://github.com/ufal/edupo/blob/main/scripts/rest\_api\_test.py](https://github.com/ufal/edupo/blob/main/scripts/rest_api_test.py)   
- nebo přes curl: [https://github.com/ufal/edupo/blob/main/scripts/rest\_api\_test.sh](https://github.com/ufal/edupo/blob/main/scripts/rest_api_test.sh)     
- podporuje GET i POST  
- umí vracet HTML, JSON a TXT

# General parameters

- accept \= json/txt/html  
  - nebo jde posílat header accept, např. "accept": "application/json"  
- poemid … tim se odkazuje k básni (kromě endpointů který nepracujou s básní s daným id)  
  - v JSONu básně je to ale klíč ‘id’ (tohle asi budem muset sjednotit na ‘poemid’ všude)

# Endpoints & parameters

Vše je pod [https://quest.ms.mff.cuni.cz/edupo/](https://quest.ms.mff.cuni.cz/edupo/) \-- adresa je stejná pro development appku a pro REST API, když na to klikám tak mi jakoby to API vrací HTML a prohlížeč ho zobrazuje… 

## Test jestli to funguje

- **/prdel**  
  - testovací endpoint  
  - nemá žádné parametry (kromě accept, ten má všechno)  
  - [https://quest.ms.mff.cuni.cz/edupo/prdel](https://quest.ms.mff.cuni.cz/edupo/prdel)  
  - [https://quest.ms.mff.cuni.cz/edupo/prdel?accept=txt](https://quest.ms.mff.cuni.cz/edupo/prdel?accept=txt)  
  - [https://quest.ms.mff.cuni.cz/edupo/prdel?accept=json](https://quest.ms.mff.cuni.cz/edupo/prdel?accept=json)

## Kde vzít báseň

4 možnosti → každopádně výsledkem je poemid a s tím se dá pracovat dál

- **/input** \-- vložit text  
  - author \= jméno autora (nepovinné)  
  - title \= název básně (nepovinné)  
  - text \= text básně (povinné)  
  - uloží báseň, vrací poemid (a tu báseň taky)  
  - [https://quest.ms.mff.cuni.cz/edupo/input?text=Kdo%20si%20tady%20hraje%0aten%20si%20tady%20hraje\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/input?text=Kdo%20si%20tady%20hraje%0aten%20si%20tady%20hraje&accept=txt)   
- **/gen** \-- vygenerovat text  
  - všechny parametry jsou nepovinné  
    - zvolej se náhodný hodnoty kdyžtak  
    - některé jsou zatím ignorované…  
    - reálně je nejlepší se podívat na parametry v [https://github.com/ufal/edupo/blob/main/webapp/templates/gen\_input.html](https://github.com/ufal/edupo/blob/main/webapp/templates/gen_input.html)  a na call\_generuj v [https://github.com/ufal/edupo/blob/main/webapp/app.py](https://github.com/ufal/edupo/blob/main/webapp/app.py)   
  - vrací to vygenerovanou báseň a její id  
  - [https://quest.ms.mff.cuni.cz/edupo/gen?metre=D\&rhyme\_scheme=ABBA\&syllables\_count=9\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/gen?metre=D&rhyme_scheme=ABBA&syllables_count=9&accept=txt)   
- **/search** \-- najít v korpuse  
  - query \= string co hledat  
  - use\_regex \= cokoliv/empty … jestli interpretovat query jako regulární výraz  
  - vrací seznam básní z korpusu odpovídajících vyhledávání  
  - [https://quest.ms.mff.cuni.cz/edupo/search?query=Ostrava\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/search?query=Ostrava&accept=txt)   
- vybrat si v korpuse  
  - **/showlist**  
    - bez parametrů, dá seznam autorů  
    - [https://quest.ms.mff.cuni.cz/edupo/showlist?accept=txt](https://quest.ms.mff.cuni.cz/edupo/showlist?accept=txt)   
  - **/showauthor**  
    - author \= jméno autora (tak jak je ve výstupu showlist)  
    - dá seznam sbírek a básní autora  
    - TODO tady je vracení JSONu zatím rozbitý  
    - [https://quest.ms.mff.cuni.cz/edupo/showauthor?author=Bezru%C4%8D,%20Petr\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/showauthor?author=Bezru%C4%8D,%20Petr&accept=txt) 

## Práce s básní

Když už mám poemid, tak s básní můžu dělat různé věci.

Vše chce jeden parametr **poemid** … ten může být získaný libovolným z těch způsobů above, může to tedy být ID básně v databázi anebo ID básně vytvořené generováním či vložené uživatelem… 

Pokud accept=html tak vše kromě show vrací redirect na show?poemid=...

- **/show**  
  - vrátí tu báseň  
  - [https://quest.ms.mff.cuni.cz/edupo/show?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/show?poemid=72197&accept=txt)   
- **/genmotives**  
  - vygeneruje k básni motivy, vrátí ty motivy  
  - [https://quest.ms.mff.cuni.cz/edupo/genmotives?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/genmotives?poemid=72197&accept=txt)   
- **/genimage**  
  - vygeneruje k básni obrázek, vrátí URL obrázku  
  - [https://quest.ms.mff.cuni.cz/edupo/genimage?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/genimage?poemid=72197&accept=txt)   
  - URL je relativní vůči serveru (https://quest.ms.mff.cuni.cz/edupo/)  
- **/gentts**  
  - vygeneruje převedenou báseň na hlas, vrátí URL MP3 souboru  
  - [https://quest.ms.mff.cuni.cz/edupo/gentts?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo/gentts?poemid=72197&accept=txt)   
- **/analyze**  
  - provede versologické analýzy (rýmy, metrum, reduplikanty, slabiky…), vrátí tu báseň podobně jako show  
  - [https://quest.ms.mff.cuni.cz/edupo/analyze?poemid=72197\&accept=json](https://quest.ms.mff.cuni.cz/edupo/analyze?poemid=72197&accept=json)   
  - navíc umí i vstup bez poemid s vytvořením básně stejně jako /input

