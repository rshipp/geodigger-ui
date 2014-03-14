import os
from pyramid.config import Configurator

import geodiggerui.config as config

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    import geodiggerui.config as config
    # Make sure the Temp dir exists.
    ui_tmp_dir = config.ui['tmp']
    if not os.path.exists(ui_tmp_dir):
        os.makedirs(ui_tmp_dir)

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'geodiggerui:static/', cache_max_age=3600)
    config.add_static_view('download', ui_tmp_dir, cache_max_age=3600)
    config.add_route('home', '/home')
    config.add_route('filter', '/')
    config.add_route('done', '/done')
    config.scan()
    return config.make_wsgi_app()
