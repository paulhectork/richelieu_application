from sqlalchemy import text
import unittest

from ..app import app, db
from .. import orm


# *******************************************
# test our sql queries and query builders,
# and especially the query builders inn
# `app.search`
# *******************************************


class TestQueries(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app = app
        self.db = db
    def tearDown(self):
        self.client = None
        self.app = None
        self.db = None

    def test_advanced_search_iconography_individual(self):
        """
        test the individual search params in `/i/avanced-search-iconography/` route.

        query arguments are written pretty much like they are
        expected to be received from the frontend, and the
        raw SQL queries are written to mimic their SQLAlchemy
        equivalents (with ILIKE etc).
        """
        route = "/i/avanced-search-iconography/"

        # query_params is an array of [ <route params>, <raw sql query> ]
        query_params = [
            [ { "title": "galerie colbert, rue vivienne, 2ème arrondissement, paris" },
              """
              SELECT * FROM iconography
              JOIN title
              ON iconography.id = title.id_iconography
              AND title.entry_name ILIKE '%galerie colbert, rue vivienne, 2ème arrondissement, paris%';
              """
            ]
            ,
            [ { "author": "achille devéria" },
              """
              SELECT * FROM iconography
              JOIN r_iconography_actor
              ON iconography.id = r_iconography_actor.id_iconography
              AND r_iconography_actor.role = 'author'
              JOIN actor
              ON actor.id = r_iconography_actor.id_actor
              AND actor.entry_name ILIKE '%achille devéria%';
              """
            ]
            ,
            [ { "publisher": "aubert & cie" },
              """
              SELECT *
              FROM iconography
              JOIN r_iconography_actor
              ON iconography.id = r_iconography_actor.id_iconography
              AND r_iconography_actor.role = 'publisher'
              JOIN actor
              ON actor.id = r_iconography_actor.id_actor
              AND actor.entry_name ILIKE '%aubert & cie%';
              """
            ]
            ,
            [ { "theme": "mobilier urbain" }
            , """
              SELECT *
              FROM iconography
              JOIN r_iconography_theme
              ON r_iconography_theme.id_iconography = iconography.id
              JOIN theme
              ON r_iconography_theme.id_theme = theme.id
              AND theme.entry_name = 'mobilier urbain';
              """
            ]
            ,
            [ { "namedEntity": "Palais-Royal" }
            , """
              SELECT *
              FROM iconography
              JOIN r_iconography_named_entity
              ON r_iconography_named_entity.id_iconography = iconography.id
              JOIN named_entity
              ON r_iconography_named_entity.id_named_entity = named_entity.id
              AND named_entity.entry_name = 'Palais-Royal';
              """
            ]
            ,
            [ { "institution": "Musée Carnavalet" }
            , """
              SELECT *
              FROM iconography
              JOIN r_institution
              ON r_institution.id_iconography = iconography.id
              JOIN institution
              ON r_institution.id_institution = institution.id
              AND institution.entry_name = 'Musée Carnavalet';
              """
            ]
            ,
            [ { "dateFilter": "dateRange", "date[]": [1800,1810] }
            , """
              SELECT *
              FROM iconography
              WHERE NOT isempty( iconography.date * int4range(1800,1810+1) );
              """
            ]
            ,
            [ { "dateFilter": "dateExact", "date[]": [1829] }
            , """
              SELECT *
              FROM iconography
              WHERE iconography.date = int4range(1829,1829+1);
              """
            ]
            ,
            [ { "dateFilter": "dateBefore", "date[]": [1829] }
            , """
              SELECT *
              FROM iconography
              WHERE lower(iconography.date) <= 1829
              """
            ]
            ,
            [ { "dateFilter": "dateAfter", "date[]": [1829] }
            , """
              SELECT *
              FROM iconography
              WHERE upper(iconography.date) >= 1829
              """
            ]

        ]
        with self.app.app_context():  # avoid RuntimeError
            for ( http_params, raw_sql ) in query_params:
                r_http = self.client.get(route, query_string=http_params)
                r_sql = self.db.session.execute(text(raw_sql))
                r_http_count = len(r_http.json)
                r_sql_count = r_sql.rowcount

                self.assertEqual(r_http.status_code, 200)
                self.assertEqual( r_http_count, r_sql_count
                                , f"a different number of results was returned "
                                + f"by HTTP ({r_http_count}) and SQL ({r_sql_count}) for params {http_params}")
                self.assertTrue( r_http_count > 0 and r_sql_count > 0
                               , f"queries must return at least 1 result, "
                               + f"got {r_http_count} (HTTP) and {r_sql_count} (SQL) for params {http_params}"  )
        return self

    def test_advanced_search_iconography_combined(self):
        """
        test the combination of different params
        in `/i/avanced-search-iconography/` route
        """
        return self

