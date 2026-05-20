# EduPo JSON Format Documentation

This document describes the structure of JSON data returned from the EduPo API.

## Format Description

The description should more or less reflect the state as of 17.3.2025.
TODO: The structure of syllables is missing; for now, see format examples below...

### Root Elements

- **author** *(string)* – Name of the poem's author (real name of the person).
- **author_name** *(string)* – Name of the author as listed in the collection (may be a pseudonym).
- **b_title** *(string)* – Title of the collection in which the poem was published.
- **book_id** *(integer)* – Unique ID of the collection.
- **born** *(integer, nullable)* – Year of birth of the author.
- **dedication** *(string, nullable)* – Dedication of the poem.
- **died** *(integer, nullable)* – Year of death of the author.
- **duplicate** *(integer)* – The poem is a duplicate of the poem with this ID.
- **edition** *(integer)* – Edition number of the book.
- **id** *(integer)* – Unique ID of the poem (**poemid**).
- **identity** *(string)* – Author's identifier.
- **imgfile** *(string, nullable)* – Path to the file with the generated image.
- **imgtitle** *(string, nullable)* – Description of the image generated for the poem.
- **motives** *(string, nullable)* – List of poem motifs (automatically determined).
- **motto** *(string, nullable)* – Motto of the poem.
- **motto_aut** *(string, nullable)* – Author of the motto.
- **openai** *(array, nullable)* – List of generated responses from the OpenAI model.
  - **prompt** *(string)* – Query posed to the model.
  - **output** *(string)* – Output response.
- **pages** *(integer, nullable)* – Number of pages in the book.
- **place** *(string, nullable)* – Place of publication.
- **plaintext** *(string)* – Poem text in plain text format.
- **poem_id_corp** *(string)* – Poem ID in the corpus.
- **present_metres** *(array, nullable)* – List of metric schemes in the poem.
- **publisher** *(string, nullable)* – Publisher of the book.
- **schemes** *(object)* – Information about rhyme schemes and poem form.
  - **form** *(string, nullable)* – Form of the poem (e.g., sonnet).
  - **rhyme_scheme** *(array)* – List of rhyme schemes (TODO: likely empty).
  - **rhymed** *(boolean)* – Indicator whether the poem contains rhyme.
  - **stanza_scheme** *(array)* – List of stanza schemes (verse lengths in stanzas).
  - **stanzaic** *(boolean)* – Indicator whether the poem contains regular stanzas.
- **schools** *(array, nullable)* – List of literary schools.
- **signature** *(string, nullable)* – Signature of the book.
- **subtitle** *(string, nullable)* – Subtitle of the poem.
- **title** *(string)* – Title of the poem.
- **translations** *(object, nullable)* – Translations of the poem into other languages.
  - **sk** *(string, nullable)* – Translation into Slovak.
  - ...
- **ttsfile** *(string, nullable)* – Path to the file with the generated TTS recitation.
- **wiki** *(string, nullable)* – ID of the author's article on Wikidata.
- **year** *(integer, nullable)* – Year of publication of the poem.
- **zena** *(boolean, nullable)* – Indicator whether the author is a woman.

### Structure of **body** (poem content, array of verses)

Each object in the `body` array contains information about one verse:

- **metre** *(object)* – Information about the verse's meter.
  - This format is inconvenient; in **verses**, it is better structured (see below).
  - **J** *(object, nullable)* – Information about iambic meter.
    - **basic** *(string)* – TODO: Not sure what this means.
    - **clause** *(string)* – Type of meter (m/f/a, etc.).
    - **foot** *(integer)* – Number of feet.
    - **pattern** *(string)* – Strong and weak positions in the meter (S/W/V).
- **punct** *(object, nullable)* – Mapping of position and punctuation.
- **rhyme** *(integer, nullable)* – Rhyme (1, 2, 3... a verse with rhyme=3 rhymes with other verses with rhyme=3; rhyme=0 means unrhymed).
- **sections** *(string, nullable)* – Syllable accents in the verse (rhythm).
- **stanza** *(integer)* – Stanza number (starting from 0).
- **text** *(string)* – Text of the verse.
- **words** *(array)* – Array containing detailed information about words.
  - **cft** *(string)* – Phonological transcription.
  - **lemma** *(string)* – Lemma of the word.
  - **morph** *(string)* – Morphological tag.
  - **phoebe** *(string)* – Phonetic representation.
  - **syllables** *(array, nullable)* – List of syllables. **TODO**: Provide a detailed description.
  - **token** *(string)* – Original token.
  - **token_lc** *(string)* – Token in lowercase.
  - **xsampa** *(string)* – X-SAMPA transcription.

### Structure of **verses** (poem content)

This is essentially the same as `body`, but slightly restructured...
Some important differences:

The meter is in a more reasonable format. Directly at the root of the verse, there are items:
- **metre** is a string (e.g., "J").
- **metrum** is the textual name of the meter (e.g., "iamb").
- **clause**
- **foot**
- **pattern**

Additionally:
- **narrators_gender** – Gender of the lyrical speaker (M/F).
- **rhymeclass**
- **rhymeletter** – A, B, C... rhyme as a letter, verse C rhymes with other verses C...
- **rhymesubscript** – If the alphabet runs out, it starts again from A, and this field adds subscript 1, 2, etc.


## Example (shorened `body` and `verses`)

```
{
  "author": "Černý, Boleslav L.",
  "author_name": "Černý, Boleslav L.",
  "b_title": "Večerní stíny",
  "book_id": 1409,
  "born": 1881,
  "dedication": null,
  "died": 1930,
  "duplicate": null,
  "edition": 1,
  "id": 69947,
  "identity": "Černý, Boleslav L.",
  "imgfile": "static/genimg/69947.png",
  "imgtitle": "Generate an image titled 'Fear', illustrating the ambiance of a silent evening when chill and mystery seep into the room. Depict a figure walking alongside the wall, submerged in icy shadows and thick fogs beyond the windows, expressing feelings of solitude and tension.\n",
  "motives": "1. Osamělost\n2. Strach a úzkost\n3. Tma a chlad\n4. Vzpomínky a nostalgie\n5. Přítomnost neznámého\n",
  "motto": null,
  "motto_aut": null,
  "openai": [
    {
      "output": "Báseň \"Strach\" od Boleslava L. Černého je spíše smutná. Vyjadřuje pocity osamělosti, úzkosti a melancholie. Atmosféra je temná a chmurná, s popisem mrazivých stínů a mlhy, které vytvářejí pocit neklidu a strachu. Opakující se motiv smutného pohledu a osamělosti posiluje celkový dojem smutku a beznaděje.",
      "prompt": "Je báseň veselá nebo smutná?"
    }
  ],
  "pages": 48,
  "place": "Praha",
  "plaintext": "Po tichu, neslyšen se v moji jizbu vkrad’...\n\nByl večer již – šel zvolna podél stěny\n\na za ním – příští noci teskný chlad\n\na čísi pohled smutně vytřeštěný....!\n\n\nA stíny mrazivé u dvéří zřely,\n\npřed okny mlhy zhoustly v závoj stmělý.\n\n\nA já byl sám!... On kráčel podél stěny\n\na za ním – pohled smutně vytřeštěný...!\n",
  "poem_id_corp": "0001-0000-0000-0012-0000",
  "present_metres": [
    "J"
  ],
  "publisher": "Pospíšil, Jaroslav; Rokyta, Jan",
  "schemes": {
    "form": null,
    "rhyme_scheme": [],
    "rhymed": true,
    "stanza_scheme": [
      "abcb",
      "aa",
      "aa"
    ],
    "stanzaic": false
  },
  "schools": [],
  "signature": "Knihovna Národního muzea, Praha; 95 III 157 (Drobné tisky)",
  "subtitle": null,
  "title": "Strach.",
  "translations": {
    "sk": "Po ticho, nepočutý sa v moju izbu vkradnúc&#8217;... \n Bol večer už &#8211; šiel zvoľna podél steny \n a za ním &#8211; budúcu noci clivý chlad \n a čísi pohľad smutně vytreštený....! \n A tiene mrazivé u dverí zreli, \n pred oknami hmly zhustli v závoj stmělý.  \n A ja bol sám!... On kráčal podél steny \n a za ním &#8211; pohľad smutně vytreštený...!"
  },
  "ttsfile": "static/gentts/69947.mp3",
  "wiki": "Q95174643",
  "year": 1907,
  "zena": null
  "body": [
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "m",
          "foot": "6",
          "pattern": "WSWSWSWSWSWS"
        }
      },
      "punct": {
        "2": ",",
        "8": "..."
      },
      "rhyme": 1,
      "sections": "R10100m1010m",
      "stanza": 0,
      "text": "Po tichu, neslyšen se v moji jizbu vkrad’...",
      "words": [
        {
          "cft": "po",
          "lemma": "po",
          "morph": "RR--6-----------",
          "phoebe": "po",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "P",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "p",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "W",
              "stress": "1"
            }
          ],
          "token": "Po",
          "token_lc": "po",
          "xsampa": "po"
        },
        {
          "cft": "ťixu",
          "lemma": "ticho",
          "morph": "NNNS6-----A-----",
          "phoebe": "Tixu",
          "punct": ",",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "t",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "ť",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "S",
              "stress": "0"
            },
            {
              "length": 0,
              "ort_consonants": "ch",
              "ort_end_consonants": "",
              "ort_vowels": "u",
              "ph_consonants": "x",
              "ph_end_consonants": "",
              "ph_vowels": "u",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "tichu",
          "token_lc": "tichu",
          "xsampa": "cIxu"
        },
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "3": "–"
      },
      "rhyme": 2,
      "sections": "m10m1101010",
      "stanza": 0,
      "text": "Byl večer již – šel zvolna podél stěny",
      "words": [
        {
          "cft": "bil",
          "lemma": "být",
          "morph": "VpIS---3R-AA---I",
          "phoebe": "bil",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "B",
              "ort_end_consonants": "l",
              "ort_vowels": "y",
              "ph_consonants": "b",
              "ph_end_consonants": "l",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "Byl",
          "token_lc": "byl",
          "xsampa": "bIl"
        },
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "6": ","
      },
      "rhyme": 3,
      "sections": "m10100R1010",
      "stanza": 1,
      "text": "A stíny mrazivé u dvéří zřely,",
      "words": [
        {
          "cft": "a",
          "lemma": "a",
          "morph": "J^--------------",
          "phoebe": "a",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "A",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "A",
          "token_lc": "a",
          "xsampa": "a"
        },
        {
          "cft": "sťíni",
          "lemma": "stín",
          "morph": "NNIP1-----A-----",
          "phoebe": "sTIni",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "st",
              "ort_end_consonants": "",
              "ort_vowels": "í",
              "ph_consonants": "sť",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "stíny",
          "token_lc": "stíny",
          "xsampa": "sci:nI"
        },
      ]
    }
  ],
  "verses": [
    {
      "clause": "m",
      "foot": "6",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSWS",
      "rhymeclass": 1,
      "rhymeletter": "A",
      "rhymesubscript": "",
      "rythm": "R10100m1010m",
      "stanza": 0,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "P"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "W",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "t"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": ", ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "ch"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "u"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "e"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "sl"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "š"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "n"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "s"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v m"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "j"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "j"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "i"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "zb"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "u"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "... ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "vkr"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0",
                "rhyming"
              ],
              "text": "a"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress0",
                "rhyming"
              ],
              "text": "d"
            }
          ],
          "position": "S",
          "stress": "0"
        }
      ],
      "text": "Po tichu, neslyšen se v moji jizbu vkrad’..."
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 2,
      "rhymeletter": "B",
      "rhymesubscript": "",
      "rythm": "m10m1101010",
      "stanza": 0,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "B"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "0"
        },
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 3,
      "rhymeletter": "C",
      "rhymesubscript": "",
      "rythm": "m10100R1010",
      "stanza": 1,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "A"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "st"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "í"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "mr"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "a"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "z"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "é"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress1"
              ],
              "text": "u"
            }
          ],
          "position": "W",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "dv"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "é"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "ř"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "í"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "zř"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1",
                "rhyming"
              ],
              "text": "e"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": ", ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1",
                "rhyming"
              ],
              "text": "l"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "A stíny mrazivé u dvéří zřely,"
    },
  ],
}
```

## Example

```
{
  "author": "Černý, Boleslav L.",
  "author_name": "Černý, Boleslav L.",
  "b_title": "Večerní stíny",
  "book_id": 1409,
  "born": 1881,
  "dedication": null,
  "died": 1930,
  "duplicate": null,
  "edition": 1,
  "id": 69947,
  "identity": "Černý, Boleslav L.",
  "imgfile": "static/genimg/69947.png",
  "imgtitle": "Generate an image titled 'Fear', illustrating the ambiance of a silent evening when chill and mystery seep into the room. Depict a figure walking alongside the wall, submerged in icy shadows and thick fogs beyond the windows, expressing feelings of solitude and tension.\n",
  "motives": "1. Osamělost\n2. Strach a úzkost\n3. Tma a chlad\n4. Vzpomínky a nostalgie\n5. Přítomnost neznámého\n",
  "motto": null,
  "motto_aut": null,
  "openai": [
    {
      "output": "Báseň \"Strach\" od Boleslava L. Černého je spíše smutná. Vyjadřuje pocity osamělosti, úzkosti a melancholie. Atmosféra je temná a chmurná, s popisem mrazivých stínů a mlhy, které vytvářejí pocit neklidu a strachu. Opakující se motiv smutného pohledu a osamělosti posiluje celkový dojem smutku a beznaděje.",
      "prompt": "Je báseň veselá nebo smutná?"
    }
  ],
  "pages": 48,
  "place": "Praha",
  "plaintext": "Po tichu, neslyšen se v moji jizbu vkrad’...\n\nByl večer již – šel zvolna podél stěny\n\na za ním – příští noci teskný chlad\n\na čísi pohled smutně vytřeštěný....!\n\n\nA stíny mrazivé u dvéří zřely,\n\npřed okny mlhy zhoustly v závoj stmělý.\n\n\nA já byl sám!... On kráčel podél stěny\n\na za ním – pohled smutně vytřeštěný...!\n",
  "poem_id_corp": "0001-0000-0000-0012-0000",
  "present_metres": [
    "J"
  ],
  "publisher": "Pospíšil, Jaroslav; Rokyta, Jan",
  "schemes": {
    "form": null,
    "rhyme_scheme": [],
    "rhymed": true,
    "stanza_scheme": [
      "abcb",
      "aa",
      "aa"
    ],
    "stanzaic": false
  },
  "schools": [],
  "signature": "Knihovna Národního muzea, Praha; 95 III 157 (Drobné tisky)",
  "subtitle": null,
  "title": "Strach.",
  "translations": {
    "sk": "Po ticho, nepočutý sa v moju izbu vkradnúc&#8217;... \n Bol večer už &#8211; šiel zvoľna podél steny \n a za ním &#8211; budúcu noci clivý chlad \n a čísi pohľad smutně vytreštený....! \n A tiene mrazivé u dverí zreli, \n pred oknami hmly zhustli v závoj stmělý.  \n A ja bol sám!... On kráčal podél steny \n a za ním &#8211; pohľad smutně vytreštený...!"
  },
  "ttsfile": "static/gentts/69947.mp3",
  "wiki": "Q95174643",
  "year": 1907,
  "zena": null
  "body": [
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "m",
          "foot": "6",
          "pattern": "WSWSWSWSWSWS"
        }
      },
      "punct": {
        "2": ",",
        "8": "..."
      },
      "rhyme": 1,
      "sections": "R10100m1010m",
      "stanza": 0,
      "text": "Po tichu, neslyšen se v moji jizbu vkrad’...",
      "words": [
        {
          "cft": "po",
          "lemma": "po",
          "morph": "RR--6-----------",
          "phoebe": "po",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "P",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "p",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "W",
              "stress": "1"
            }
          ],
          "token": "Po",
          "token_lc": "po",
          "xsampa": "po"
        },
        {
          "cft": "ťixu",
          "lemma": "ticho",
          "morph": "NNNS6-----A-----",
          "phoebe": "Tixu",
          "punct": ",",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "t",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "ť",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "S",
              "stress": "0"
            },
            {
              "length": 0,
              "ort_consonants": "ch",
              "ort_end_consonants": "",
              "ort_vowels": "u",
              "ph_consonants": "x",
              "ph_end_consonants": "",
              "ph_vowels": "u",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "tichu",
          "token_lc": "tichu",
          "xsampa": "cIxu"
        },
        {
          "cft": "neslišen",
          "lemma": "slyšet",
          "morph": "VsIS---3R-NP---I",
          "phoebe": "nesliSen",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "sl",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "sl",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            },
            {
              "length": 0,
              "ort_consonants": "š",
              "ort_end_consonants": "n",
              "ort_vowels": "e",
              "ph_consonants": "š",
              "ph_end_consonants": "n",
              "ph_vowels": "e",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "neslyšen",
          "token_lc": "neslyšen",
          "xsampa": "nEslISEn"
        },
        {
          "cft": "se",
          "lemma": "se",
          "morph": "P7-X4-----------",
          "phoebe": "se",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "s",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "s",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "se",
          "token_lc": "se",
          "xsampa": "sE"
        },
        {
          "cft": "v",
          "lemma": "v",
          "morph": "RR--4-----------",
          "phoebe": "v",
          "syllables": [],
          "token": "v",
          "token_lc": "v",
          "xsampa": "v"
        },
        {
          "cft": "moji",
          "lemma": "můj",
          "morph": "PSFS4-S1--------",
          "phoebe": "moji",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "v_m",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "v_m",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "j",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "j",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "moji",
          "token_lc": "moji",
          "xsampa": "mojI"
        },
        {
          "cft": "jizbu",
          "lemma": "jizba",
          "morph": "NNFS4-----A-----",
          "phoebe": "jizbu",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "j",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "j",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "zb",
              "ort_end_consonants": "",
              "ort_vowels": "u",
              "ph_consonants": "zb",
              "ph_end_consonants": "",
              "ph_vowels": "u",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "jizbu",
          "token_lc": "jizbu",
          "xsampa": "jIzbu"
        },
        {
          "cft": "fkrat",
          "lemma": "vkrad´",
          "morph": "X24-------------",
          "phoebe": "fkrat",
          "punct": "...",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "vkr",
              "ort_end_consonants": "d",
              "ort_vowels": "a",
              "ph_consonants": "fkr",
              "ph_end_consonants": "t",
              "ph_vowels": "a",
              "position": "S",
              "rhyme_from": "v",
              "stress": "0"
            }
          ],
          "token": "vkrad",
          "token_lc": "vkrad",
          "xsampa": "fkrat"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "3": "–"
      },
      "rhyme": 2,
      "sections": "m10m1101010",
      "stanza": 0,
      "text": "Byl večer již – šel zvolna podél stěny",
      "words": [
        {
          "cft": "bil",
          "lemma": "být",
          "morph": "VpIS---3R-AA---I",
          "phoebe": "bil",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "B",
              "ort_end_consonants": "l",
              "ort_vowels": "y",
              "ph_consonants": "b",
              "ph_end_consonants": "l",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "Byl",
          "token_lc": "byl",
          "xsampa": "bIl"
        },
        {
          "cft": "veZer",
          "lemma": "večer",
          "morph": "NNIS1-----A-----",
          "phoebe": "veCer",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "v",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "v",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "č",
              "ort_end_consonants": "r",
              "ort_vowels": "e",
              "ph_consonants": "Z",
              "ph_end_consonants": "r",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "večer",
          "token_lc": "večer",
          "xsampa": "vEt_SEr"
        },
        {
          "cft": "jiš",
          "lemma": "již",
          "morph": "Db--------------",
          "phoebe": "jiS",
          "punct": "–",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "j",
              "ort_end_consonants": "ž",
              "ort_vowels": "i",
              "ph_consonants": "j",
              "ph_end_consonants": "š",
              "ph_vowels": "i",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "již",
          "token_lc": "již",
          "xsampa": "jIS"
        },
        {
          "cft": "šel",
          "lemma": "jít",
          "morph": "VpMS---3R-AA---I",
          "phoebe": "Sel",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "š",
              "ort_end_consonants": "l",
              "ort_vowels": "e",
              "ph_consonants": "š",
              "ph_end_consonants": "l",
              "ph_vowels": "e",
              "position": "W",
              "stress": "1"
            }
          ],
          "token": "šel",
          "token_lc": "šel",
          "xsampa": "SEl"
        },
        {
          "cft": "zvolna",
          "lemma": "zvolna",
          "morph": "Db--------------",
          "phoebe": "zvolna",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "zv",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "zv",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "ln",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "ln",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "zvolna",
          "token_lc": "zvolna",
          "xsampa": "zvolna"
        },
        {
          "cft": "podél",
          "lemma": "podél",
          "morph": "RR--2-----------",
          "phoebe": "podEl",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "p",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "p",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 1,
              "ort_consonants": "d",
              "ort_end_consonants": "l",
              "ort_vowels": "é",
              "ph_consonants": "d",
              "ph_end_consonants": "l",
              "ph_vowels": "é",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "podél",
          "token_lc": "podél",
          "xsampa": "podE:l"
        },
        {
          "cft": "sťeni",
          "lemma": "stěna",
          "morph": "NNFS2-----A-----",
          "phoebe": "sTeni",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "st",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "sť",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "rhyme_from": "v",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "rhyme_from": "c",
              "stress": "0"
            }
          ],
          "token": "stěny",
          "token_lc": "stěny",
          "xsampa": "scEnI"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "m",
          "foot": "5",
          "pattern": "WSWSWSWSWS"
        }
      },
      "punct": {
        "3": "–"
      },
      "rhyme": 1,
      "sections": "mRm1010101",
      "stanza": 0,
      "text": "a za ním – příští noci teskný chlad",
      "words": [
        {
          "cft": "a",
          "lemma": "a",
          "morph": "J^--------------",
          "phoebe": "a",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "a",
          "token_lc": "a",
          "xsampa": "a"
        },
        {
          "cft": "za",
          "lemma": "za",
          "morph": "RR--7-----------",
          "phoebe": "za",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "z",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "z",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "za",
          "token_lc": "za",
          "xsampa": "za"
        },
        {
          "cft": "ňím",
          "lemma": "on",
          "morph": "P5IS7--3--------",
          "phoebe": "NIm",
          "punct": "–",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "n",
              "ort_end_consonants": "m",
              "ort_vowels": "í",
              "ph_consonants": "ň",
              "ph_end_consonants": "m",
              "ph_vowels": "í",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "ním",
          "token_lc": "ním",
          "xsampa": "Ji:m"
        },
        {
          "cft": "příšťí",
          "lemma": "příští",
          "morph": "AAFP1----1A-----",
          "phoebe": "pRISTI",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "př",
              "ort_end_consonants": "",
              "ort_vowels": "í",
              "ph_consonants": "př",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 1,
              "ort_consonants": "št",
              "ort_end_consonants": "",
              "ort_vowels": "í",
              "ph_consonants": "šť",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "příští",
          "token_lc": "příští",
          "xsampa": "pP\\i:Sci:"
        },
        {
          "cft": "noci",
          "lemma": "noc",
          "morph": "NNFP1-----A-----",
          "phoebe": "noci",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "c",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "c",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "noci",
          "token_lc": "noci",
          "xsampa": "not_sI"
        },
        {
          "cft": "teskní",
          "lemma": "teskný",
          "morph": "AAIS4----1A-----",
          "phoebe": "tesknI",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "t",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "t",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 1,
              "ort_consonants": "skn",
              "ort_end_consonants": "",
              "ort_vowels": "ý",
              "ph_consonants": "skn",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "teskný",
          "token_lc": "teskný",
          "xsampa": "tEskni:"
        },
        {
          "cft": "xlat",
          "lemma": "chlad",
          "morph": "NNIS4-----A-----",
          "phoebe": "xlat",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "chl",
              "ort_end_consonants": "d",
              "ort_vowels": "a",
              "ph_consonants": "xl",
              "ph_end_consonants": "t",
              "ph_vowels": "a",
              "position": "S",
              "rhyme_from": "v",
              "stress": "1"
            }
          ],
          "token": "chlad",
          "token_lc": "chlad",
          "xsampa": "xlat"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "5": "....!"
      },
      "rhyme": 2,
      "sections": "m1010101000",
      "stanza": 0,
      "text": "a čísi pohled smutně vytřeštěný....!",
      "words": [
        {
          "cft": "a",
          "lemma": "a",
          "morph": "J^--------------",
          "phoebe": "a",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "a",
          "token_lc": "a",
          "xsampa": "a"
        },
        {
          "cft": "Zísi",
          "lemma": "čísi",
          "morph": "PZIS1-----------",
          "phoebe": "CIsi",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "č",
              "ort_end_consonants": "",
              "ort_vowels": "í",
              "ph_consonants": "Z",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "s",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "s",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "čísi",
          "token_lc": "čísi",
          "xsampa": "t_Si:sI"
        },
        {
          "cft": "pohlet",
          "lemma": "pohled",
          "morph": "NNIS1-----A-----",
          "phoebe": "pohlet",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "p",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "p",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "hl",
              "ort_end_consonants": "d",
              "ort_vowels": "e",
              "ph_consonants": "hl",
              "ph_end_consonants": "t",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "pohled",
          "token_lc": "pohled",
          "xsampa": "poh\\lEt"
        },
        {
          "cft": "smutňe",
          "lemma": "smutně",
          "morph": "Dg-------1A-----",
          "phoebe": "smutNe",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "sm",
              "ort_end_consonants": "",
              "ort_vowels": "u",
              "ph_consonants": "sm",
              "ph_end_consonants": "",
              "ph_vowels": "u",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "tn",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "tň",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "smutně",
          "token_lc": "smutně",
          "xsampa": "smutJE"
        },
        {
          "cft": "vitřešťení",
          "lemma": "vytřeštěný",
          "morph": "AAIS1----1A-----",
          "phoebe": "vitReSTenI",
          "punct": "....!",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "v",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "v",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "tř",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "tř",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            },
            {
              "length": 0,
              "ort_consonants": "št",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "šť",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "rhyme_from": "v",
              "stress": "0"
            },
            {
              "length": 1,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "ý",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "W",
              "rhyme_from": "c",
              "stress": "0"
            }
          ],
          "token": "vytřeštěný",
          "token_lc": "vytřeštěný",
          "xsampa": "vItP\\EScEni:"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "6": ","
      },
      "rhyme": 3,
      "sections": "m10100R1010",
      "stanza": 1,
      "text": "A stíny mrazivé u dvéří zřely,",
      "words": [
        {
          "cft": "a",
          "lemma": "a",
          "morph": "J^--------------",
          "phoebe": "a",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "A",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "A",
          "token_lc": "a",
          "xsampa": "a"
        },
        {
          "cft": "sťíni",
          "lemma": "stín",
          "morph": "NNIP1-----A-----",
          "phoebe": "sTIni",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "st",
              "ort_end_consonants": "",
              "ort_vowels": "í",
              "ph_consonants": "sť",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "stíny",
          "token_lc": "stíny",
          "xsampa": "sci:nI"
        },
        {
          "cft": "mrazivé",
          "lemma": "mrazivý",
          "morph": "AAIP1----1A-----",
          "phoebe": "mrazivE",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "mr",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "mr",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "z",
              "ort_end_consonants": "",
              "ort_vowels": "i",
              "ph_consonants": "z",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            },
            {
              "length": 1,
              "ort_consonants": "v",
              "ort_end_consonants": "",
              "ort_vowels": "é",
              "ph_consonants": "v",
              "ph_end_consonants": "",
              "ph_vowels": "é",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "mrazivé",
          "token_lc": "mrazivé",
          "xsampa": "mrazIvE:"
        },
        {
          "cft": "u",
          "lemma": "u",
          "morph": "RR--2-----------",
          "phoebe": "u",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "u",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "u",
              "position": "W",
              "stress": "1"
            }
          ],
          "token": "u",
          "token_lc": "u",
          "xsampa": "u"
        },
        {
          "cft": "dvéří",
          "lemma": "dveře",
          "morph": "NNFP2-----A-----",
          "phoebe": "dvERI",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "dv",
              "ort_end_consonants": "",
              "ort_vowels": "é",
              "ph_consonants": "dv",
              "ph_end_consonants": "",
              "ph_vowels": "é",
              "position": "S",
              "stress": "0"
            },
            {
              "length": 1,
              "ort_consonants": "ř",
              "ort_end_consonants": "",
              "ort_vowels": "í",
              "ph_consonants": "ř",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "dvéří",
          "token_lc": "dvéří",
          "xsampa": "dvE:P\\i:"
        },
        {
          "cft": "zřeli",
          "lemma": "zřít",
          "morph": "VpFP---3R-AA---I",
          "phoebe": "zReli",
          "punct": ",",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "zř",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "zř",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "rhyme_from": "v",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "l",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "l",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "rhyme_from": "c",
              "stress": "0"
            }
          ],
          "token": "zřely",
          "token_lc": "zřely",
          "xsampa": "zP\\ElI"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "7": "."
      },
      "rhyme": 3,
      "sections": "R1010101010",
      "stanza": 1,
      "text": "před okny mlhy zhoustly v závoj stmělý.",
      "words": [
        {
          "cft": "přet",
          "lemma": "před",
          "morph": "RR--7-----------",
          "phoebe": "pRet",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "př",
              "ort_end_consonants": "d",
              "ort_vowels": "e",
              "ph_consonants": "př",
              "ph_end_consonants": "t",
              "ph_vowels": "e",
              "position": "W",
              "stress": "1"
            }
          ],
          "token": "před",
          "token_lc": "před",
          "xsampa": "pP\\Et"
        },
        {
          "cft": "okni",
          "lemma": "okno",
          "morph": "NNNP7-----A-----",
          "phoebe": "okni",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "0"
            },
            {
              "length": 0,
              "ort_consonants": "kn",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "kn",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "okny",
          "token_lc": "okny",
          "xsampa": "oknI"
        },
        {
          "cft": "mLhi",
          "lemma": "mlha",
          "morph": "NNFS2-----A-----",
          "phoebe": "mLhi",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "m",
              "ort_end_consonants": "",
              "ort_vowels": "l",
              "ph_consonants": "m",
              "ph_end_consonants": "",
              "ph_vowels": "L",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "h",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "h",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "mlhy",
          "token_lc": "mlhy",
          "xsampa": "ml=h\\I"
        },
        {
          "cft": "sxOstli",
          "lemma": "zhoustnout",
          "morph": "VpIP---3R-AA--1P",
          "phoebe": "sx0stli",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "zh",
              "ort_end_consonants": "",
              "ort_vowels": "ou",
              "ph_consonants": "sx",
              "ph_end_consonants": "",
              "ph_vowels": "O",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "stl",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "stl",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "zhoustly",
          "token_lc": "zhoustly",
          "xsampa": "sxo_ustlI"
        },
        {
          "cft": "v",
          "lemma": "v",
          "morph": "RR--4-----------",
          "phoebe": "v",
          "syllables": [],
          "token": "v",
          "token_lc": "v",
          "xsampa": "v"
        },
        {
          "cft": "závoj",
          "lemma": "závoj",
          "morph": "NNIS4-----A-----",
          "phoebe": "zAvoj",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "v_z",
              "ort_end_consonants": "",
              "ort_vowels": "á",
              "ph_consonants": "v_z",
              "ph_end_consonants": "",
              "ph_vowels": "á",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "v",
              "ort_end_consonants": "j",
              "ort_vowels": "o",
              "ph_consonants": "v",
              "ph_end_consonants": "j",
              "ph_vowels": "o",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "závoj",
          "token_lc": "závoj",
          "xsampa": "za:voj"
        },
        {
          "cft": "stmňelí",
          "lemma": "stmělý",
          "morph": "X24-------------",
          "phoebe": "stmNelI",
          "punct": ".",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "stm",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "stmň",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "rhyme_from": "v",
              "stress": "1"
            },
            {
              "length": 1,
              "ort_consonants": "l",
              "ort_end_consonants": "",
              "ort_vowels": "ý",
              "ph_consonants": "l",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "W",
              "rhyme_from": "c",
              "stress": "0"
            }
          ],
          "token": "stmělý",
          "token_lc": "stmělý",
          "xsampa": "stmJEli:"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "4": "!..."
      },
      "rhyme": 2,
      "sections": "cmmmm101010",
      "stanza": 2,
      "text": "A já byl sám!... On kráčel podél stěny",
      "words": [
        {
          "cft": "a",
          "lemma": "a",
          "morph": "J^--------------",
          "phoebe": "a",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "A",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "c"
            }
          ],
          "token": "A",
          "token_lc": "a",
          "xsampa": "a"
        },
        {
          "cft": "já",
          "lemma": "já",
          "morph": "PP-S1--1--------",
          "phoebe": "jA",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "j",
              "ort_end_consonants": "",
              "ort_vowels": "á",
              "ph_consonants": "j",
              "ph_end_consonants": "",
              "ph_vowels": "á",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "já",
          "token_lc": "já",
          "xsampa": "ja:"
        },
        {
          "cft": "bil",
          "lemma": "být",
          "morph": "VpMS---3R-AA---I",
          "phoebe": "bil",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "b",
              "ort_end_consonants": "l",
              "ort_vowels": "y",
              "ph_consonants": "b",
              "ph_end_consonants": "l",
              "ph_vowels": "i",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "byl",
          "token_lc": "byl",
          "xsampa": "bIl"
        },
        {
          "cft": "sám",
          "lemma": "sám",
          "morph": "PLMS1-----------",
          "phoebe": "sAm",
          "punct": "!...",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "s",
              "ort_end_consonants": "m",
              "ort_vowels": "á",
              "ph_consonants": "s",
              "ph_end_consonants": "m",
              "ph_vowels": "á",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "sám",
          "token_lc": "sám",
          "xsampa": "sa:m"
        },
        {
          "cft": "on",
          "lemma": "on",
          "morph": "PPMS1--3--------",
          "phoebe": "on",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "n",
              "ort_vowels": "O",
              "ph_consonants": "",
              "ph_end_consonants": "n",
              "ph_vowels": "o",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "On",
          "token_lc": "on",
          "xsampa": "on"
        },
        {
          "cft": "kráZel",
          "lemma": "kráčet",
          "morph": "VpMS---3R-AA---I",
          "phoebe": "krACel",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "kr",
              "ort_end_consonants": "",
              "ort_vowels": "á",
              "ph_consonants": "kr",
              "ph_end_consonants": "",
              "ph_vowels": "á",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "č",
              "ort_end_consonants": "l",
              "ort_vowels": "e",
              "ph_consonants": "Z",
              "ph_end_consonants": "l",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "kráčel",
          "token_lc": "kráčel",
          "xsampa": "kra:t_SEl"
        },
        {
          "cft": "podél",
          "lemma": "podél",
          "morph": "RR--2-----------",
          "phoebe": "podEl",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "p",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "p",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 1,
              "ort_consonants": "d",
              "ort_end_consonants": "l",
              "ort_vowels": "é",
              "ph_consonants": "d",
              "ph_end_consonants": "l",
              "ph_vowels": "é",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "podél",
          "token_lc": "podél",
          "xsampa": "podE:l"
        },
        {
          "cft": "sťeni",
          "lemma": "stěna",
          "morph": "NNFS2-----A-----",
          "phoebe": "sTeni",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "st",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "sť",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "rhyme_from": "v",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "W",
              "rhyme_from": "c",
              "stress": "0"
            }
          ],
          "token": "stěny",
          "token_lc": "stěny",
          "xsampa": "scEnI"
        }
      ]
    },
    {
      "metre": {
        "J": {
          "basic": "1",
          "clause": "f",
          "foot": "5",
          "pattern": "WSWSWSWSWSW"
        }
      },
      "punct": {
        "3": "–",
        "6": "...!"
      },
      "rhyme": 2,
      "sections": "mRm10101000",
      "stanza": 2,
      "text": "a za ním – pohled smutně vytřeštěný...!",
      "words": [
        {
          "cft": "a",
          "lemma": "a",
          "morph": "J^--------------",
          "phoebe": "a",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "a",
          "token_lc": "a",
          "xsampa": "a"
        },
        {
          "cft": "za",
          "lemma": "za",
          "morph": "RR--7-----------",
          "phoebe": "za",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "z",
              "ort_end_consonants": "",
              "ort_vowels": "a",
              "ph_consonants": "z",
              "ph_end_consonants": "",
              "ph_vowels": "a",
              "position": "S",
              "stress": "0"
            }
          ],
          "token": "za",
          "token_lc": "za",
          "xsampa": "za"
        },
        {
          "cft": "ňím",
          "lemma": "on",
          "morph": "P5IS7--3--------",
          "phoebe": "NIm",
          "punct": "–",
          "syllables": [
            {
              "length": 1,
              "ort_consonants": "n",
              "ort_end_consonants": "m",
              "ort_vowels": "í",
              "ph_consonants": "ň",
              "ph_end_consonants": "m",
              "ph_vowels": "í",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "ním",
          "token_lc": "ním",
          "xsampa": "Ji:m"
        },
        {
          "cft": "pohlet",
          "lemma": "pohled",
          "morph": "NNIS1-----A-----",
          "phoebe": "pohlet",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "p",
              "ort_end_consonants": "",
              "ort_vowels": "o",
              "ph_consonants": "p",
              "ph_end_consonants": "",
              "ph_vowels": "o",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "hl",
              "ort_end_consonants": "d",
              "ort_vowels": "e",
              "ph_consonants": "hl",
              "ph_end_consonants": "t",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "pohled",
          "token_lc": "pohled",
          "xsampa": "poh\\lEt"
        },
        {
          "cft": "smutňe",
          "lemma": "smutně",
          "morph": "Dg-------1A-----",
          "phoebe": "smutNe",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "sm",
              "ort_end_consonants": "",
              "ort_vowels": "u",
              "ph_consonants": "sm",
              "ph_end_consonants": "",
              "ph_vowels": "u",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "tn",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "tň",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            }
          ],
          "token": "smutně",
          "token_lc": "smutně",
          "xsampa": "smutJE"
        },
        {
          "cft": "vitřešťení",
          "lemma": "vytřeštěný",
          "morph": "AAIS1----1A-----",
          "phoebe": "vitReSTenI",
          "punct": "...!",
          "syllables": [
            {
              "length": 0,
              "ort_consonants": "v",
              "ort_end_consonants": "",
              "ort_vowels": "y",
              "ph_consonants": "v",
              "ph_end_consonants": "",
              "ph_vowels": "i",
              "position": "S",
              "stress": "1"
            },
            {
              "length": 0,
              "ort_consonants": "tř",
              "ort_end_consonants": "",
              "ort_vowels": "e",
              "ph_consonants": "tř",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "W",
              "stress": "0"
            },
            {
              "length": 0,
              "ort_consonants": "št",
              "ort_end_consonants": "",
              "ort_vowels": "ě",
              "ph_consonants": "šť",
              "ph_end_consonants": "",
              "ph_vowels": "e",
              "position": "S",
              "rhyme_from": "v",
              "stress": "0"
            },
            {
              "length": 1,
              "ort_consonants": "n",
              "ort_end_consonants": "",
              "ort_vowels": "ý",
              "ph_consonants": "n",
              "ph_end_consonants": "",
              "ph_vowels": "í",
              "position": "W",
              "rhyme_from": "c",
              "stress": "0"
            }
          ],
          "token": "vytřeštěný",
          "token_lc": "vytřeštěný",
          "xsampa": "vItP\\EScEni:"
        }
      ]
    }
  ],
  "verses": [
    {
      "clause": "m",
      "foot": "6",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSWS",
      "rhymeclass": 1,
      "rhymeletter": "A",
      "rhymesubscript": "",
      "rythm": "R10100m1010m",
      "stanza": 0,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "P"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "W",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "t"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": ", ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "ch"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "u"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "e"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "sl"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "š"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "n"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "s"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v m"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "j"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "j"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "i"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "zb"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "u"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "... ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "vkr"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0",
                "rhyming"
              ],
              "text": "a"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress0",
                "rhyming"
              ],
              "text": "d"
            }
          ],
          "position": "S",
          "stress": "0"
        }
      ],
      "text": "Po tichu, neslyšen se v moji jizbu vkrad’..."
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 2,
      "rhymeletter": "B",
      "rhymesubscript": "",
      "rythm": "m10m1101010",
      "stanza": 0,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "B"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "e"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "č"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "r"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "– ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "j"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "i"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "ž"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "š"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress1"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress1"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "zv"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "ln"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "a"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "p"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "d"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "é"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "st"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1",
                "rhyming"
              ],
              "text": "ě"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1",
                "rhyming"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "Byl večer již – šel zvolna podél stěny"
    },
    {
      "clause": "m",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWS",
      "rhymeclass": 1,
      "rhymeletter": "A",
      "rhymesubscript": "",
      "rythm": "mRm1010101",
      "stanza": 0,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "a"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "z"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "a"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": "– ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "í"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "m"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "př"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "í"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "št"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "í"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "c"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "t"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "e"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "skn"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "ý"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "chl"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1",
                "rhyming"
              ],
              "text": "a"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress1",
                "rhyming"
              ],
              "text": "d"
            }
          ],
          "position": "S",
          "stress": "1"
        }
      ],
      "text": "a za ním – příští noci teskný chlad"
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 2,
      "rhymeletter": "B",
      "rhymesubscript": "",
      "rythm": "m1010101000",
      "stanza": 0,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "a"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "č"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "í"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "s"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "p"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "hl"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "d"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "sm"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "u"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "tn"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "ě"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "y"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "tř"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "št"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0",
                "rhyming"
              ],
              "text": "ě"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": "....! ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0",
                "rhyming"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "ý"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "a čísi pohled smutně vytřeštěný....!"
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 3,
      "rhymeletter": "C",
      "rhymesubscript": "",
      "rythm": "m10100R1010",
      "stanza": 1,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "A"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "st"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "í"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "mr"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "a"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "z"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "i"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "é"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress1"
              ],
              "text": "u"
            }
          ],
          "position": "W",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "dv"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "é"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "ř"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "í"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "zř"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1",
                "rhyming"
              ],
              "text": "e"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": ", ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1",
                "rhyming"
              ],
              "text": "l"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "A stíny mrazivé u dvéří zřely,"
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 3,
      "rhymeletter": "C",
      "rhymesubscript": "",
      "rythm": "R1010101010",
      "stanza": 1,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "př"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress1"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress1"
              ],
              "text": "d"
            }
          ],
          "position": "W",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "kn"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "m"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "l"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "h"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "zh"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "ou"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "stl"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v z"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "á"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "v"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "o"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "j"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "stm"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1",
                "rhyming"
              ],
              "text": "ě"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": ". ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1",
                "rhyming"
              ],
              "text": "l"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "ý"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "před okny mlhy zhoustly v závoj stmělý."
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 2,
      "rhymeletter": "B",
      "rhymesubscript": "",
      "rythm": "cmmmm101010",
      "stanza": 2,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stressc"
              ],
              "text": "A"
            }
          ],
          "position": "W",
          "stress": "c"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "j"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "á"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "b"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "y"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "!... ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "s"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "á"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionS",
                "afterstress0"
              ],
              "text": "m"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "O"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "n"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "kr"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "á"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "č"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "p"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "d"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "é"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "l"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "st"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1",
                "rhyming"
              ],
              "text": "ě"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1",
                "rhyming"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "y"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "A já byl sám!... On kráčel podél stěny"
    },
    {
      "clause": "f",
      "foot": "5",
      "metre": "J",
      "metrum": "jamb",
      "narrators_gender": "",
      "pattern": "WSWSWSWSWSW",
      "rhymeclass": 2,
      "rhymeletter": "B",
      "rhymesubscript": "",
      "rythm": "mRm10101000",
      "stanza": 2,
      "syllables": [
        {
          "after": "",
          "parts": [],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "a"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "z"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0"
              ],
              "text": "a"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": "– ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "í"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "m"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "p"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "o"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "hl"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            },
            {
              "classes": [
                "syllpart",
                "ort_end_consonants",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "d"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "sm"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "u"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": " ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "tn"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "ě"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress1",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "v"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress1"
              ],
              "text": "y"
            }
          ],
          "position": "S",
          "stress": "1"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress1"
              ],
              "text": "tř"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0"
              ],
              "text": "e"
            }
          ],
          "position": "W",
          "stress": "0"
        },
        {
          "after": "",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionS",
                "beforestress0",
                "afterpositionW",
                "afterstress0"
              ],
              "text": "št"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionS",
                "stress0",
                "rhyming"
              ],
              "text": "ě"
            }
          ],
          "position": "S",
          "stress": "0"
        },
        {
          "after": "...! ",
          "parts": [
            {
              "classes": [
                "syllpart",
                "ort_consonants",
                "beforepositionW",
                "beforestress0",
                "afterpositionS",
                "afterstress0",
                "rhyming"
              ],
              "text": "n"
            },
            {
              "classes": [
                "syllpart",
                "ort_vowels",
                "positionW",
                "stress0",
                "rhyming"
              ],
              "text": "ý"
            }
          ],
          "position": "W",
          "stress": "0"
        }
      ],
      "text": "a za ním – pohled smutně vytřeštěný...!"
    }
  ],
}
```
