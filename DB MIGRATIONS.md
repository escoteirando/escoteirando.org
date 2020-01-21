export FLASK_APP=escoteirando.app:create_app
export FLASK_ENV=development
export FLASK_DEBUG=true

flask db init
flask db migrate
flask db upgrade

## Docker PG

https://linuxhint.com/run_postgresql_docker_compose/