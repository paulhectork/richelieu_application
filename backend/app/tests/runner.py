import unittest

from .serializations import TestSerializations
from .advanced_search_internal import TestAdvancedSearchInternal


def load_tests( loader=unittest.TestLoader()
              , tests=[]
              , pattern=None ) -> unittest.TestSuite:
    """
    load all the tests we'll need to run
    """
    # array of test cases to run. could be completed with other test classes
    test_cases = [TestSerializations, TestAdvancedSearchInternal]
    # suite of tests that will be run
    suite = unittest.TestSuite()
    for t in test_cases:
        tests = loader.loadTestsFromTestCase(t)
        suite.addTests(tests)
    return suite


def runner() -> None:
    """
    run the tests
    """
    textrunner = unittest.TextTestRunner()
    suite = load_tests()
    textrunner.run(suite)
    return