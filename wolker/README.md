## Skládání složitějších stránek

### share.py / post.py
Prostě jak se výsledky skládají do stránky, která se pak sdílí a promítá atd...

Vezmou se vstupy z parametrů, postupně se za sebe naskládají, a vytvořené HTML se uloží do souboru `genouts/key.html`

Jednotlivé parametry se vizualizují skrzevá různé html soubory s návodným jménem, v tomto pořadí:
* title: název příspěvku (share_title.html)
* text: textový obsah příspěvku; nikoliv konverzace s Wolkerem (share_text.html)
* messages: jednotlivé zprávy z konverzace s Wolkerem (konverzaci identifikuje parametr thread_id); sekvence střídajících se zpráv uživatele (user) a chatbota (assistant), vizualizované skrzevá soubory pro jednotlivé zprávy:
  * share_message_user.html
  * share_message_assistant.html
* image: vygenerovaný obrázek (share_image.html)
* author: jméno autora aneb uživatele (share_author.html)

### wolker_image.py
Výsledek generování obrázku:
* result_image.html
* result_image_backlink.html -- pokud je vyplněný parametr `back`, zobrazí se i tato stránka, umožňující jít o krok zpět a upravit prompt

### gallery.py
* gallery_admin_head.html (pokud je to admin)
* gallery_head.html
