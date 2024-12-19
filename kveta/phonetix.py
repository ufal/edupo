import os
import re
import string
import csv
import pickle
import sys

#from unidecode import unidecode

class Phonetix:
    '''
    ₁
    ₂
    ₃
    ₄
    ₅ Hranice mezi grafickými slovy
    ₆ Hranice mezi grafickými slovy obsahující "silnou" interpunkci
    '''

    def __init__(self):
        '''
        Constructor: definition of sound categories
        '''
        self.v = 'aáeéiíoóuúůyýěAEO'
        self.c = 'bcZčŽdďfghjkmnňpqřŘsštťvwxzž'
        self.p = self.c + 'rlRL'
        self.voic = 'bvdzďžghZŽ'
        self.unvoic = 'pftsťškxcč'
        self.son = 'mnňMNrlRLjvPB' + self.v

        self.parent = os.path.dirname(__file__)

        file_general = os.path.join(self.parent, 'dicts',
                                    'general.pickle')
        with open(file_general, 'rb') as handle:
            dict_general = pickle.load(handle)

        file_loanwords = os.path.join(self.parent, 'dicts',
                                      'loanwords.pickle')
        with open(file_loanwords, 'rb') as handle:
            dict_loanwords = pickle.load(handle)

        file_diphthongs = os.path.join(self.parent, 'dicts',
                                       'diphthongs.pickle')
        with open(file_diphthongs, 'rb') as handle:
            dict_diphthongs = pickle.load(handle)

        self.dict = {
            'general': dict_general,
            'loanwords': dict_loanwords,
            'diphthongs': dict_diphthongs,
        }

    def replace(self, tab):
        '''
        General replace function
        '''
        for t in tab:
            self.t = re.sub(t[0], t[1], self.t)

    def punctuation(self):
        '''
        Mark boundaries according to punctuation.
        Remove remaining punctuation.
        '''
        self.replace((
            (r'[.;?!,]+', r'₆'),
            (r' [\-\–]+ ', r'₆'),
            (r'^|$', r'₆'),
            (r'(\s)', r' '),
            (r'(\w)[\'’‘](\w)', r'\1\2'), # "byl's", pokud je jako jeden token
            # ('₆(\s)', r'₆\1₆'),
            # ('([^₆])(\s)', r'\1 \2 '),
            (r'["#$%&\'’‘()*+/:;<=>@[\]^_`{|}~–]', r' '),
            (r' +', r'₅'),
            (r'₅*₆+₅*', r'₆'),
        ))
    
    def numbers(self):
        '''
        Replace numbers expressed by digits by respective word forms.
        '''
        # TODO: líp udělat víceciferná čísla
        self.replace((
            (r'0', r'nula'),
            (r'1', r'jedna'),
            (r'2', r'dva'),
            (r'3', r'tři'),
            (r'4', r'čtyři'),
            (r'5', r'pět'),
            (r'6', r'šest'),
            (r'7', r'sedm'),
            (r'8', r'osm'),
            (r'9', r'devět'),
        ))

    def lowercase(self):
        '''
        Lowercase all characters
        '''
        self.t = self.t.lower()

    def loanwords(self):
        '''
        Get transcription of loanwords from the dictionary
        '''
        for w in self.dict['loanwords']:
            self.replace((
                (w, self.dict['loanwords'][w]),
            ))

    def loanchars(self):
        '''
        Replace non-Czech alphabet characters
        '''
        vx = re.sub('u', '', self.v)
        self.replace((
            (r'qu([{0}])'.format(self.v), r'kv\1'),
            # (r'q([{0}])'.format(vx), r'kv\1'),
            (r'q'.format(vx), r'kv'),
            ('ĺ|ľ', 'lj'),
        ))
        self.t = self.t.translate(str.maketrans('†æîâźôêęçïϊàèwäöüëćśńł', 'teiazoeeciiáéveeyečšňl'))

    def simplify_con_groups(self):
        '''
        Simplify complex consonant clusters
        '''
        self.replace((
            (r'([{0}])\1+ '.format(self.p), r'\1 '),
            ('dt ', 't '),
            # TODO -- přidat jako možnost celé třídy:
            # slavnostní výslovnost: neaplikovat
            ('srdc', 'src'),
            ('dcer', 'cer'),
            ('dceř', 'ceř'),
            ('zsina', 'sina'),
            ('anna', 'ana'),
            ('nně', 'ně'),
            ('nní', 'ní'),
            ('nn(y|ý|ou|á|é)', r'n\1'),
            ('nnost', 'nost'),
            ('ěkk', 'ěk'),
        ))

    def hyphen(self):
        '''
        Process words with hyphen
        '''
        self.replace((
            (r'([jmnňřrlaáeéiíoóuúůyýě])\-(li|liž)(₅|₆)', r'\1₁\2\3'),
            (r'([ěo])\-', r'\1₄'),
            (r'\-(li|liž)(₅|₆)', r'₂\1\2'),
            (r'\-', r'₆'),
            (r'₅*₆+₅*', r'₆'),
        ))

    def diphthongs1(self):
        '''
        Process bigram <ou>
        '''
        self.replace((
            ('ou(₅|₆)', r'O\1'),
        ))

    def glottal_stop(self):
        '''
        Add glottal stop
        '''
        self.replace((
            # fakultativní - možnost třídy
            ('(₅|₆)nej([{0}])'.format(self.v), r'\1nejX\2'),
            ('(₅|₆)(pod|nad|bez|roz|ob|ne)ú', r'\1\2Xú'),
            ('oú', 'oXú'),
            ('áctapůl', 'áctXapůl'),
            ('(₅|₆)(dva|tři|čtyři|pět|šest|sedm|osm|devět|deset|půl)a',
             r' \1\2Xa'),
            ('(₅|₆)(anglo|anty|arci|celo|dvou|eko|indo|jedno|jiho|' +
             'kvazi|lehko|makro|malo|mezi|mikro|mnoho|multi|nacti|' +
             'nízko|novo|proti|prvo|pře|při|pseudo|rychlo|sebe|' +
             'semi|severo|spolu|staro|středo|své|těžko|tří|ultra|' +
             'vele|velko|vnitro|vy|vý|východo|vysoko|západo|znovu)' +
             '([{0}])'.format(self.v), r'\1\2X\3'),
        ))

        d = self.dict['general']
        dv = list(re.sub('^(₅|₆)*|(₅|₆)*\n', '', i)
                  for i in d if re.match(r'^(₅|₆)*[{0}]'.format(self.v), i))
        dv = ("|").join(dv)
        dc = list(re.sub('^(₅|₆)*|(₅|₆)*\n', '', i)
                  for i in d if re.match(r'(₅|₆)*s', i))
        dc = ("|").join(dc)
        d = list(re.sub('^(₅|₆)*|(₅|₆)*\n', '', i) for i in d)
        d = ("|").join(d)

        self.replace((
            (r'(₅|₆)(ne)?({0})({0})?({1})'
             .format('s|z|v|po|od|na|při|pře|pod|nad|před', dv),
             r' \1\2\3X\4'),
            (r'(₅|₆)neod({0})'.format(d), r'\1neXod\2'),
            (r'(₅|₆)(ne)?(po|na|při)?(pod|od|nad|před)({0})'
             .format(dc),
             r'\1\2\3\4₃\5'),
            ))

    def hiatus(self):
        '''
        Insert <j> into vocalic clusters
        '''
        vx = 'iyíý'
        self.replace((
            ('([{0}])([{1}])'.format(vx, self.v), r'\1j\2'),
            ('([{0}])([{1}])'.format(self.v, vx), r'\1j\2'),
            # ? yard > yjard >[později]> jjard === musí následovat po [def iy]
        ))

    def diphthongs2(self):
        '''
        Process bigrams <ou>, <eu>, <au>
        TODO: dictionary || random forest classification
        '''

        self.replace((
            #('(₅|₆)au', r'\1A'),
            #('(₅|₆)eu', r'\1E'),
            #('(₅|₆)ou', r'\1O'),
            ('ou', 'O'),
            ('o₇u', 'ou'), # ₇ is used here as a sign in places where ou is not a diphtong
            ('au', 'A'),
            ('a₇u', 'au'), # ₇ is used here as a sign in places where au is not a diphtong
            ('eu', 'E'),
            ('e₇u', 'eu'), # ₇ is used here as a sign in places where eu is not a diphtong
            # TODO: v některých případech sem patří také ráz "glottal stop"
        ))

    def yat(self):
        '''
        Process <ě>
        '''
        self.replace((
            ('dě', 'ďe'),
            ('tě', 'ťe'),
            ('ně', 'ňe'),
            ('bě', 'bje'),
            ('pě', 'pje'),
            ('fě', 'fje'),
            ('vě', 'vje'),
            ('mě', 'mňe'),
            ('ě', 'e'),
        ))

    def iy(self):
        '''
        Process <i>/<y>
        '''
        self.replace((
            ('di', 'ďi'),
            ('ti', 'ťi'),
            ('ni', 'ňi'),
            ('dí', 'ďí'),
            ('tí', 'ťí'),
            ('ní', 'ňí'),
            ('(₅|₆)y([{0}])'.format(self.v), r'\1j\2'),
            # tohle pravidlo nikdy nenastane > ^ya přepíše pravislo pro hiát
            ('(₅|₆)y([{0}])'.format(self.p), r'\1i\2'),
            # tohle lze vypustit (viz y>i)
            ('([{0}])y([{0}])'.format(self.v), r'\1j\2'),
            ('([{0}])y([{0}])'.format(self.c), r'\1i\2'),
            # tohle lze vypustit (viz y>i)
            ('y', 'i'),
            # subsumuje taky poslední dvě uvedený v souboru

            # TODO -- doplnit, že musí následovat vokál
            #('(₅|₆)i', r'\1j'),
            ('ý', 'í')
        ))

    def overring(self):
        '''
        Process <ů>
        '''
        self.replace((
            ('ů', 'ú'),
        ))

    def x_ch(self):
        '''
        Process <x>
        '''
        self.replace((
            # TODO - na začátku slova, nebo po X (ráz), nebo malá 4
            ('ex([{0}])'.format(self.v), r'egz\1'),
            ('x', 'ks'),
            ('ch', 'x'),
        ))

    def ismus(self):
        '''
        Process <ismus> suffix and its derivates
        '''
        self.replace((
            ('ismus(₅|₆)', r'izmus\1'),
            ('ismu(₅|₆)', r'izmu\1'),
            ('isme(₅|₆)', r'izme\1'),     # FIXME -- bysme !!!
            ('ismem(₅|₆)', r'izmem\1'),
            ('ismi(₅|₆)', r'izmi\1'),
            ('ismú(₅|₆)', r'izmú\1'),
            ('ismúm(₅|₆)', r'izmúm\1'),
            ('ismex(₅|₆)', r'izmey\1'),
        ))

    def affricate(self):
        '''
        Convert <ts>, <ds>, <tz>... to simple affricates
        '''
        self.replace((
            ('[td]s', 'c'),
            ('[td]z', 'Z'),
            ('[td]š', 'č'),
            ('[td]ž', 'Ž'),
            #('([td])\-([szšž])', '\1\2'),
        ))

    def assimilation(self):
        '''
        Process assimilation of voicing
        '''
        for i in range(len(self.t)-2, 0, -1):
            follower = self.t[i+1:]

            # neslabičné předložky voiced > unvoiced
            if i > 0 and len(follower) > 1 and re.match('^[₅₆][vz]₅', self.t[i-1:i+2]):
                if re.match('^₅[{0}]'.format(self.unvoic), follower):
                    self.t = self.t[:i] + self.unvoic[self.voic.index(self.t[i])] + follower
            # voiced > unvoiced
            elif self.t[i] in self.voic:
                if (re.match('^[{0}₅₆₂₄₁X]'.format(self.unvoic), follower)
                or  re.match('^ř[{0}₅₆₁]'.format(self.unvoic), follower)):
                    self.t = self.t[:i] + self.unvoic[self.voic.index(self.t[i])] + follower

            # neslabičné předložky unvoiced > voiced
            if i > 0 and len(follower) > 1 and re.match('^[₅₆][ks]₅', self.t[i-1:i+2]):
                if re.match('^₅[{0}]'.format(self.voic), follower):
                    self.t = self.t[:i] + self.voic[self.unvoic.index(self.t[i])] + follower
            # unvoiced > voiced
            elif self.t[i] in self.unvoic:
                if re.match('^ř?[{0}]'.format(self.voic[0] + self.voic[2:]), follower):
                    self.t = self.t[:i] + self.voic[self.unvoic.index(self.t[i])] + follower
                if (re.match('ř?[₂₄X₁]ř?[{0}]'.format(self.voic), follower)
                or  re.match('ř?[₂₄X₁]ř[{0}]'.format(self.son), follower)):
                    self.t = self.t[:i] + self.voic[self.unvoic.index(self.t[i])] + follower
        
    def sonant(self):
        '''
        Process sonants: mark syllabic ones, process their assimilation
        '''
        c = self.c.replace('j', '') + 'lr' # předslabikotvorný, r může být jiné r, např 'vrrrr'
        self.replace((
            # TODO -- přidat "rl " jako možnost třídy
            ('([{0}])r(₅|₆)'.format(c), r'\1R\2'),
            ('([{0}])l(₅|₆)'.format(c), r'\1L\2'),
            ('([{0}])r(₁)?l'.format(c), r'\1R\2l'),
            ('([{0}])l(₁)?r'.format(c), r'\1Lr'),
            ('([{0}])l(₁)?l'.format(c), r'\1L\2l'),
            ('([{0}])r([{1}])'.format(c, self.c), r'\1R\2'),
            ('([{0}])l([{1}])'.format(c, self.c), r'\1L\2'),

            # TODO -- možnost (pouze pro m)
            ('m([fv])'.format(c, self.c), r'V\1'),
            ('n([kg])'.format(c, self.c), r'W\1'),

            # TODO -- Aleš nejdřív ověří pravidla
            # ('([{0}])n([{0} ₂₄X])'.format(self.voic+self.unvoic), r'\1B\2'),
            # ('([{0}])([{1}])n([ ₂₄X])'.format(self.voic+self.unvoic+self.son,
            # self.voic+self.unvoic+'řŘmnňMNrljv'), r'\1\2B\3'),
            # ('([{0}])([{1}])m([ ₂₄X])'.format(self.voic+self.unvoic+self.son,
            # self.voic+self.unvoic+'řŘmnňMNrljv'), r'\1\2P\3'),

            # dočasně přidávám 'sedm' a 'osm' než Aleš ověří pravidla
            ('sedm([₅₆₂₄X{0}])'.format(self.voic+self.unvoic+'mnňMNrlRLjvPB'), r'sedP\1'),
            ('osm([₅₆₂₄X{0}])'.format(self.voic+self.unvoic+'mnňMNrlRLjvPB'), r'osP\1'),

        ))

    def unvoic_r(self):
        '''
        Unvoiced [ř]
        '''
        self.replace((
            ('ř(₅|₆)', r'Ř\1'),
            ('ř([₂₄X₁])([{0}])'.format(self.unvoic), r'Ř\1\2'),
            #('ř[₂₄X]([{0}])'.format(self.sonant), r'Ř@1'),
            ('([{0}])ř'.format(self.unvoic), r'\1Ř'),
        ))

    def initial_glottal_stop(self):
        '''
        Prepend glottal stop to words starting with vowel
        '''
        self.replace((
            ('(₅|₆)({[0]})'.format(self.v), r'\1X\2'),
        ))

    def final_schwa(self):
        '''
        Přidání švy nakonec neslabičných souhláskových skupin, které nejsou předložkami
        '''
        self.replace((
            ('(₅|₆)([bcZčŽdďfghjkmnňpqřŘsštťvwxzž]+)(₅|₆)', r'\1\2@\3'),
            ('(₅|₆)([bcZčŽdďfghjkmnňpqřŘsštťvwxzž]+)(₅|₆)', r'\1\2@\3'),
            # opakuji ten samý řádek, protože když následuje jedno hned po druhém, neopraví se obojí
        ))


    def transcript(self, text):
        '''
        GENERAL TRANSCRIPTION FUNCTION
        '''
        self.t = text
        self.punctuation()
        self.numbers()
        self.lowercase()
        self.loanwords()
        self.loanchars()
        self.simplify_con_groups()
        self.hyphen()
        self.diphthongs1()
        self.diphthongs2()
        self.glottal_stop()
        self.hiatus()
        self.yat()
        self.iy()
        self.overring()
        self.x_ch()
        self.ismus()
        self.affricate()
        self.assimilation()
        self.sonant()
        self.unvoic_r()
        self.initial_glottal_stop()
        self.final_schwa()

        return self.t

    def transcript_poem(self, poem):
        '''
        Apply transcription to Kveta object
        '''
        
        for i, l in enumerate(poem):
            text_string = str()
            for j, w in enumerate(l['words']):
                if 'nodip' in w:
                    text_string += w['nodip'] + ' '
                else:
                    text_string += w['token'] + ' '
                if 'punct' in w and re.search(r'[.;?!,\-\–]', w['punct']):
                       text_string += (' – ')
                     
            t = self.transcript(text_string)
            t = re.sub('[₅₆]', ' ', t)
            t = re.sub('[₁₂₃₄₇]', '', t)
            ts = t.strip().split(' ')
            for j, w in enumerate(l['words']):
                if len(ts) <= j:
                    print("WARNING: token mismatch during the transcription:", t, file=sys.stderr)
                    print(l['words'], file=sys.stderr)
                else:
                    # pokud je slovem neslabičná předložka, které fonetika přidala nakonec švu, musí se tato šva odstranit
                    if poem[i]['words'][j]['morph'][0] == 'R' and ts[j][-1] == '@':
                        ts[j] = ts[j][:-1]

                    poem[i]['words'][j]['cft'] = ts[j]
                
        return poem

    def phoebe2cft(self, poem):
        phoebe2cft_dict = {
            'a': 'a',
            'e': 'e',
            'i': 'i',
            'o': 'o',
            'u': 'u',

            'A': 'á',
            'E': 'é',
            'I': 'í',
            'O': 'ó',
            'U': 'ú',

            '0': 'O',
            '1': 'A',
            '2': 'E',

            'Q': 'R',
            'L': 'L',

            'p': 'p',
            'b': 'b',
            't': 't',
            'd': 'd',
            'T': 'ť',
            'D': 'ď',
            'k': 'k',
            'g': 'g',

            'f': 'f',
            'v': 'v',
            's': 's',
            'z': 'z',
            'S': 'š',
            'Z': 'ž',
            'x': 'x',
            #    'X',
            'h': 'h',
            'G': 'G', #je to v KČV?

            'c': 'c',
            '3': 'č',
            '4': 'Ž',
            'm': 'm',
            'n': 'n',
            'N': 'ň',
            '5': 'V',
            '6': 'W',
            'C': 'Z',
            #'Ž': 'č',

            'r': 'r',
            'l': 'l',
            'j': 'j',
            'R': 'ř', # 'P\\',
            'P': 'Ř', #: 'Q\\',

            'M': 'M', # slabikotvorné M
            'W': 'Y', # slabikotvorné Z
            'J': 'J', # slabikotvorné S
            'B': 'N', # slabikotvorné N
            'K': 'K', # slabikotvorné Š
            'Y': 'V', # slabikotvorné Ž

        }
        for i, l in enumerate(poem):
            for j, w in enumerate(l['words']):
                cft = ""
                for c in w["phoebe"]:
                    cft += phoebe2cft_dict[c]
                poem[i]['words'][j]['cft'] = cft
        return poem
    

                                    
