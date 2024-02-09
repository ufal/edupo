import bottle
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
        replacements[name.upper()] = bottle.request.params.getunicode(name, '')
    return replacements

# serve static files in the given subdirectories
@bottle.route('/<root:re:(wtr|wolker|panwtr)>/<directory:path:re:(css|genimgs|fa-symbols|fonts).*>/<filename>')
def static(root, directory, filename):
    return bottle.static_file(filename, directory)

# intro
@bottle.route('/wtr/', method='ANY')
@bottle.route('/wtr/index.py', method='ANY')
def intro():
    return common.page('intro.html', get_replacements())

# serve simple generic pages
@bottle.route('/wtr/page.py', method='ANY')
def page():
    return common.page(get_page(), get_replacements())

# serve specific pages
@bottle.route('/wtr/gallery.py', method='ANY')
def gallery():
    import gallery
    return gallery.main()

@bottle.route('/wtr/slideshow.py', method='ANY')
def slideshow():
    return common.slideshow()

# admin gallery: at different path!
@bottle.route('/panwtr/gallery.py')
def admin_gallery():
    return gallery.main('admin')

# public post: at different path!
@bottle.route('/wolker/<key>')
def public_post(key):
    return common.post(key)

application = bottle.default_app()

