from escoteirando.mappa.mappa import Mappa

mappa = Mappa('.cache')

assert mappa.login('guionardo','A1GU')
print(dict(mappa))