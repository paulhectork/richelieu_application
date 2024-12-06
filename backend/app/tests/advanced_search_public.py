"""
test the advanced search module using the public API
(route "/api/v1/search")

the batches of tests here test at the same time:
  - the route in `src/routes/api_public.py` (parameter sanitization and validation)
  - the advanced search module (`src/search/search_iconography.py`)
by running the same queries as raw sql and http get requests.
"""
import typing as t
import os

from sqlalchemy import text
import unittest

from ..app import app, db


class TestAdvancedSearchPublic(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.route = "/api/v1/search"
        self.app = app
        self.db = db
    def tearDown(self):
        self.client = None
        self.route = None
        self.app = None
        self.db = None

    def test_individual(self):
        """
        test the individual search params

        query arguments are written like they are expected to
        be received in the public api, and the raw SQL queries are
        written to mimic their SQLAlchemy equivalents (with ILIKE etc).
        """
        # queries is an array of [ <route params>, <raw sql query> ]
        queries = [
            [ { "title": "bourse,théâtre" },
              r"""
              SELECT DISTINCT iconography.id
              FROM iconography
              JOIN title
              ON title.id_iconography = iconography.id
              AND title.entry_name ILIKE ANY(ARRAY['%bourse%', '%théâtre%']);
              """
            ]
            ,
            [ { "author": "Daumier,atget" },
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
            [ { "publisher": "Aubert,Martinet" },
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
            #TODO so far, the separator is ",". it should be "\s*,\s*" or "\s*|\s*"
            # with a `.strip()` on individual values and this should be valid
            [ { "publisher": "Aubert, Martinet" },
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
            [ { "named_entity": 'Martinet Éditeur,Lecointe architecte' },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              JOIN r_iconography_named_entity
              ON r_iconography_named_entity.id_iconography = iconography.id
              JOIN named_entity
              ON r_iconography_named_entity.id_named_entity = named_entity.id
              AND named_entity.entry_name IN ('Martinet Éditeur', 'Lecointe architecte');
              """
            ]
            ,
            [ { "theme": 'mobilier urbain,actualité' },
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
            [ { "institution": "Bibliothèque nationale de France,Paris Musées" },
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
            [ { "date": "1826" },
              """
              SELECT iconography.id
              FROM iconography
              WHERE iconography.date = '[1826,1827)'::int4range
              """
            ]
            ,
            [ { "date": "1826" },
              """
              SELECT iconography.id
              FROM iconography
              WHERE iconography.date = '[1826,1827)'::int4range
              """
            ]
            ,
            [ { "date": "1815,1820" },
              """
              SELECT iconography.id
              FROM iconography
              WHERE NOT isempty(iconography.date * '[1815,1821)'::int4range)
              """
            ]
        ]
        tester_all_good(self, queries)
        return

    def test_combined(self):
        """
        test the combination of different params with AND, OR, NOT boolean operators.
        """
        queries = [
            # basic AND
            [ { "named_entity"     : "Galerie Vivienne",
                "theme"            : "commerce",
                "theme_boolean_op" : "and"
              },
              """
              SELECT iconography.id
              FROM iconography
              JOIN r_iconography_named_entity
              ON r_iconography_named_entity.id_iconography = iconography.id
              JOIN named_entity
              ON named_entity.id = r_iconography_named_entity.id_named_entity
              AND named_entity.entry_name IN ('Galerie Vivienne')
              AND iconography.id IN
              (
                SELECT iconography.id
                FROM iconography
                JOIN r_iconography_theme
                ON r_iconography_theme.id_iconography = iconography.id
                JOIN theme
                ON theme.id = r_iconography_theme.id_theme
                AND theme.entry_name IN ('commerce')
              );
              """
            ]
            ,
            # basic OR
            [ { "named_entity"     : "Galerie Vivienne",
                "theme"            : "boutique",
                "theme_boolean_op" : "or"
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
            #TODO `NOT` is not yet allowed as a boolean_op in the public api.
            # basic NOT
            [ { "theme"                  : "boutique",
                "named_entity"           : "Galerie Vivienne",
                "named_entity_boolean_op": "not"
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
            # chaining `and`s
            [ { "theme"            : "commerce",
                "theme_boolean_op" : "and",
                "title"            : "galerie",
                "title_boolean_op" : "and",
                "author"           : "atget",
                "author_boolean_op": "and"  },
              r"""
              SELECT DISTINCT iconography.id_uuid
              FROM iconography
              WHERE iconography.id_uuid IN (
                SELECT iconography.id_uuid
                FROM iconography
                JOIN r_iconography_theme
                ON r_iconography_theme.id_iconography = iconography.id
                JOIN theme
                ON r_iconography_theme.id_theme = theme.id
                AND theme.entry_name IN ('commerce')
              ) AND iconography.id_uuid IN (
                  SELECT DISTINCT iconography.id_uuid
                  FROM iconography
                  JOIN r_iconography_actor
                  ON r_iconography_actor.id_iconography = iconography.id
                  AND r_iconography_actor.role = 'author'
                  JOIN actor
                  ON r_iconography_actor.id_actor = actor.id
                  AND actor.entry_name ILIKE ANY(ARRAY['%atget%'])
              ) AND iconography.id_uuid IN (
                  SELECT DISTINCT iconography.id_uuid
                  FROM iconography
                  JOIN title
                  ON title.id_iconography = iconography.id
                  AND title.entry_name ILIKE ANY(ARRAY['%galerie%'])
              );"""
            ]
            ,
            #TODO: "NOT" is not yet allowed in the public api.
            # fancier query
            [ { "institution"             : "Bibliothèque historique de la Ville de Paris",
                "institution_boolean_op"  : "and",
                "theme"                   : "actualité",
                "theme_boolean_op"        : "not",
                "named_entity"            : "Franck photographe",
                "named_entity_boolean_op" : "or",
                "date"                    : "1800,1850"  # dateBooleanOp is implicit
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
            [ { "named_entity"          : "Agence Fournier",
                "theme"                 : "architecture",
                "theme_boolean_op"      : "or",
                "institution"           : "Bibliothèques spécialisées de la Ville de Paris",
                "institution_boolean_op": "or"
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
            #TODO: "NOT" is not yet allowed in the public api.
            # query with only NOT boolean operators
            [ { "date"                 : "1800,1850",
                "date_boolean_op"        : "not",
                "institution"          : "Paris Musées",
                "institution_boolean_op" : "not" },
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
            [ { "institution"           : "Paris Musées",
                "institution_boolean_op": "or",
                "theme"                 : "mobilier urbain",
                "theme_boolean_op"      : "or",
                "title"                 : "mode",
                "title_boolean_op"      : "or"
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
        tester_all_good(self, queries)
        return self

    def test_expected_problems(self):
        """
        test that expected problems happen: when passing invalid
        parameters, or invalid parameter values, we except an HTTP
        error to be raised.
        here, we don't need to check for raw SQL or anything.
        """
        # assert that all the below queries will raise errors
        queries = [ { "this should raise an error": "Dale Cooper" }    # unallowed parameter
                  , { "date": [1800,1900] }                            # date must be a string matching "\d{4},(\d{4})?"
                  , { "date": "1800,1801,1900" }                       # same. here, 3 dates are given
                  , { "date": "xyz" }                                  # same. this can't be retyped to string
                  , { "title": ["Le moniteur de la mode"] }            # in the public api, all parameters are strings
                  , { "title": "Le moniteur de la mode",               # here title is valid, but the boolean op is not.
                      "titleBooleanOp": "what are you trying to accomplish here ? " }
        ]
        http_codes = []
        with self.app.app_context():
            for http_params in queries:
                r = self.client.post(self.route, query_string=http_params )
                http_codes.append(r.status_code)
                self.assertTrue( int(r.status_code) >= 299
                               , f"expected HTTP code to be 400+ or 500+, instead got `{r.status_code}` with params `{http_params}`" )
        print("TestAdvancedSearchPublic.test_expected_problems(): all status codes : ", set(http_codes))
        return self


def tester_all_good( ctx: TestAdvancedSearchPublic
                   , _queries: t.List[ t.Dict|str ]):
    """
    this function does the actual testing in some functions
    of `TestAdvancedSearchPublic` that need the same test being done
    but using different data (in `_queries`).

    :param ctx: the context: our test case class defined above
    :param _queries: an array of [ <json_params>, <sql_query> ]
        both json and sql describing the same query (one in route params,
        the other in raw sql).
    """
    with ctx.app.app_context():
        for ( http_params, raw_sql ) in _queries:
            r_http = ctx.client.get(ctx.route, query_string=http_params)
            r_sql = ctx.db.session.execute(text(raw_sql))

            if r_http.status_code != 200:  # debug message
                mul = 150 # os.terminal_size().columns
                print( f"\n\n{ '*' * mul }\n"
                     , r_http.get_data(True)
                     , f"\n{ '*' * mul }\n"
                     , "with params : ", http_params
                     , f"\n{ '*' * mul }\n\n")

            r_http_count = len(r_http.json)
            r_sql_count = r_sql.rowcount

            # http request success
            ctx.assertEqual(r_http.status_code, 200
                           , f"expected HTTP status `200`, got `{r_http.status_code}` "
                           + f"with params `{str(http_params)}`" )
            # same number of rows in both results
            ctx.assertEqual( r_http_count, r_sql_count
                            , f"a different number of results was returned "
                            + f"by HTTP ({r_http_count}) and SQL ({r_sql_count}) for params {http_params}")
            # both queries returned at least 1 row
            ctx.assertTrue( r_http_count > 0 and r_sql_count > 0
                           , f"queries must return at least 1 result, "
                           + f"got {r_http_count} (HTTP) and {r_sql_count} (SQL) for params {http_params}"  )
    return ctx




