from escoteirando.ext.bootstrap import bootstrap_nav, MenuItem

_default_itens = [
    MenuItem('Home'),
    MenuItem('Minha seção', subitens=[
        MenuItem('Mapa de progressões')
    ]),
    MenuItem('Usuário',
             right_align=True,
             subitens=[
                 MenuItem('Perfil', disabled=True),
                 MenuItem('Informações UEB'),
                 MenuItem('Sair', onclick="logout()")
             ])
]


def get_login_navbar():
    return bootstrap_nav([
        MenuItem('Login', onclick="loginClick('login')"),
        MenuItem('Registrar', onclick="loginClick('register')"),
        MenuItem('Perdi minha senha', onclick="loginClick('perdi')")
    ])


def get_navbar():
    return bootstrap_nav(_default_itens)


def init_app(app):
    pass
    # app.jinja_env.globals.update(navbar=get_navbar)
