# -*- coding: utf-8 -*-

import re

#from text2num import text2num
# text2num has to be downloaded and in the same dir as the rest of the code

# num2words supports a wide range of languages, a list can be
# found on the webpage:
#   https://pypi.python.org/pypi/num2words
import num2words

# digify is an updated version of "text2num".
# I currently only supports british and american english
import digify




class Language:
    '''A base class representing a language. Derived classes may
    provide language specific implementations.

    '''


    '''A list of all available languages.'''
    languages = {
        'en' : 'English',
        'de' : 'German'
    }


    @classmethod
    def create(cls,language):
        '''A convenience function to instantiate a language from a
        two-letter language shortcut (e.g. "en")

        Arguments
        ---------
        language : str
            The two-letter language shortcut.

        Returns
        -------
        Language : a newly create language object.

        Throws
        ------
        LookupError : if the given language shortcut is not supported.
        '''
        className = cls.languages[language]
        classObject =  globals()[className]
        return classObject()


    def __init__(self):
        '''Language constructor. Compile some language specific regular
        expressions.
        '''

        # We need a prefix here to avoid some bad things from happening
        # FIXME[question]: but what bad things? provide examples, provide tests!
        prefix = r'(?:^|[ \-\$"\[\(])' # this is ugly!
        number = '(\d+(?:\{0}\d\d\d)*)'.format(self.thousandsSeparator)
        postfix = '[ \.,\!\?:\-€;\]\)"]'
        self._numbers_regex = re.compile(prefix + number + postfix, re.M)


    def precompile_numberwords(self,min,max):
        '''Prepare a regular expression that can be used to
        search for number words.

        Arguments
        ---------
        min,max: int
                The minimal and maximal number to be matched.
        '''
        words = self.numberwords_range(min,max)
        regex = r"\b(" + "|".join(words)+ r")\b"
        self._number_words_regex = re.compile(words)     


    def numberwords_range(self, min, max):
        '''Generate a list of number words.
        
        Arguments
        ---------
        min, max: int
            The minimal and maximal number to include.

        Result
        ------
        list of str
            The list of numberwords.
        '''
        return [w for w in self.numberWords
                if min <= self.numberWords[w] <= max]


    def convert_numberword(self, numberword):
        '''Convert a number word in the corresponding integer number.

        Arguments
        ---------
        number : str
            The spelled number to convert.

        Result
        ------
        int
            The corresponding integer.

        Raises
        ------
        NumberException
            The number word was not understood.
        '''
        if numberword in self.numberWords:
            return self.numberWords.get[numberword]
        raise NumberException("Unrecognized number word: {}".format(numberword))


    def match_numbers(self, line):
        '''Match numbers (written as digits) in a given line.

        Arguments
        ---------
        line: str
            A line of text.
 
        Result
        ------
        A list of integers, corresponding to the numbers found in the line.
        '''

        matches = self._numbers_regex.findall(line)
        numbers = []
        for match in matches:
            text = match.replace(self.thousandsSeparator, "")
            numbers.append(int(text))
        
        return numbers

    
    def match_number_words(self, line):
        '''Match numbers (written as words) in a given line.

        Arguments
        ---------
        line: str
            A line of text.

        Result
        ------
        A list of integers, corresponding to the numbers found in the line.
        '''

        matches = self._number_words_regex.findall(line)
        numbers = []
        for match in matches:
            try:
                numbers.append(self.convert_numberword(match))
            except NumberException:
                pass # we just ignore number words we don't understand ...
        return numbers



class English(Language):

    decimalSeparator = "."
    thousandsSeparator = ","

    # old - not used anymore but kept as a backup (in case we want to
    # go without num2words/digify)
    numberWords = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'twenty': 20,
        'thirty': 30,
        'fourty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90,
        'hundred': 100,
        'thousand': 1000
    }


    _use_num2words_flag = True
    
    def numberwords_range(self, min, max):
        '''Generate a list of number words.
        
        Arguments
        ---------
        min, max: int
            The minimal and maximal number to include.

        Result
        ------
        list of str
            The list of numberwords.
        '''
        return [num2words.num2words(i,lang='en') for i in range(min,max+1)] \
            if self._use_num2words_flag \
            else super(English, self).numberwords_range(min,max)


    def convert_numberword(self, numberword):
        '''Convert a number word in the corresponding integer number.

        Arguments
        ---------
        numberword : str
            The spelled number to convert.

        Result
        ------
        int
            The corresponding integer.

        Raises
        ------
        ValueError
            The number word was not understood.
        '''
        return digify.spelled_num_to_digits(numberword)



class German(Language):

    decimalSeparator = ","
    thousandsSeparator = "."

    numberWords = {
        'null': 0,
        'eins': 1,
        'zwei': 2,
        'drei': 3,
        'vier': 4,
        'fünf': 5,
        'sechs': 6,
        'sieben': 7,
        'acht': 8,
        'neun': 9,
        'zehn': 10,
        'elf': 11,
        'zwölf': 12,
        'zwanzig': 20,
        'dreißig': 30,
        'vierzig': 40,
        'fünfzig': 50,
        'sechzig': 60,
        'siebzig': 70,
        'achtzig': 80,
        'neunzig': 90,
        'hundert': 100,
        'tausend': 1000
    }


