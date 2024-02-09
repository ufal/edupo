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
        replacements[name.upper()] = bottle.request.params.get(name, '')
    return replacements

# serve static files in the given subdirectories
@bottle.route('/wtr/<directory:path:re:(css|genimgs|fa-symbols|fonts).*>/<filename>')
def static(directory, filename):
    return bottle.static_file(filename, directory)

# serve simple generic pages
@bottle.route('/wtr/', method='ANY')
@bottle.route('/wtr/page.py', method='ANY')
def page():
    return common.page(get_page(), get_replacements())

# serve specific pages
import slideshow
mains = {
    'slideshow': slideshow.main,
}
@bottle.route('/wtr/<page:re:(gallery|slideshow).py>', method='ANY')
def dynamic_page(page):
    return mains[page]()

# public access to posts: serve at different path!
@bottle.route('/wolker/<directory:path:re:(css|genimgs|fa-symbols|fonts).*>/<filename>')
def public_static(directory, filename):
    return bottle.static_file(filename, directory)

@bottle.route('/wolker/<key>')
def public_post():
    return common.post(key)

application = bottle.default_app()

