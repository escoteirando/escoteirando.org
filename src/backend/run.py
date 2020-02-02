# -*- coding: utf-8 -*-
from app.start import config, create_app, pre_run_tasks

if __name__ == '__main__':
    if not pre_run_tasks():
        exit()

    app = create_app(config.FLASK_ENV)
    app.run(
        host=config.APP_HOST,
        debug=config.DEBUG,
        port=config.APP_PORT,
        use_reloader=config.DEBUG
    )
