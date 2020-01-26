from escoteirando.ext.html import Tag
from random import randint


class MenuItem:

    def __init__(self, text: str, **args):
        self._text = text
        self.enabled = 'disabled' not in args
        self.href = '#' if 'href' not in args else args['href']
        self.onclick = None if 'onclick' not in args else args['onclick']
        self.subitens = [] if 'subitens' not in args else args['subitens']
        self.right_align = 'right-align' in args

    def to_tag(self, first: bool = False):
        if len(self.subitens) == 0:
            a = Tag('a', _class='nav-link'+('' if self.enabled else ' disabled'),
                    href=self.href, _innertext=self._text +
                    ('' if not first else '<span class="sr-only">(current)</span>'))
            if not self.enabled:
                a.add_attr('aria-disabled', 'true')
            if self.onclick:
                a.add_attr('onclick', self.onclick)
            li = Tag('li', _class='nav-item' +
                     ('' if not first else 'active'), _children=[a])
        else:
            id = 'dropdown_{0:09d}'.format(randint(0, 999999999))

            div = Tag('div', _class='dropdown-menu', aria_labelledby=id)
            for item in self.subitens:
                item_a = Tag('a', _class='dropdown-item'+('' if item.enabled else ' disabled'),
                             href=item.href, _innertext=item._text)
                if not item.enabled:
                    item_a.add_attr('aria-disabled', 'true')
                if item.onclick:
                    item_a.add_attr('onclick', item.onclick)
                div.add_child(item_a)

            a = Tag('a', _class='nav-link dropdown-toggle', href='#', id=id, data_toggle='dropdown',
                    aria_haspopup='true', aria_expanded='false', _innertext=self._text)

            li = Tag('li', _class='nav-item dropdown'+('' if not first else 'active'), _children=[
                a, div
            ])

        return li


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


def bootstrap_nav(menuitens, tabbed: bool = False) -> str:
    ul = Tag('ul', _class='navbar-nav mr-auto')
    first = True
    for item in menuitens:
        ul.add_child(item.to_tag(first))
        first = False

    navbar_id = 'navbar_escoteirando'
    nav = Tag('nav',
              _class='navbar navbar-expand-md navbar-dark bg-dark fixed-top',
              _children=[
                  Tag('a', _class='navbar-brand', href='#', _children=[
                      Tag('img', src='/static/img/flor_de_lis_sombra.svg',
                          style='height:2em',
                          title="Escoteirando: Um portal para escotistas")
                  ]),
                  # Tag('a', _class='navbar-brand',
                  #     href='#', _innertext='Escoteirando'),
                  Tag('button', _class='navbar-toggler', _type='button', data_toggle='collapse', data_target='#navbar_escoteirando',
                      aria_controls='navbar_escoteirando', aria_expanded='false', aria_label='Toggle navigation', _children=[
                          Tag('span', _class='navbar-toggler-icon')
                      ]),
                  Tag('div', id='navbarExampleDefault',
                      _class='collapse navbar-collapse', _children=[ul])

              ])

    return nav.to_html(tabbed)


'''
<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
  <a class="navbar-brand" href="#">Navbar</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar_escoteirando" aria-controls="navbar_escoteirando" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbar_escoteirando">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="dropdown01" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dropdown</a>
        <div class="dropdown-menu" aria-labelledby="dropdown01">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <a class="dropdown-item" href="#">Something else here</a>
        </div>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
      <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>
'''
