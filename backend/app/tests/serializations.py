from sqlalchemy.orm import Session
from random import randint
import unittest

from ..app import app, db
from .. import orm


# ********************************************
# test that the `serialize_lite` and
# `serialize_full` functions exist and
# return valid results
# ********************************************

# https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb

class TestSerializations(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.db = db
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
        self.app = None
        self.db = None

    def test_serializations_exist(self):
        """
        test that tables that have serialization functions have both
        `serialize_lite` and `serialize_full` methods
        """
        for t in self.tables:
            if hasattr(t, "serialize_lite") or hasattr(t, "serialize_full"):
                self.assertTrue(all([ hasattr(t, "serialize_lite")
                                    , hasattr(t, "serialize_full") ]),
                                f"{t} needs to contain both `serialize_lite()` and `serialize_full()` methods !")
        return self


    def test_serializations_work(self):
        """
        test that `serialize_lite` and `serialize_full` methods work
        """
        for t in self.tables:
            if hasattr(t, "serialize_lite") or hasattr(t, "serialize_full"):
                with self.app.app_context():
                    rowcount = len( db.session.execute( db.select(t) ).all() )
                    if rowcount > 0:
                        # `obj` is a random database row in `t`
                        id_ = randint(0, rowcount-1)
                        obj = t.query.get(id_)

                        # test `serialize_lite` and `serialize_full`
                        self.assertTrue( isinstance( obj.serialize_lite(), dict )
                                       , f"on table `{t}`: expected type `dict` "
                                       + f"on `{obj}.serialize_lite()`, "
                                       + f"got f{type(obj.serialize_lite())}")
                        self.assertTrue( isinstance( obj.serialize_full(), dict )
                                       , f"on table `{t}`: expected type `dict` "
                                       + f"on `{obj}.serialize_lite()`, "
                                       + f"got {type(obj.serialize_lite())}")

        return self


if __name__ == "__main__":
    unittest.main()
