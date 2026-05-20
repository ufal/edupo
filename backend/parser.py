from dataclasses import dataclass
import re

import parsy

special_symbols = '↪↩↦↻↺⇉⇇' #↤
nonres_chars = parsy.regex(r'[^' + special_symbols + ']+')

def parse_to_dict(p):
    return p.map(lambda x: [a for a in x if a is not None]).map(dict)

class TParser():
    pass

@dataclass
class Fixed(TParser):
    value: str
    
    @staticmethod
    def parser():
        return nonres_chars.map(Fixed).desc('fixed string')
    
    def poem_parser(self):
        return parsy.string(self.value).result(None).desc(f'fixed string {repr(self.value)}')

@dataclass
class Variable(TParser):
    name: str
    separator: str
    
    @staticmethod
    def parser():
        return parsy.seq(
            parsy.string('↪') >> nonres_chars << parsy.string('↦'),
            nonres_chars << parsy.string('↩')
        ).combine(Variable).desc('variable')
    
    def poem_parser(self):
        return parsy.regex(r'(.*?)' + re.escape(self.separator), group=1).tag(self.name).desc(f'variable {self.name}')

@dataclass
class Verse(TParser):
    items: list[TParser]

    @staticmethod
    def parser():
        items = parsy.alt(Fixed.parser(), Variable.parser())
        return (parsy.string('↻') >> items.many() << parsy.string('↺')).map(Verse).desc('verse')

    def poem_parser(self):
        return parse_to_dict(parsy.seq(*[item.poem_parser() for item in self.items])).desc('verse').many().tag('verses')

@dataclass
class Stanza(TParser):
    items: list[TParser]

    @staticmethod
    def parser():
        items = parsy.alt(Fixed.parser(), Variable.parser(), Verse.parser())
        return (parsy.string('⇉') >> items.many() << parsy.string('⇇')).map(Stanza).desc('stanza')

    def poem_parser(self):
        return parse_to_dict(parsy.seq(*[item.poem_parser() for item in self.items])).desc('stanza').many().tag('stanzas')

class Template(TParser):
    def __init__(self, template_txt):
        self.template = Template.parser().parse(template_txt)

    def __repr__(self):
        return f'Template({self.template})'

    @staticmethod
    def parser():
        return parsy.alt(Fixed.parser(), Variable.parser(), Verse.parser(), Stanza.parser()).many().desc('template')

    def poem_parser(self):
        return parse_to_dict(parsy.seq(*[item.poem_parser() for item in self.template])) << parsy.string('\n').many()

'''
with open('prompt_templates/chudoba.txt') as f:
    template = Template(f.read())

print(template)

with open('test2.txt') as f:
    txt = f.read()
    print(txt)
    poem = template.poem_parser().parse(txt)
    print(poem)
'''