# -*- coding: utf-8 -*-

from app import app
from infra.tools.pre_run_tasks import pre_run_tasks

if __name__ == '__main__':
    if not pre_run_tasks():
        exit()
    ip = '0.0.0.0'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']

    # executa o servidor web do flask
    app.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
