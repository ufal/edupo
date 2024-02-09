import bottle
import edupo.wolker.common as common

@bottle.route('/')
def page():
    return common.page()

application = bottle.default_app()

