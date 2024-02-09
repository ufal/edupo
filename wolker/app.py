import bottle
# import edupo.wolker.common as common
import common

DEFAULTPAGE = 'welcome'
def get_page():
    page = bottle.request.params.get('page', DEFAULTPAGE)
    if not page.isidentifier():
        page = DEFAULTPAGE
    return f"{page}.html"

def get_replacements():
    replacements = {}
    names = bottle.request.params.replacements.split(',')
    for name in names:
        replacements[name.upper()] = bottle.request.params[name]
    return replacements

# serve static files in the given subdirectories
@bottle.route('/wtr/<directory:path:re:(css|genimgs|fa-symbols|fonts).*>/<style>')
def static(directory, style):
    return bottle.static_file(style, directory)

# serve simple pages
@bottle.route('/wtr/', method='ANY')
@bottle.route('/wtr/page.py', method='ANY')
def page():
    return common.page(get_page(), get_replacements())

application = bottle.default_app()

