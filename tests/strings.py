import unittest
from ... import main


class TestStringMethods(unittest.TestCase):

    def test(self):
        strings = [
            ('"this is string"', True),
            ('"open quote', False),
            ('close quote"', False),
            ('"12341"', True),
        ]
        for test_case in strings:
            self.assertEqual(main.is_string(test_case[0]), test_case[1])


if __name__ == '__main__':
    unittest.main()
