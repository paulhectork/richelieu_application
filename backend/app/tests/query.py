from sqlalchemy import text
import unittest

from ..app import app, db
from .. import orm


# *******************************************
# test our sql queries and query builders,
# and especially the query builders inn
# `app.search`
# *******************************************


"""
-- the logic of doing AND,OR,NOT queries on JOINS

-- NOT. returns (1,3)
SELECT q1.id
FROM
  ( SELECT iconography.id FROM iconography
    WHERE iconography.id IN (1,2,3) ) AS q1
WHERE q1.id NOT IN
  ( SELECT iconography.id FROM iconography
    WHERE iconography.id IN (2,5,6) );

-- OR. returns (1,2,3,5,6)
SELECT *
FROM
  ( SELECT iconography.id FROM iconography
    WHERE iconography.id IN (1,2,3) ) AS q1
UNION
  ( SELECT iconography.id FROM iconography
    WHERE iconography.id IN (2,5,6) )
ORDER BY "id" ASC;

-- AND
SELECT iconography.id
FROM iconography
WHERE iconography.id IN (1,2,3)
AND iconography.id IN (2,5,6);

-- AND as inner join between subqueries
SELECT *
FROM
  ( SELECT iconography.id FROM iconography
    WHERE iconography.id IN (1,2,3) ) AS q1
INNER JOIN
  ( SELECT iconography.id FROM iconography
    WHERE iconography.id IN (2,5,6) ) AS q2
ON q1.id = q2.id;
"""



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
        test the individual search params in `/i/iconography/search` route.

        query arguments are written pretty much like they are
        expected to be received from the frontend, and the
        raw SQL queries are written to mimic their SQLAlchemy
        equivalents (with ILIKE etc).

        '%' is a special character in python strings, so we need to prefix
        strings that contain it with 'r'.
        """
        route = "/i/iconography/search"

        # queries is an array of [ <route params>, <raw sql query> ]
        queries = [
            [ { "title": ["bourse", "théâtre"] },
              r"""
              SELECT DISTINCT iconography.id
              FROM iconography
              JOIN title
              ON title.id_iconography = iconography.id
              AND title.entry_name ILIKE ANY(ARRAY['%bourse%', '%théâtre%']);
              """
            ]
            ,
            [ { "author": ["Daumier", "Atget"] },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              JOIN r_iconography_actor
              ON r_iconography_actor.id_iconography = iconography.id
              AND r_iconography_actor.role = 'author'
              JOIN actor
              ON r_iconography_actor.id_actor = actor.id
              AND actor.entry_name ILIKE ANY(ARRAY['%daumier%', '%atget%']);
              """
            ]
            ,
            [ { "publisher": ["Aubert", "Martinet"] },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              JOIN r_iconography_actor
              ON r_iconography_actor.id_iconography = iconography.id
              AND r_iconography_actor.role = 'publisher'
              JOIN actor
              ON r_iconography_actor.id_actor = actor.id
              AND actor.entry_name ILIKE ANY(ARRAY['%Aubert%', '%Martinet%']);
              """
            ]
            ,
            [ { "namedEntity": ['Martinet éditeur', 'Lecointe architecte'] },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              JOIN r_iconography_named_entity
              ON r_iconography_named_entity.id_iconography = iconography.id
              JOIN named_entity
              ON r_iconography_named_entity.id_named_entity = named_entity.id
              AND named_entity.entry_name IN ('Martinet éditeur', 'Lecointe architecte');
              """
            ]
            ,
            [ { "theme": ['mobilier urbain', 'actualité'] },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              JOIN r_iconography_theme
              ON r_iconography_theme.id_iconography = iconography.id
              JOIN theme
              ON r_iconography_theme.id_theme = theme.id
              AND theme.entry_name IN ('mobilier urbain', 'actualité');
              """
            ]
            ,
            [ { "institution": ["Bibliothèque nationale de France", "Paris Musées"] },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              JOIN r_institution
              ON r_institution.id_iconography = iconography.id
              JOIN institution
              ON r_institution.id_institution = institution.id
              AND institution.entry_name IN ('Bibliothèque nationale de France', 'Paris Musées');
              """
            ]
            ,
            [ { "date": [ { "data": [1815,1820], "filter": "dateRange"  },
                          { "data": [1826],      "filter": "dateExact"  },
                          { "data": [1800],      "filter": "dateBefore" },
                          { "data": [1900],      "filter": "dateAfter"  }
              ] },
              """
              SELECT iconography.id
              FROM iconography
              WHERE
                NOT isempty(iconography.date * '[1815,1821)'::int4range)
                OR iconography.date = '[1826,1827)'::int4range
                OR (NOT isempty(iconography.date) AND lower(iconography.date) <= 1800)
                OR (NOT isempty(iconography.date) AND upper(iconography.date) >= 1900);
              """
            ]
        ]

        with self.app.app_context():  # avoid RuntimeError
            for ( http_params, raw_sql ) in queries:
                r_http = self.client.post(route, json=http_params)
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
        test the combination of different params with AND, OR, NOT boolean operators.
        """
        route = "/i/iconography/search"
        queries = [
            # basic OR
            [ { "namedEntity"   : [ "Galerie Vivienne" ],
                "theme"         : [ "boutique" ],
                "themeBooleanOp": "or"
              },
              """
              SELECT iconography.id
              FROM iconography
              JOIN r_iconography_named_entity
              ON r_iconography_named_entity.id_iconography = iconography.id
              JOIN named_entity
              ON named_entity.id = r_iconography_named_entity.id_named_entity
              AND named_entity.entry_name IN ('Galerie Vivienne')
              UNION
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_iconography_theme
                ON r_iconography_theme.id_iconography = iconography.id
                JOIN theme
                ON theme.id = r_iconography_theme.id_theme
                AND theme.entry_name IN ('boutique')
              );
              """
            ]
            ,
            # basic AND
            [ { "theme"               : [ "boutique" ],
                "namedEntity"         : [ "Galerie Vivienne" ],
                "namedEntityBooleanOp": "not"
              },
              """
              SELECT iconography.id
              FROM iconography
              JOIN r_iconography_theme
              ON r_iconography_theme.id_iconography = iconography.id
              JOIN theme
              ON theme.id = r_iconography_theme.id_theme
              AND theme.entry_name IN ('boutique')
              WHERE iconography.id NOT IN
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_iconography_named_entity
                ON r_iconography_named_entity.id_iconography = iconography.id
                JOIN named_entity
                ON named_entity.id = r_iconography_named_entity.id_named_entity
                AND named_entity.entry_name IN ('Galerie Vivienne')
              );
              """
            ]
            ,
            # fancier query
            [ { "institution"          : [ "Bibliothèque historique de la Ville de Paris" ],
                "institutionBooleanOp" : "and",
                "theme"                : [ "actualité" ],
                "themeBooleanOp"       : "not",
                "namedEntity"          : [ "Franck photographe" ],
                "namedEntityBooleanOp" : "or",
                "date"                 : [ { "data": [1800,1850], "filter": "dateRange" } ]  # dateBooleanOp is implicit
              },
              """
              SELECT iconography.id
              FROM iconography
              JOIN r_institution ON r_institution.id_iconography = iconography.id
              JOIN institution ON institution.id = r_institution.id_institution
              AND institution.entry_name IN ('Bibliothèque historique de la Ville de Paris')
              WHERE iconography.date IS NOT NULL
              AND NOT isempty( iconography.date * '[1800,1851)'::int4range )
              AND iconography.id NOT IN
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_iconography_theme ON r_iconography_theme.id_iconography = iconography.id
                JOIN theme ON theme.id = r_iconography_theme.id_theme
                AND theme.entry_name IN ('actualité')
              )
              UNION
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_iconography_named_entity ON r_iconography_named_entity.id_iconography = iconography.id
                JOIN named_entity ON named_entity.id = r_iconography_named_entity.id_named_entity
                AND named_entity.entry_name IN ('Franck photographe')
              )
              """
            ]
            ,
            # another fancy query
            [ { "namedEntity"         : ["Agence Fournier"],
                "theme"               : ["architecture"],
                "themeBooleanOp"      : "or",
                "institution"         : ["Bibliothèques spécialisées de la Ville de Paris"],
                "institutionBooleanOp": "or"
              },
              r"""
              SELECT iconography.id FROM iconography
              JOIN r_iconography_named_entity ON iconography.id = r_iconography_named_entity.id_iconography
              JOIN named_entity ON named_entity.id = r_iconography_named_entity.id_named_entity
              AND named_entity.entry_name IN ('Agence Fournier')
              UNION
                ( SELECT iconography.id FROM iconography
                  JOIN r_iconography_theme ON iconography.id = r_iconography_theme.id_iconography
                  JOIN theme ON theme.id = r_iconography_theme.id_theme
                  AND theme.entry_name IN ('architecture')
                )
              UNION
                ( SELECT iconography.id FROM iconography
                  JOIN r_institution ON r_institution.id_iconography = iconography.id
                  JOIN institution ON r_institution.id_institution = institution.id
                  AND institution.entry_name IN ('Bibliothèques spécialisées de la Ville de Paris')
                );
              """
            ]
            ,
            # yet another fancy query
            [ { "author"              : ["henrard", "atget"],
                "date"                : [{ "filter": "dateAfter", "data": [1910] }],
                "theme"               : ["photographe", "architecture"],
                "institution"         : ["Bibliothèque nationale de France"],
                "institutionBooleanOp": "not"
              },
              r"""
              SELECT iconography.id
              FROM iconography
              JOIN r_iconography_actor
              ON r_iconography_actor.id_iconography = iconography.id
              AND r_iconography_actor.role = 'author'
              JOIN actor ON actor.id = r_iconography_actor.id_actor
              AND actor.entry_name ILIKE ANY(ARRAY['%atget%', '%henrard%'])
              JOIN r_iconography_theme ON r_iconography_theme.id_iconography = iconography.id
              JOIN theme ON theme.id = r_iconography_theme.id_theme
              AND theme.entry_name IN ('architecture', 'photographe')
              WHERE NOT isempty(iconography.date) AND upper(iconography.date) >= 1910
              AND iconography.id NOT IN
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_institution
                ON r_institution.id_iconography = iconography.id
                JOIN institution
                ON institution.id = r_institution.id_institution
                AND institution.entry_name IN ('Bibliothèque nationale de France')
              );
              """
            ]
            ,
            # query with only NOT boolean operators
            [ { "date"                 : [ {"data": [1800,1850], "filter": "dateRange"} ],
                "dateBooleanOp"        : "not",
                "institution"          : ["Paris Musées"],
                "institutionBooleanOp" : "not" },
              """
              SELECT iconography.id
              FROM iconography
              WHERE iconography.id NOT IN
              (
                SELECT iconography.id
                FROM iconography
                WHERE iconography.date IS NOT NULL
                AND  NOT isempty( iconography.date * '[1800,1851)'::int4range ))
              AND iconography.id NOT IN
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_institution ON r_institution.id_iconography = iconography.id
                JOIN institution ON r_institution.id_institution = institution.id
                AND institution.entry_name IN ('Paris Musées')
              );
              """
            ]
            ,
            # query with only OR boolean operators
            # this will test the transformation of the first "or" to an "and"
            [ { "institution"          : ["Paris Musées"],
                "institutionBooleanOp" : "or",
                "theme"                : ["mobilier urbain"],
                "themeBooleanOp"       : "or",
                "title"                : ["mode"],
                "titleBooleanOp"       : "or"
              },
              """
              SELECT DISTINCT iconography.id
              FROM iconography
              JOIN r_institution
              ON r_institution.id_iconography = iconography.id
              JOIN institution
              ON r_institution.id_institution = institution.id
              AND institution.entry_name IN ('Paris Musées')
              UNION
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_iconography_theme
                ON r_iconography_theme.id_iconography = iconography.id
                JOIN theme ON r_iconography_theme.id_theme = theme.id
                AND theme.entry_name IN ('mobilier urbain')
              )
              UNION
              (
                SELECT iconography.id
                FROM iconography
                JOIN title
                ON iconography.id = title.id_iconography
                AND title.entry_name ILIKE ANY(ARRAY['%mode%'])
              );
              """
            ]
        ]
        # the queries change but the tests are the same as in the previous function
        with self.app.app_context():  # avoid RuntimeError
            for ( http_params, raw_sql ) in queries:
                r_http = self.client.post(route, json=http_params)
                r_sql = self.db.session.execute(text(raw_sql))

                if r_http.status_code != 200:
                    print(f"\n\n{'~'*50}\n", r_http.get_data(True), f"\n{'~'*50}\n\n")
                    exit()

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


    def test_advanced_search_iconography_expected_problems(self):
        """
        test that expected problems happen: when passing invalid
        parameters, or invalid parameter values, we except an HTTP
        error to be raised.
        here, we don't need to check for raw SQL or anything.
        """
        route = "/i/iconography/search"

        # get on this route returns a 400
        with self.app.app_context():
            r = self.client.get(route)
            self.assertEqual(r.status_code, 400)

        # assert that all the below queries will raise errors
        queries = [ { "this should raise an error": "Dale Cooper" }    # unallowed parameter
                  , { "date": [1800,1900] }                            # date must be an array of { "filter": <str>, "data": t.List[int] }
                  , { "date": [{ "data": [1800],                       # type-wise this is ok, but with "dateRange", we need 2 dates
                                 "dateFilter": "dateRange" }] }
                  , { "date": [{ "data": [1800,1810],                  # type-wise this is ok, but with `filter != "dateRange"`, we need 1 dates
                                 "dateFilter": "dateExact" }] }
                  , { "title": "Le moniteur de la mode" }              # except for boolean ops, all parameters must be given as arrays
                  , { "title": ["Le moniteur de la mode"],             # here title is valid, but booleanops must be string, not t.List[str]
                      "titleBooleanOp": ["and"] }
        ]
        with self.app.app_context():
            for http_params in queries:
                r = self.client.post(route, json=http_params )
                if r.status_code != 500:
                    print(http_params)
                self.assertEqual(r.status_code, 500)
        return self