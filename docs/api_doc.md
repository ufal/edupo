# EduPo REST API Dokumentace

## Obecné informace

REST API nyní běží na endpointu:  
**[https://edupo.cz/api/](https://edupo.cz/api/)**

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
  - [https://edupo.cz/api/prdel](https://edupo.cz/api/prdel)  
  - [https://edupo.cz/api/prdel?accept=txt](https://edupo.cz/api/prdel?accept=txt)  
  - [https://edupo.cz/api/prdel?accept=json](https://edupo.cz/api/prdel?accept=json)

### Vložení nové básně
`/input`
- Parametry:
  - `author` = Jméno autora (nepovinné)
  - `title` = Název básně (nepovinné)
  - `text` = Text básně (povinné)
- Vrací: **poemid** nové básně.
- Příklad:  
  - [https://edupo.cz/api/input?text=Kdo%20si%20tady%20hraje%0aten%20si%20tady%20hraje\&accept=txt](https://edupo.cz/api/input?text=Kdo%20si%20tady%20hraje%0aten%20si%20tady%20hraje&accept=txt)   

### Úplná specifikace parametrů pro generování
`/get_generation_parameters_specification`
- Vrací: JSON schéma třídy `GenerationParameters` (viz [`backend/data_types.py`](https://github.com/ufal/edupo/blob/main/backend/data_types.py)) popisující všechny parametry generování a jejich typy/výchozí hodnoty.
- Příklad:
  - [https://edupo.cz/api/get_generation_parameters_specification?accept=json](https://edupo.cz/api/get_generation_parameters_specification?accept=json)

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
  - [https://edupo.cz/api/gen?metre=D\&rhyme\_scheme=ABBA\&syllables\_count=9\&accept=txt](https://edupo.cz/api/gen?metre=D&rhyme_scheme=ABBA&syllables_count=9&accept=txt)   

### Interaktivní generování básně
`/geninter`
- Generuje báseň po částech (verších/skupinách veršů) s možností postupného doplňování ze strany uživatele.
- Parametry:
  - `interactive_mode` = režim interakce (výchozí `lines_gh`)
  - `modelspec` = identifikátor modelu (výchozí `mc`)
  - `title` = název básně (výchozí `Bez názvu`)
  - `metre` = `T` / `J` / `D` / `N` (výchozí `T`)
  - `rhyme_scheme` = např. `AABB` (výchozí `AABB`)
  - `syllables_count` = počet slabik na řádek (výchozí `8`)
  - `poemid` = ID rozpracované básně (volitelné, pro pokračování)
  - `rawtext` = dosud vygenerovaný „surový“ text (pro pokračování)
  - `userinput` = vstup uživatele (verš/část přidaná uživatelem)
- Vrací: další část generované básně (a její `poemid`).

### Přegenerování (oprava) jednoho verše
`/regen`
- Parametry:
  - `poemid` = ID básně, kterou chceme upravit (povinné)
  - `badline` = přesné znění verše, který má být nahrazen (povinné)
- Vrací: novou verzi básně (s novým `poemid`), v níž je `badline` nahrazen verzí navrženou modelem (OpenAI). Nový verš se snaží zachovat rým a metrum původního verše.

### Vyhledání básně v korpusu
`/search`
- Parametry:
  - `query` = Hledaný text
  - `use_regex` = `true` / `''` (volitelné, pokud má být použit regulární výraz)
- Vrací: Seznam odpovídajících básní.
- Příklad:  
  - [https://edupo.cz/api/search?query=Ostrava\&accept=txt](https://edupo.cz/api/search?query=Ostrava&accept=txt)   

### Zobrazení seznamu autorů
`/showlist`
- Vrací: Seznam autorů dostupných v databázi.
- Příklad:  
  - [https://edupo.cz/api/showlist?accept=txt](https://edupo.cz/api/showlist?accept=txt)   

`/showlistgen`
- Vrací: seznam ID vygenerovaných básní (uložených jako JSON ve `static/poemfiles`), seřazený sestupně.
- Příklad:
  - [https://edupo.cz/api/showlistgen?accept=txt](https://edupo.cz/api/showlistgen?accept=txt)

`/showauthor`
- Parametry:
  - `author` = Jméno autora (tak jak je ve výstupu `showlist`)
- Vrací: Seznam sbírek a básní autora.
- Příklad:  
    - [https://edupo.cz/api/showauthor?author=Bezru%C4%8D,%20Petr\&accept=txt](https://edupo.cz/api/showauthor?author=Bezru%C4%8D,%20Petr&accept=txt) 

### Typologické rysy autora
`/typfeatures`
- Parametry:
  - `author` = jméno autora (pokud není zadáno, použije se výchozí seznam autorů: Mácha, Erben, Neruda, Hálek, Březina, Karásek ze Lvovic, Hlaváček, Gellner, Bezruč)
- Vrací: textový přehled typologických rysů autora/autorů (počty básní a sbírek, top metra, top rýmová schémata, top motivy, typická slova podle TF-IDF). Aktuálně vrací jen plain text.
- Příklad:
  - [https://edupo.cz/api/typfeatures?author=Bezru%C4%8D,%20Petr](https://edupo.cz/api/typfeatures?author=Bezru%C4%8D,%20Petr)

### Zobrazení básně
`/show`
- Parametry:
  - `poemid` = ID básně
- Vrací: Text básně.
- Pokud není zadané `poemid`, vrací náhodnou báseň.
- Příklad:  
  - [https://edupo.cz/api/show?poemid=72197\&accept=txt](https://edupo.cz/api/show?poemid=72197&accept=txt)   

### Generování motivů básně
`/genmotives`
- Parametry:
  - `poemid` = ID básně
- Vrací: Seznam automaticky odhadnutých motivů básně.
- Příklad:  
  - [https://edupo.cz/api/genmotives?poemid=72197\&accept=txt](https://edupo.cz/api/genmotives?poemid=72197&accept=txt)   

### Odhad nálady básně
`/guessmood`
- Parametry:
  - `poemid` = ID básně (povinné)
  - `regenerate` = pokud je nastaveno (nenulové), vynutí nový odhad i pokud je již uložen
- Vrací: jedno ze slov `veselá` / `smutná` / `žádná` (odhad převládající nálady básně).
- Výsledek se cachuje do `static/mood/{poemid}.txt`.

### Generování ilustrace k básni
`/genimage`
- Parametry:
  - `poemid` = ID básně
- Vrací: URL obrázku (relativní vůči serveru)
- Příklad:  
  - [https://edupo.cz/api/genimage?poemid=72197\&accept=txt](https://edupo.cz/api/genimage?poemid=72197&accept=txt)   

### Generování zvukového výstupu (TTS)
`/gentts`
- Parametry:
  - `poemid` = ID básně
- Vrací: URL MP3 souboru s přednesem básně (relativní vůči serveru).
- Příklad:  
  - [https://edupo.cz/api/gentts?poemid=72197\&accept=txt](https://edupo.cz/api/gentts?poemid=72197&accept=txt)   

### Překlad básně
`/translate`
- Parametry:
  - `poemid` = ID básně (povinné)
  - `language` = cílový jazyk (výchozí `sk`). Pro `sk` se používá služba Česílko (CS→SK), pro ostatní jazyky překladač LINDAT (`cs-<language>`, např. `uk`).
- Vrací: text přeloženého textu básně. Překlad se uloží do dat básně pod klíčem `translations[language]`.

### Analytické zpracování básně modelem LLM
`/processopenai`
- Aplikuje libovolný uživatelský prompt na zadanou báseň pomocí LLM (OpenAI / OpenRouter).
- Parametry:
  - `poemid` = ID básně (povinné)
  - `openaiprompt` = systémový/instrukční prompt aplikovaný na text básně (povinné)
  - `modelspec` = identifikátor modelu (výchozí `gpt-4o-mini`)
- Vrací: výstup modelu. Záznamy `{model, prompt, output}` se kumulují v poli `openai` v datech básně.

### Volné generování textu modelem LLM
`/openaigenerate`
- Parametry:
  - `prompt` = prompt pro model (výchozí `Máte rádi ptakopysky?`)
- Vrací: HTML stránku s výstupem modelu (jednoduché rozhraní, vrací vždy HTML).

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
  - [https://edupo.cz/api/analyze?poemid=72197\&accept=json](https://edupo.cz/api/analyze?poemid=72197&accept=json)   
  - [https://edupo.cz/api/analyze?text=Sedí losos na jabloni. Má své oči na mamoni.](https://edupo.cz/api/analyze?text=Sed%C3%AD%20losos%20na%20jabloni.%0AM%C3%A1%20sv%C3%A9%20o%C4%8Di%20na%20mamoni.)

---

## Změny oproti předchozí verzi

1. **Změněn hlavní endpoint** z `https://quest.ms.mff.cuni.cz/edupo/` na `https://quest.ms.mff.cuni.cz/edupo-api/`.
2. **Aktualizovány URL ve všech příkladech**.
3. **Přidány nové endpointy** podle aktuální verze API v aplikaci.
4. **Upřesněny popisy parametrů a návratových hodnot**.
5. **Hlavní endpoint přesunut** na `https://edupo.cz/api/`. Dřívější adresa `https://quest.ms.mff.cuni.cz/edupo-api/` zůstává funkční (tatáž instance je dostupná pod oběma adresami).
