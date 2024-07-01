# Dvouhlásky

## Soubory

- *diphtongs.py* převádí slovník z formátu `orto,phoebe` do formátu "slovo na řádek, potenciální dvouhlásky rozdělené `-`, pokud dvouhláskou nejsou"
- *hyphenator.py* třída, která načte patterns a rozděluje potenciální dvouhlásky
- *validate.py* spočítá accuracy patternů na slovníku
- *create_val_data.py* vyrobí data rozdělená pro cross-validaci; předpokládá, že slova se v datech neopakují
- *diphthongs_from_corpus.py* vybere z korpusu slova s (potenciálními) dvouhláskami a vypíše je ve formátu `orto,phoebe`
- *run_patgen.sh* vyrobí soubor s patterny

## Potenciální vylepšení

- dodat víc dat
- váhy podle četnosti v datech (see cshyphen, vypadá to, že s tím nějak pracují)
- tunit hyperparametry trénování patternů (see cshyphen)

## Copyright

`czech.tra` and `patgen` copied from https://github.com/tensojka/cshyphen
