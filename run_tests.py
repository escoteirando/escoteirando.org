from pprint import pprint

from escoteirando.mappa.mappa import Mappa

mappa = Mappa('.cache')

assert mappa.login('guionardo', 'A1GU')
pprint(mappa.__dict__())
