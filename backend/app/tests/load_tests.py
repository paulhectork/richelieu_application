import unittest

from .serializations import TestSerializations


def load_tests(loader=unittest.TestLoader(), tests=[], pattern=None):
    # array of test cases to run. could be completed with other test classes
    test_cases = [TestSerializations]
    # suite of tests that will be run
    suite = unittest.TestSuite()
    for t in test_cases:
        tests = loader.loadTestsFromTestCase(t)
        suite.addTests(tests)
    return suite
