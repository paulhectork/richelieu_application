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
-- title
SELECT DISTINCT iconography.id_uuid
FROM iconography
JOIN title
ON title.id_iconography = iconography.id
AND title.entry_name ILIKE ANY(ARRAY['%bourse%', '%théâtre%']);

-- author
SELECT DISTINCT(iconography.id_uuid)
FROM iconography
JOIN r_iconography_actor
ON r_iconography_actor.id_iconography = iconography.id
AND r_iconography_actor.role = 'author'
JOIN actor
ON r_iconography_actor.id_actor = actor.id
AND actor.entry_name ILIKE ANY(ARRAY['%daumier%', '%atget%']);

-- publisher
SELECT DISTINCT(iconography.id_uuid)
FROM iconography
JOIN r_iconography_actor
ON r_iconography_actor.id_iconography = iconography.id
AND r_iconography_actor.role = 'publisher'
JOIN actor
ON r_iconography_actor.id_actor = actor.id
AND actor.entry_name ILIKE ANY(ARRAY['%Aubert%', '%Martinet%']);

-- named entity
SELECT iconography.id_uuid, named_entity.entry_name
FROM iconography
JOIN r_iconography_named_entity
ON r_iconography_named_entity.id_iconography = iconography.id
JOIN named_entity
ON r_iconography_named_entity.id_named_entity = named_entity.id
AND named_entity.entry_name IN ('Martinet éditeur', 'Lecointe architecte');

-- theme
SELECT DISTINCT(iconography.id_uuid)
FROM iconography
JOIN r_iconography_theme
ON r_iconography_theme.id_iconography = iconography.id
JOIN theme
ON r_iconography_theme.id_theme = theme.id
AND theme.entry_name IN ('architecture', 'actualité');

-- institution
SELECT DISTINCT(iconography.id_uuid)
FROM iconography
JOIN r_institution
ON r_institution.id_iconography = iconography.id
JOIN institution
ON r_institution.id_institution = institution.id
AND institution.entry_name IN ('Bibliothèque nationale de France', 'Paris Musées');

-- date
SELECT * FROM iconography
WHERE
  NOT isempty(iconography.date * '[1815,1821)'::int4range)
  OR iconography.date = '[1826,1827)'::int4range
  OR (NOT isempty(iconography.date) AND lower(iconography.date) <= 1800)
  OR (NOT isempty(iconography.date) AND upper(iconography.date) >= 1900)
;

"""

"""
-- examples; could be used to write tests
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


-- theme OR named_entity
SELECT q1.id
FROM
  ( SELECT iconography.id FROM iconography
    JOIN r_iconography_named_entity ON iconography.id = r_iconography_named_entity.id_iconography
    JOIN named_entity ON named_entity.id = r_iconography_named_entity.id_named_entity
    AND named_entity.entry_name IN ('Agence Fournier')
  ) AS q1
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

-- BHVP, dating from 1800,1851
-- whose theme is not 'actualité'
-- or whose named entity is 'Franck photographe'
SELECT q1.id
FROM
(
  SELECT iconography.id
  FROM iconography
  JOIN r_institution ON r_institution.id_iconography = iconography.id
  JOIN institution ON institution.id = r_institution.id_institution
  AND institution.entry_name IN ('Bibliothèque historique de la Ville de Paris')
  WHERE NOT isempty( iconography.date * '[1800,1851)'::int4range )
) AS q1
WHERE
q1.id NOT IN
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

-- all pictures by Roger Henrard and Eugène Atget
-- dating from after 1910, with theme 'photographe' or 'architecture'
-- not conserved by the BnF.
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
  AND institution.entry_name IN ('Paris Musées')
)
;
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
            [ { "title": "galerie colbert, rue vivienne, 2ème arrondissement, paris" },
              r"""
              SELECT * FROM iconography
              JOIN title
              ON iconography.id = title.id_iconography
              AND title.entry_name ILIKE '%galerie colbert, rue vivienne, 2ème arrondissement, paris%';
              """
            ]
            ,
            [ { "author": "achille devéria" },
              r"""
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
              r"""
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
            [ { "theme": "mobilier urbain" },
              """
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
            [ { "namedEntity": "Palais-Royal" },
              """
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
            [ { "institution": "Musée Carnavalet" },
              """
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
            [ { "dateFilter": "dateRange", "date[]": [1800,1810] },
              """
              SELECT *
              FROM iconography
              WHERE NOT isempty( iconography.date * int4range(1800,1810+1) );
              """
            ]
            ,
            [ { "dateFilter": "dateExact", "date[]": [1829] },
              """
              SELECT *
              FROM iconography
              WHERE iconography.date = int4range(1829,1829+1);
              """
            ]
            ,
            [ { "dateFilter": "dateBefore", "date[]": [1829] },
              """
              SELECT *
              FROM iconography
              WHERE lower(iconography.date) <= 1829
              """
            ]
            ,
            [ { "dateFilter": "dateAfter", "date[]": [1829] },
              """
              SELECT *
              FROM iconography
              WHERE upper(iconography.date) >= 1829
              """
            ]
        ]

        with self.app.app_context():  # avoid RuntimeError
            for ( http_params, raw_sql ) in queries:
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
        in `/i/iconography/search` route
        """
        route = "/i/iconography/search"

        queries = [
            [ { "namedEntity": "Galerie Vivienne", "theme": "boutique" },
              """
              SELECT iconography.id_uuid
                     , iconography.date
                     , theme.entry_name AS theme
                     , named_entity.entry_name AS named_entity
              FROM iconography
              JOIN r_iconography_named_entity
              ON r_iconography_named_entity.id_iconography = iconography.id
              JOIN named_entity
              ON named_entity.id = r_iconography_named_entity.id_named_entity
              AND named_entity.entry_name = 'Galerie Vivienne'
              JOIN r_iconography_theme
              ON r_iconography_theme.id_iconography = iconography.id
              JOIN theme
              ON theme.id = r_iconography_theme.id_theme
              AND theme.entry_name = 'boutique';
              """
            ]
            ,
            [ { "author": "daumier", "dateFilter": "dateAfter", "date[]": [1855] },
              r"""
              SELECT iconography.date
              FROM iconography
              JOIN r_iconography_actor
              ON r_iconography_actor.id_iconography = iconography.id
              AND r_iconography_actor.role = 'author'
              JOIN actor
              ON actor.id = r_iconography_actor.id_actor
              AND actor.entry_name ILIKE '%daumier%'
              WHERE upper(iconography.date) >= 1855;
              """
            ]
            ,
            [ { "publisher": "martinet", "dateFilter": "dateExact", "date[]": [1833] },
              r"""
              SELECT *
              FROM iconography
              JOIN r_iconography_actor
              ON r_iconography_actor.id_iconography = iconography.id
              AND r_iconography_actor.role = 'publisher'
              JOIN actor
              ON actor.id = r_iconography_actor.id_actor
              AND actor.entry_name ILIKE '%martinet%'
              WHERE iconography.date = INT4RANGE(1833,1833+1);
              """
            ]
            ,
            [ { "theme": "édition", "dateFilter": "dateRange", "date[]": [1850,1860] },
              """
              SELECT theme.entry_name, iconography.date
              FROM theme
              JOIN r_iconography_theme
              ON r_iconography_theme.id_theme = theme.id
              AND theme.entry_name = 'édition'
              JOIN iconography
              ON r_iconography_theme.id_iconography = iconography.id
              AND iconography.date IS NOT NULL
              AND NOT isempty( iconography.date * INT4RANGE(1850,1861) )
              ORDER BY iconography.date DESC;
              """
            ]
        ]

        # the queries change but the tests are the same as in the previous function
        with self.app.app_context():  # avoid RuntimeError
            for ( http_params, raw_sql ) in queries:
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


    def test_advanced_search_iconography_expected_problems(self):
        """
        test that expected problems happen: when passing invalid
        parameters, or invalid parameter values, we except an HTTP
        error to be raised.
        here, we don't need to check for raw SQL or anything.
        """
        route = "/i/iconography/search"

        queries = [ { "this should raise an error": "Dale Cooper" }    # unallowed parameter
                  , { "date[]": [1800,1900] }                          # dateFilter is missing
                  , { "dateFilter": "dateExact", "date[]": ["aaaaa"] } # `date[]` must be an integer array
                  , { "dateFilter": "dateRange", "date[]": [1900] }    # with `dateRange`, we must have 2 values
        ]

        with self.app.app_context():
            for http_params in queries:
                r = self.client.get(route, query_string=http_params )
                self.assertEqual(r.status_code, 500)
        return self









