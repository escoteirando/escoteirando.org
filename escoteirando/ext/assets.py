from flask_assets import Environment, Bundle


def init_app(app):
    assets = Environment(app)
    js = Bundle('api.js', 'base.js', 'signin.js',
                filters='jsmin', output='gen/packed.js')
    assets.register('js_all', js)
