import unittest
from factorize import factorize

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        '''
        Check that if argument passed to function is float or str
        then it raise TypeError.

        with subTest
        Test variables: "string", "1.5".
        '''
        cases = ["string", 1.5]
        for case in cases:
            with self.subTest(case=case):
                self.assertRaises(TypeError, factorize, case)

    def test_negative(self):

        '''
        Check that if argument passed to function is negative number
        then it raise TypeError.

        with subTest
        Test variables: "-1", "-10", "-100"
        '''
        cases = [-1, -10, -100]
        for case in cases:
            with self.subTest(case=case):
                self.assertRaises(ValueError, factorize, case)

    def test_zero_and_one_cases(self):

        '''
        Check that if argument passed to function is 0 or 1
        then the results will be (0, ) and (1, )
        '''
        cases = [0, 1]
        answers = [(0, ), (1, )]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                self.assertEqual(factorize(cases[i]), answers[i])

    def test_simple_numbers(self):

        '''
        Tests: 3 -> (3,), 13 -> (13,), 29 -> (29,)
        '''
        cases = [3, 13, 29]
        answers = [(3,), (13,), (29, )]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                self.assertEqual(factorize(cases[i]), answers[i])

    def test_two_simple_multipliers(self):

        '''
        Chech arguments when function should return cortege with two elements (x, y).
        Tests:  6 → (2, 3),   26 → (2, 13),   121 -> (11, 11).
        '''
        cases = [6, 26, 121]
        answers = [(2, 3), (2, 13), (11, 11)]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                self.assertEqual(factorize(cases[i]), answers[i])

    def test_many_multipliers(self):

        '''
        Chech arguments when function should return cortege with
        more than two elements (x, y, z, ...).
        Tests:  1001 → (7, 11, 13) ,   9699690 → (2, 3, 5, 7, 11, 13, 17, 19).
        '''
        cases = [1001, 9699690]
        answers = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for i in range(len(cases)):
            with self.subTest(case=cases[i]):
                self.assertEqual(factorize(cases[i]), answers[i])

if __name__ == "__main__":
    unittest.main()
