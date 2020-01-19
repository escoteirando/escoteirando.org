from escoteirando.mappa.mappa import Mappa



def test_mappa_login():
    mappa = Mappa('.cache')
    assert mappa.login('guionardo', 'A1GU')
