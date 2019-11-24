# -*- coding: utf-8 -*-
import infra.config
from app import app

if __name__ == '__main__':
    #if not pre_run_tasks():
    #    exit()
    ip = '0.0.0.0'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']
    
    app.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
