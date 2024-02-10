## Skládání stránek

Stránky jsou primárně v HTML.

Dynamiky se dosahuje tím, že tam jsou kapitálkama parametry, keré se nahradí vhodnými hodnotami.
Takže typicky věci jako TEXT, TITLE, IMAGE, KEY... jsou automaticky nahrazeny za správné hodnoty.

Většina stránek jsou tak jednoduché, že ani nemají vlastní PY skript. Místo toho používají společný skript `page.py`, který podle hodnoty parametru `page` zobrazí správný HTML soubor (a případně dle hodnoty parametru `replacements` nahradí zadané parametry).
Parametr může být GET i POST, takže stránku lze zobrazit buď skrzevá formulář, který má `action="page.py"` a skrze hidden input definuje hodnotu parametru `page`; ale taky lze prostě udělat odkaz na `page.py?page=stranka`.
Hodnota parametru `page` je název HTML souboru *bez přípony*; tj. např. `page.py?page=credits` zobrazí stránku `credits.html`.

Není ale dobré odkazovat přímo na HTML soubor, protože pak by tam chyběl header a footer

## Skládání složitějších stránek

### share.py / post.py
Prostě jak se výsledky skládají do stránky, která se pak sdílí a promítá atd...

Vezmou se vstupy z parametrů, postupně se za sebe naskládají, a vytvořené HTML se uloží do souboru `genouts/{key}.html` (key je datum a čas vygenerování příspěvku)

Jednotlivé parametry se vizualizují skrzevá různé html soubory s návodným jménem, v tomto pořadí:
* title: název příspěvku (share_title.html)
* text: textový obsah příspěvku; nikoliv konverzace s Wolkerem (share_text.html)
* messages: jednotlivé zprávy z konverzace s Wolkerem (konverzaci identifikuje parametr thread_id); sekvence střídajících se zpráv uživatele (user) a chatbota (assistant), vizualizované skrzevá soubory pro jednotlivé zprávy:
  * share_message_user.html
  * share_message_assistant.html
* image: vygenerovaný obrázek (share_image.html)
* author: jméno autora aneb uživatele (share_author.html)

### wolker_chat.py
Chatování s Wolkerem:
* wolker_chat_head.html (aktuálně prázdné)
* jednotlivé zprávy z konverzace s Wolkerem; sekvence střídajících se zpráv uživatele (user) a chatbota (assistant), vizualizované skrzevá soubory pro jednotlivé zprávy:
  * wolker_chat_message_user.html
  * wolker_chat_message_assistant.html
* wolker_chat_controls.html (zadávání odpovědí, sdílení...)

### welcome_wolker_feel.py
Generování k básní:
* welcome_wolker_feel.html
  * COUNT: nahradí se za počet básní
  * POEMS: nahradí se za jednotlivé básně (COUNT-krát za sebe slepené `poem.html`)
* poem.html -- pro každou báseň
  * POEMID: 0 až COUNT-1
  * TITLE: název
  * TEXT: text, nyní s opravdovými newlines (proto je to uvnitř `<pre>`); můžu tam provést nahrazní newlines za `<br>` když mi někdo řekne :-)

### wolker_image.py
Výsledek generování obrázku:
* result_image.html
* result_image_backlink.html -- pokud je vyplněný parametr `back`, zobrazí se i tato stránka, umožňující jít o krok zpět a upravit prompt

### gallery.py
* gallery_admin_head.html (pokud je to admin)
* gallery_head.html
* pro každý příspěvek:
  * `genouts/{key}.html`
  * gallery_admin_sharebutton.html (pokud je to admin)
  * gallery_sep.html
