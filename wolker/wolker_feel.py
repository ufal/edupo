#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
from image_generation import get_image_for_line
import random

print("Content-type: text/html")
print()

print(f"""
<!DOCTYPE html>
    <html lang="cs">
    <head>
        <title>Pocity z Wolkerovy poezie</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Pocity z Wolkerovy poezie</h1>
""")
        

nazvy = ["Okna", "Pokora", "Těžká hodina"]
titles = ["Windows", "Humility", "Hard hour"]

basne = [
"""Okna

Okno je skleněná loď,
připoutaná k břehům mé světnice.
Mladý námořník nepotřebuje sedmimílové střevíce.
Vsedne a odjede;
každou chvílí
urazí očima dychtivýma deset tisíc mílí
nad mořem
po nebi krásném a širokém.

Bílá oblaka,
bílé skály,
Afriku i Australii jsme zcestovali,
s černochy se pobratřili,
Indiány navštívili.
Našli jsme i nové světadíly,
ze všech světadílů nejmladší,
to vše ale nestačí,
abychom se zastavili.

Svět je kulatý.
Po mnoha dobrodružstvích rád vrátíš se zase 
do nízké světničky, která zavírá se
nad starými známými věcmi.
U rozviklaného stolu mezi dvěma vysychajícími kalamáři
nejlépe uplatníš povídku s polární září.
Vše bude tiché a štastné — ty sám nejvíce.
Oči své položíš doprostřed světnice: 
dáreček z cesty —
— album světa.""",

"""Pokora

Stanu se menším a ještě menším,
až budu nejmenším na celém světě.

Po ránu, na louce, v létě
po kvítku vztáhnu se nejmenším.
Zašeptám, až se obejmu s ním:
„Chlapečku bosý,
nebe dlaň o tebe opřelo si
kapičkou rosy,
aby nespadlo.“""",

"""TĚŽKÁ HODINA

Přišel jsem na svět,
abych si postavil život
dle obrazu srdce svého.

Chlapecké srdce je písnička na začátku,
plán pro zámek, který bys lidem jak milé dal k svátku,
ale mužovo srdce jsou ruce a mozoly,
které se krví svou do cihel probolí,
aby tu stála alespoň skutečná hospoda u silnice
pro ušlé poutníky a pro poutnice.

Dnes je má těžká hodina.
Chlapecké srdce mi zemřelo a sám v rakvi je vynáším
a zemřelým trpě, trpím i tím,
které mi v prsu se roditi počíná.
Dnes je má těžká hodina;
jedno srdce jsem pohřbil a druhé ještě nemám,
sesláblý úzkostí, sesláblý samotou
marně se bráním studeným stěnám
pokoje svého
uštěpačného.
<pageNum>7</pageNum>

Milenčin dopise, lampo, kniho kamarádova,
věci zrozené z lásky, světla a víry
dnes při mně stůjte a třikrát mi věrnější buďte,
když zůstal jsem na světě sirý
a modlete se,
aby mi narostlo srdce statečné a nesmlouvavé
a věřte dnes za mě, že tomu tak bude
a věřte dnes za mě, že postavím
dle obrazu jeho
život člověka spravedlivého.

Já mužné srdce ještě nemám,
sám v těžké své hodině;
a proto nevěřím."""


        ]


poems = [
        """Windows

        A window is a glass ship,
        chained to the shores of my living room.
        A young sailor doesn't need seven-mile boots.
        He gets in and leaves;
        Any moment now
        he'll travel ten thousand miles with eager eyes
        over the sea
        ...for a sky fair and wide.

        White clouds,
        white rocks,
        Africa and Australia we have travelled,
        ...and fraternized with the blacks,
        We visited the Indians.
        We found new continents,
        ...the youngest of all the continents,
        but it's not enough,
        to stop us.

        The world is round.
        After many adventures, you'll be glad to come back 
        to the low world that closes
        over old familiar things.
        At a rickety table between two drying calamari
        ...you'll find the best use for a story with an aurora borealis.
        All will be quiet and happy - yourself most of all.
        Thou shalt lay thine eyes in the middle of the room: 
        a gift from the road -
        - a world album.
        """,
        """Humility

        I shall become smaller and smaller still,
        when I'm the smallest in the world.

        In the morning, in the meadow, in the summer
        ...I'll be the smallest flower.
        I will whisper as I embrace him:
        "Barefoot boy,
        "Heaven has put his hand on you
        ...with a drop of dew,
        ...it did not fall."
        """,

        """HARD HOUR

        I came into the world,
        to build my life
        in the image of my heart.

        A boy's heart is a song at the beginning,
        A plan for the castle you'd give to people as a lovely feast,
        But a man's heart is hands and calluses,
        that will be pierced with their blood into the bricks,
        so that at least there's a real tavern by the roadside
        ...for lost pilgrims and pilgrim women.

        Today is my hard hour.
        My boy's heart is dead, and I carry it out in a coffin alone.
        and to the dead I suffer,
        ...that is conceived in my breast.
        Today is my hour of trouble;
        I have buried one heart, and have not yet the other,
        ...broken by anguish, broken by loneliness...
        I struggle in vain against the cold walls.
        of my room
        ...of my abject room.
        <pageNum>7</pageNum>

        "Mistress's letter, lampoon, friend's book,
        things born of love, light and faith
        stand by me today and be thrice more faithful to me,
        when I am left in the world gray
        and pray,
        ...that I may grow a heart brave and uncomplaining...
        and believe for me this day that it shall be so.
        And believe for me this day that I will build
        in his image
        the life of a righteous man.

        I have not yet a manly heart,
        alone in my hour of need;
        and therefore I do not believe."
        """]


# zpracuj feedback

form = cgi.FieldStorage()
index = int(form.getvalue("index", 0))
text = form.getvalue("text", None)
prompt = form.getvalue("prompt", None)

if prompt and not text:
    text = prompt

if text:
    seed = random.randint(0, 10000000)
    # TODO translate text to English
    # but probably will use DALLE anyway which can take Czech as well
    # TODO take into account whole text, not only title
    prompt = "An abstract dreamy image, relating to the topic of " + titles[index]
    image_filename = get_image_for_line(prompt, seed)


if text and image_filename:
    
    print(f"""
    <h2>{nazvy[index]}: {text}</h2>
    <p>Zde je obrázek zobrazující tvé pocity ve vztahu k této básni.</p>
    <img src="genimgs/{image_filename}.png">
    <br>
    <input disabled type="submit" value="Sdílet">
    <hr>
    """)


index = random.randint(0, 2)

options = [
    "je to hrozně smutný",
    "láska je zlá",
    "cítím to stejně",
    "to mě potěšilo",
    "tomu nerozumím",
    ]

basen_text = basne[index].replace('\n', '<br>')

print(f"""
        <h2>{nazvy[index]}</h2>
        <p>Zde máš jednu náhodně vybranou Wolkerovu báseň. Jaké pocity v tobě
        vyvolává?</p>
        <p>(Zatim to náhodně vybírá jen ze 3 básní.)</p>
        <p>{basen_text}</p>
        <form method="post">
            <input name="index" type="hidden" value="{index}">
            {' '.join([ f'<input type="submit" name="text" value="{opt}"><br>' for opt in options])}
            <input name="prompt"> <input type="submit" value="Poslat">
        </form>
        <br>
        <form method="post">
            <input type="submit" value="Vyber mi náhodně jinou báseň">
        </form>
        </body>
        </html>
        """)


