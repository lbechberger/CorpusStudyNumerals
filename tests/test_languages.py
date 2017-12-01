import unittest

from languages import English, German

class EnglishTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(EnglishTest, self).__init__(*args, **kwargs)
        self.en = English()

    def test_numbwords(self):
        words = self.en.numberwords_range(1,3)
        self.assertEqual(words, ['one','two','three'])

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

    def test_number_at_end(self):
        sentence = "Latest figures (for February this year) show the local command to have 112 officers rostered, instead of the authorised 105."
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [112, 105])
    
    def test_parentheses(self):
        sentence = "Many people (200 to 300) attended the lecture."
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [200, 300])

    def test_quotation(self):
        sentence = 'Merkel said: "300 euros are not enough."'
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [300])
    
    def test_brackets(self):
        sentence = "Many people [200] attended the lecture."
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [200])
   
    def test_dollar_question_mark(self):
        sentence = "You only want $2?"
        matches = self.en.match_numbers(sentence)
        self.assertEqual(matches, [2])


class GermanTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GermanTest, self).__init__(*args, **kwargs)
        self.de = German()

    def test_numbwords(self):
        words = self.de.numberwords_range(1,3)
        self.assertEqual(words, ['eins','zwei','drei'])
    
if __name__ == '__main__':
    unittest.main()
