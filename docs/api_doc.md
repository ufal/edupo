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
  - `modelspec` = identifikátor našeho modelu (starý 'mc', nový 'tm') nebo komerčního modelu (např. 'gpt-4o-mini' nebo 'google/gemini-3.1-pro-preview'); některé modely podporují jen některé options (komerční podporují všechny options)
  - `title` = např. `V lese`
  - `author` = např. `Mácha, Karel Hynek`
  - `collection_style` = např. `Hřbitovní kvítí` (styl sbírky)
  - `metre` = `T` (trochej), `J` (jamb), `D` (daktyl), `N` (volný)
  - `rhyme_scheme` = Např. `ABBA` (platí pro první sloku; lze zadat i pro několik slok, např. `ABBA XCXC`)
  - `syllables_count` = Počet slabik na řádek (platí pro první verš), např. `9`; podporuje i obecnější specifikátory `short` a `long`
  - `verses_count` = Počet veršů (v první sloce), např. `6` (lze zadat i počty veršů pro několik slok, např. `4 4 3 3`)
  - `max_strophes` = Maximální počet slok, např. `2`
  - `poem_length` = `short`/`medium`/`long`
  - `form` = Pevná forma, např. `sonet`, `haiku` nebo `gazel`
  - `motives` = Motivy, např. `láska` nebo `ztráta bližního`; může být i víc motivů oddělených konci řádků, např. `láska\nnenávist`
  - `rhymed` = `yes` / `no`
  - `old_style` = `old` / `modern` / `contemporary`
  - `mood` = `veselá` / `smutná`
  - `first_words`
  - `temperature`
  - `max_tries`
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
- Pokud není zadané `poemid`, vrací náhodnou báseň.
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

### Lajkování
`/like_count`
- Parametry:
  - `poemid` = ID básně
- Vrací: počet lajků básně.

`/add_like`
- Parametry:
  - `poemid` = ID básně
- Vrací: počet lajků básně (předtím ho zvýší o 1).

### Analýza básně
`/analyze`
- Parametry:
  - `poemid` = ID básně
  - anebo `text` = text básně (a případně další parametry jako u `input`) pro báseň co dosud nemá poemid
- Vrací: Versologickou analýzu básně.
- Příklad:  
  - [https://quest.ms.mff.cuni.cz/edupo-api/analyze?poemid=72197\&accept=json](https://quest.ms.mff.cuni.cz/edupo-api/analyze?poemid=72197&accept=json)   
  - [https://quest.ms.mff.cuni.cz/edupo-api/analyze?text=Sedí losos na jabloni. Má své oči na mamoni.](https://quest.ms.mff.cuni.cz/edupo-api/analyze?text=Sed%C3%AD%20losos%20na%20jabloni.%0AM%C3%A1%20sv%C3%A9%20o%C4%8Di%20na%20mamoni.)

---

## Změny oproti předchozí verzi

1. **Změněn hlavní endpoint** z `https://quest.ms.mff.cuni.cz/edupo/` na `https://quest.ms.mff.cuni.cz/edupo-api/`.
2. **Aktualizovány URL ve všech příkladech**.
3. **Přidány nové endpointy** podle aktuální verze API v aplikaci.
4. **Upřesněny popisy parametrů a návratových hodnot**.
