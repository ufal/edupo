import re

import parsy

special_symbols = '↪↩↦↻↺⇉⇇' #↤
nonres_chars = parsy.regex(r'[^' + special_symbols + ']+')

def parse_to_dict(p):
    return p.map(lambda x: [a for a in x if a is not None]).map(dict)

# TODO convert these to dataclasses
class Fixed():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Fixed({repr(self.value)})'
    
    @staticmethod
    def parser():
        return nonres_chars.map(Fixed).desc('fixed string')
    
    def poem_parser(self):
        return parsy.string(self.value) >> parsy.success(None).desc(f'fixed string {repr(self.value)}')

class Variable():
    def __init__(self, name, separator):
        self.name = name
        self.separator = separator

    def __repr__(self):
        return f'Variable({self.name}↦{repr(self.separator)})'

    @staticmethod
    def parser():
        return parsy.seq(
            parsy.string('↪') >> nonres_chars << parsy.string('↦'),
            nonres_chars << parsy.string('↩')
        ).combine(Variable).desc('variable')
    
    def poem_parser(self):
        return parsy.regex(r'(.*?)' + re.escape(self.separator), group=1).tag(self.name).desc(f'variable {self.name}')

class Verse():
    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f'Verse({self.items})'

    @staticmethod
    def parser():
        items = parsy.alt(Fixed.parser(), Variable.parser())
        return (parsy.string('↻') >> items.many() << parsy.string('↺')).map(Verse).desc('verse')

    def poem_parser(self):
        return parse_to_dict(parsy.seq(*[item.poem_parser() for item in self.items])).desc('verse').many().tag('verses')

class Stanza():
    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f'Stanza({self.items})'

    @staticmethod
    def parser():
        items = parsy.alt(Fixed.parser(), Variable.parser(), Verse.parser())
        return (parsy.string('⇉') >> items.many() << parsy.string('⇇')).map(Stanza).desc('stanza')

    def poem_parser(self):
        return parse_to_dict(parsy.seq(*[item.poem_parser() for item in self.items])).desc('stanza').many().tag('stanzas')

class Template():
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