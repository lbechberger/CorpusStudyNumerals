import unittest

from languages import English

class EnglishTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(EnglishTest, self).__init__(*args, **kwargs)
        self.en = English()

    def test_hundred(self):
        sentence = "With balls being struck at around 100 mph, injuries are part and parcel of the game -- and Hoog has experienced her fair share."
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [100])

    def test_thousands(self):
        sentence = "Your article can go from 100 views to 100,000 very quickly."
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [100, 100000])

    def test_number_at_beginning(self):
        sentence = "54321 people participated in the survey."
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [54321])


if __name__ == '__main__':
    unittest.main()
