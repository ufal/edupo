import bottle
import common

DEFAULTPAGE = 'intro'
def get_page():
    page = bottle.request.params.get('page', DEFAULTPAGE)
    if not page.isidentifier():
        page = DEFAULTPAGE
    return f"{page}.html"

def get_replacements(names=[]):
    replacements = {}
    if not names:
        names = bottle.request.params.replacements.split(',')
    for name in names:
        replacements[name.upper()] = bottle.request.params.getunicode(name, '')
    return replacements

# serve static files in the given subdirectories
@bottle.route('/<root:re:(wtr|wolker|panwtr)>/<directory:path:re:(css|genimgs|qrcodes|fa-symbols|fonts).*>/<filename>')
def static(root, directory, filename):
    return bottle.static_file(filename, directory)

@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico')

#@bottle.route('/<directory:path:re:(css|fa-symbols|fonts).*>/<filename>')
#def static_root(directory, filename):
#    return bottle.static_file(filename, directory)

# intro
@bottle.route('/wtr/', method='ANY')
@bottle.route('/wtr/index.py', method='ANY')
def intro():
    return common.indexpage()

# serve simple generic pages
@bottle.route('/wtr/page.py', method='ANY')
def page():
    return common.page(get_page(), get_replacements())

# serve specific pages
@bottle.route('/wtr/wolker_image.py', method='ANY')
def wolker_image():
    form = bottle.request.params
    replacements = get_replacements([
        'image', 'thread_id', 'text', 'title', 'back', 'prevfull', 'zalozni'])
    return common.wolker_image(form.title, form.prefix, form.text, replacements)

@bottle.route('/wtr/wolker_chat.py', method='ANY')
def wolker_chat():
    form = bottle.request.params
    return common.wolker_chat(
            form.text,
            form.get('typ', 'poem'),
            form.title,
            form.thread_id)

@bottle.route('/wtr/wolker_chat_illustrate.py', method='ANY')
def wolker_chat_illustrate():
    form = bottle.request.params
    replacements = get_replacements()
    return common.wolker_chat_illustrate(form, replacements)

@bottle.route('/wtr/welcome_wolker_feel.py', method='ANY')
def wolker_feel():
    form = bottle.request.params
    return common.wolker_feel(form.title, form.text)

@bottle.route('/wtr/share.py', method='ANY')
def share_page():
    form = {}
    for field in ['thread_id', 'title', 'text', 'image', 'author', 'zalozni']:
        form[field] = bottle.request.params.getunicode(field, '')
    return common.share_page(form)

@bottle.route('/wtr/gallery.py', method='ANY')
def gallery():
    return common.gallery()

@bottle.route('/wtr/slideshow.py', method='ANY')
def slideshow():
    return common.slideshow()

# admin gallery: at different path and password protect!
import hashlib
USER_HASH = '45a9b0809a297ff07bf70e2479709bfbe16dec18be8ba673b5b6131dff495f75'
PASS_HASH = '572d8c4a6ed4c265b6572650e2025146a418be4865955a1ce7a0b5e1b0b4c1e3'
def check_hash(text, hexhash):
    return hexhash == hashlib.sha256(text.encode()).hexdigest()
def auth_check(username, password):
    return check_hash(username, USER_HASH) and check_hash(password, PASS_HASH)

@bottle.route('/panwtr/gallery.py', method='ANY')
@bottle.auth_basic(auth_check)
def admin_gallery():
    return common.gallery('admin',
            bottle.request.params.delete,
            bottle.request.params.like)

@bottle.error()
def error_generic(e):
    return common.error(e)

@bottle.error(404)
def error_404(e):
    return common.error('Tato stránka neexistuje! ' + str(e))

@bottle.error(401)
def error_401(e):
    return common.error('Nejste přihlášeni platným jménem a heslem! ' + str(e))

# public post: at different path!
@bottle.route('/')
@bottle.route('/index.py')
@bottle.route('/wolker/')
@bottle.route('/wolker/index.py')
def public_home():
    return bottle.redirect('/wolker/credits')

@bottle.route('/wolker/credits')
def credits_public():
    return common.creditspublic()

@bottle.route('/wolker/<key>')
def public_post(key):
    return common.post(key)

application = bottle.default_app()

