# Květa - automatická anotace české poezie

- morfologická a syntaktická analýza
- fonetický přepis
- detekce rýmů a reduplikantů
- určení počtu slabik, přízvuků, metra, ...

`pip install -r requirements.txt`

## Automatická anotace básně v plaintextu:
`kveta.py basen.txt basen.json`

## Automatická anotace existující básně z Korpusu české poezie:
Extrahuje se pouze text z formátu JSON, ostatní anotace se zahodí a vygenerují se nové automatické anotace

`kveta.py input.json output.json`

