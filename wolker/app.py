import bottle
# import edupo.wolker.common as common
import common

@bottle.route('/')
def page():
    return common.page()


# serve static files in the given subdirectories
@bottle.route('/<directory:path:re:(css|genimgs|fa-symbols|fonts).*>/<style>')
def static(directory, style):
    return bottle.static_file(style, directory)



application = bottle.default_app()

