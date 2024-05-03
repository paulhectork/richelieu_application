from sqlalchemy.orm import Session
import unittest

from .build_engine import build_engine
from .. import orm


# ********************************************
# test that the `serialize_lite` and
# `serialize_full` functions exist and
# return valid results
# ********************************************


# voir ici pour faire des tests
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb

class TestSerializations(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()
        self.session = Session(self.engine)
        self.tables = [ orm.Institution
                      , orm.Licence
                      , orm.AdminPerson
                      , orm.Iconography
                      , orm.Cartography
                      , orm.Directory
                      , orm.Filename
                      , orm.Base
                      , orm.Place
                      , orm.Address
                      , orm.Title
                      , orm.Annotation
                      , orm.Theme
                      , orm.NamedEntity
                      , orm.Actor
                      , orm.PlaceGroup
                      , orm.R_IconographyActor
                      , orm.R_IconographyPlace
                      , orm.R_CartographyPlace
                      , orm.R_AddressPlace
                      , orm.R_IconographyNamedEntity
                      , orm.R_IconographyTheme
                      , orm.R_AdminPerson
                      , orm.R_Institution ]


    def tearDown(self):
        self.engine.rollback()

    def test_serializations(self):
        for t in self.tables:
            if hasattr(t, "serialize_lite") or hasattr(t, "serialize_full"):
                print("hello")


if __name__ == "__main__":
    unittest.main()
