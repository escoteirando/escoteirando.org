class Tag(dict):
    def __init__(self, name: str, **attributes):
        if not isinstance(name, str) or not name:
            raise ValueError('Tag name must be informed')
        self._name = name
        self._attributes = {}
        self._children = []
        self._innertext = None
        if len(attributes) > 0:
            for attr_name in attributes:
                value = attributes[attr_name]
                if attr_name == '_children':
                    self.add_child(value)
                elif attr_name == '_innertext':
                    self._innertext = value
                else:
                    if attr_name.startswith('_'):
                        attr_name = attr_name[1:]
                    attr_name = attr_name.replace('_', '-')
                    self.add_attr(attr_name, value)

    def add_attr(self, attribute: str, value=None):
        self._attributes[attribute] = value
        return self

    def rem_attr(self, attribute: str):
        if attribute in self._attributes:
            del(self._attributes[attribute])
        return self

    def add_child(self, child):
        if not isinstance(child, list):
            child = [child]

        for c in child:
            if c is not None:
                self._children.append(c)

        return self

    def set_innertext(self, text):
        self._children.clear()
        self._innertext = text
        return self

    def to_html(self, tabbed: bool = False, level: int = 0):
        spaces = '' if not tabbed else ' '*level*4
        subspaces = '' if not tabbed else ' '*(level+1)*4
        linebreak = '' if not tabbed else '\n'
        html = f'{spaces}<{self._name}'
        if len(self._attributes) > 0:
            attr = []
            for attr_name in self._attributes:
                if self._attributes[attr_name] is None:
                    attr.append(attr_name)
                else:
                    attr.append(f'{attr_name}="{self._attributes[attr_name]}"')
            html += ' ' + (' '.join(attr))
        html += '>'+linebreak
        if len(self._children) > 0 or self._innertext:
            if self._innertext:
                html += subspaces+self._innertext+linebreak
            else:
                for child in self._children:
                    html += child.to_html(tabbed, level+1)
        html += spaces+f'</{self._name}>'

        return html + linebreak

    def __str__(self):
        return f'Tag "{self._name}"'
