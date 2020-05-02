from escoteirando.ext.html import Tag
from escoteirando.ext.bootstrap import MenuItem, bootstrap_nav


def test_html():
    tag = Tag('a')
    assert tag.to_html() == '<a></a>'

    tag = Tag('a', href='#', enabled=None)
    assert tag.to_html() == '<a href="#" enabled></a>'

    tag = Tag('a', href='#').\
        add_child([Tag('p').set_innertext('Guionardo')])
    html = tag.to_html(tabbed=True)
    print(html)
    assert html

    nav = Tag('nav',
              _class='navbar navbar-expand-md navbar-dark bg-dark fixed-top',
              _children=[
                  Tag('a', _class='navbar-brand', href='#', _innertext='Navbar'),
                  Tag('button', _class='navbar-toggler', _type='button', data_toggle='collapse', data_target='#navbarsExampleDefault',
                      aria_controls='navbarsExampleDefault', aria_expanded='false', aria_label='Toggle navigation', _children=[
                          Tag('span', _class='navbar-toggler-icon')
                      ]),
                  Tag('div', id='navbarExampleDefault', _class='collapse navbar-collapse', _children=[
                      Tag('ul', _class='navbar-nav mr-auto', _children=[

                      ])
                  ])

              ])

    html = nav.to_html(tabbed=True)
    print(html)
    assert(html)

    _itens = [
        MenuItem('Home'),
        MenuItem('Link'),
        MenuItem('Disabled', disabled=True),
        MenuItem('Dropdown', subitens=[
            MenuItem('Action'),
            MenuItem('Another action'),
            MenuItem('Something else here')
        ])
    ]

    html = bootstrap_nav(_itens, True)
    with open('bootstrap.html','w') as f:
        f.write(html)

    print(html)
    assert html
