import unittest
import re

class RegexTest(unittest.TestCase):

    def test_search(self):
        regex = re.compile("\d")
        sentence = "more than 200 people"
        y = regex.search(sentence)

    def test_digits(self):
        regex = re.compile("(\d+)")
        sentence = "more than 200 people"
        matches = regex.findall(sentence)
        self.assertEqual(matches, ['200'])

    def test_boundaries(self):
        regex = re.compile(r"\b(\d+)\b")
        sentence = "more than 200 people"
        matches = regex.findall(sentence)
        self.assertEqual(matches, ['200'])

    def test_disjunction(self):
        regex = re.compile(r"(one|two|three)")
        sentence = "three apples and two pears"
        matches = regex.findall(sentence)
        self.assertEqual(matches, ['three', 'two'])

        regex2 = re.compile(r"\b(one|two|three)\b")
        matches = regex2.findall(sentence)
        self.assertEqual(matches, ['three', 'two'])


if __name__ == '__main__':
    unittest.main()
