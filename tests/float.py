import unittest
import main
import re


class TestStringMethods(unittest.TestCase):

    def test(self):
        strings = [
            ('1.0', True),
            ('.00', False),
            ('asd.02', False),
            ('1.', False),
        ]
        for test_case in strings:
            print(test_case)
            self.assertEqual(
                bool(re.fullmatch(main.Patterns.float_pattern, test_case[0])), test_case[1])


if __name__ == '__main__':
    unittest.main()
