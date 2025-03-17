# EduPo REST API Dokumentace

## Obecné informace

REST API nyní běží na endpointu:  
**[https://quest.ms.mff.cuni.cz/edupo-api/](https://quest.ms.mff.cuni.cz/edupo-api/)**

Podporuje:
- Metody **GET** a **POST**
- Formáty odpovědí: **HTML, JSON, TXT**
- Použití viz:
    - v Pythonu (implementace frontendu): [https://github.com/ufal/edupo/blob/main/frontend/app.py](https://github.com/ufal/edupo/blob/main/frontend/app.py)
    - v Pythonu (několik ukázek použití) [https://github.com/ufal/edupo/blob/main/scripts/rest\_api\_test.py](https://github.com/ufal/edupo/blob/main/scripts/rest_api_test.py)   
    - přes curl: [https://github.com/ufal/edupo/blob/main/scripts/rest\_api\_test.sh](https://github.com/ufal/edupo/blob/main/scripts/rest_api_test.sh)     

## Obecné parametry

- **accept** = `json` / `txt` / `html`
  - Nebo lze posílat v hlavičce jako `"accept": "application/json"`
- **poemid** – unikátní identifikátor básně (povinné pro některé endpointy)
    - ve vraceném JSONu někdy jako `id`

## Formát výstupu

- pokud to vrací báseň, tak:
  - HTML: určené pro zobrazení
  - TXT: plaintext s názvem, autorem a textem básně (co verš to řádek, hranice
    slok = prázdný řádek)
  - JSON: báseň ve formátu viz [dokumentace](https://github.com/ufal/edupo/blob/main/docs/json_doc.md)

## Endpoints

### Test spojení
`/prdel`
- Vrací testovací odpověď.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/prdel](https://quest.ms.mff.cuni.cz/edupo-api/prdel)  
  - [https://quest.ms.mff.cuni.cz/edupo-api/prdel?accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/prdel?accept=txt)  
  - [https://quest.ms.mff.cuni.cz/edupo-api/prdel?accept=json](https://quest.ms.mff.cuni.cz/edupo-api/prdel?accept=json)

### Vložení nové básně
`/input`
- Parametry:
  - `author` = Jméno autora (nepovinné)
  - `title` = Název básně (nepovinné)
  - `text` = Text básně (povinné)
- Vrací: **poemid** nové básně.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/input?text=Kdo%20si%20tady%20hraje%0aten%20si%20tady%20hraje\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/input?text=Kdo%20si%20tady%20hraje%0aten%20si%20tady%20hraje&accept=txt)   

### Generování básně
`/gen`
- Parametry (nepovinné, náhodné hodnoty pokud nejsou zadány):
  - `metre` = Např. `T` (trochej), `J` (jamb), `D` (daktyl)
  - `rhyme_scheme` = Např. `ABBA`
  - `syllables_count` = Počet slabik na řádek
  - `author`
  - `title`
  - `modelspec`
  - `first_words`
  - `temperature`
  - a další parametry, viz [vstupní formulář](https://github.com/ufal/edupo/blob/main/backend/templates/gen_input.html)
- Vrací: **poemid** generované básně a vlastní vygenerovanou báseň.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/gen?metre=D\&rhyme\_scheme=ABBA\&syllables\_count=9\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/gen?metre=D&rhyme_scheme=ABBA&syllables_count=9&accept=txt)   

### Vyhledání básně v korpusu
`/search`
- Parametry:
  - `query` = Hledaný text
  - `use_regex` = `true` / `''` (volitelné, pokud má být použit regulární výraz)
- Vrací: Seznam odpovídajících básní.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/search?query=Ostrava\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/search?query=Ostrava&accept=txt)   

### Zobrazení seznamu autorů
`/showlist`
- Vrací: Seznam autorů dostupných v databázi.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/showlist?accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/showlist?accept=txt)   

`/showauthor`
- Parametry:
  - `author` = Jméno autora (tak jak je ve výstupu `showlist`)
- Vrací: Seznam sbírek a básní autora.
- Příklad:  
    - [https://quest.ms.mff.cuni.cz/edupo-api/showauthor?author=Bezru%C4%8D,%20Petr\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/showauthor?author=Bezru%C4%8D,%20Petr&accept=txt) 

### Zobrazení básně
`/show`
- Parametry:
  - `poemid` = ID básně
- Vrací: Text básně.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/show?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/show?poemid=72197&accept=txt)   

### Generování motivů básně
`/genmotives`
- Parametry:
  - `poemid` = ID básně
- Vrací: Seznam automaticky odhadnutých motivů básně.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/genmotives?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/genmotives?poemid=72197&accept=txt)   

### Generování ilustrace k básni
`/genimage`
- Parametry:
  - `poemid` = ID básně
- Vrací: URL obrázku (relativní vůči serveru)
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/genimage?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/genimage?poemid=72197&accept=txt)   

### Generování zvukového výstupu (TTS)
`/gentts`
- Parametry:
  - `poemid` = ID básně
- Vrací: URL MP3 souboru s přednesem básně (relativní vůči serveru).
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/gentts?poemid=72197\&accept=txt](https://quest.ms.mff.cuni.cz/edupo-api/gentts?poemid=72197&accept=txt)   

### Analýza básně
`/analyze`
- Parametry:
  - `poemid` = ID básně
  - anebo parametry jako u `input` pro báseň co dosud nemá poemid
- Vrací: Versologickou analýzu básně.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/analyze?poemid=72197\&accept=json](https://quest.ms.mff.cuni.cz/edupo-api/analyze?poemid=72197&accept=json)   

---

## Změny oproti předchozí verzi

1. **Změněn hlavní endpoint** z `https://quest.ms.mff.cuni.cz/edupo/` na `https://quest.ms.mff.cuni.cz/edupo-api/`.
2. **Aktualizovány URL ve všech příkladech**.
3. **Přidány nové endpointy** podle aktuální verze API v aplikaci.
4. **Upřesněny popisy parametrů a návratových hodnot**.
