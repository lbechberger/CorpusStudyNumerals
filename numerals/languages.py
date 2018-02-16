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


    def precompile_regex(self,min,max):
        '''Language constructor. Compile some language specific regular
        expressions.
        (1) regular expression searching for numbers
        (2) Prepare a regular expression that can be used to
        search for number words.

        Arguments
        ---------
        min,max: int
                The minimal and maximal number to be matched.
        '''
        
        _numbers_pattern = r'\b(?P<number>\d+(?:\{0}\d\d\d)*(?:\.\d+)?)\b'.format(self.thousandsSeparator)
        # [p] changed regex to include word before and after number!

        words = self.numberwords_range(min,max) # uses method below to return list of numberwords
        _numberwords_pattern = r'(?i)' + r'\b(?P<numword>' + '|'.join(words)+ r')\b'
        
        prec_approx = ['exactly', 'precisely', 'to be precise']
        impr_approx = ['about', 'approximately', 'roughly', 'around', 'or so', 'round about', 'roughly around', 'some']
        asym_approx = ['more than', 'nearly', 'over', 'almost', 'below', 'above', 'fewer than', 'less than', 'at most', 'at least', 'close to', 'near to', 'up to', 'as high as', 'as low as', 'not quite', ]
        _prec_approx_pattern = r'(?P<precise>' + '|'.join(prec_approx) + r')'
        _impr_approx_pattern = r'(?P<imprecise>' + '|'.join(impr_approx) + r')'
        _asym_approx_pattern = r'(?P<asymmetr>' + '|'.join(asym_approx) + r')'
        _approx_pattern = r'(?P<approximator>' + _prec_approx_pattern  + '|' + _impr_approx_pattern + _asym_approx_pattern + r')?'
        
        _numeral_pattern = '(' + _numbers_pattern + '|' + _numberwords_pattern + ')(?! (hundred|thousand|million|billion|bn))'
        
        _unit_pattern = r' ?(?P<unit>[^\s]+)'
        
        self._complex_regex = re.compile(_approx_pattern + ' ' + _numeral_pattern + _unit_pattern + r'\b')    


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

        
    def match_expression(self, line):
        '''
        (1) Match numbers (written as digits) in a given line.
        (2) Match numbers (written as words) in a given line.

        Arguments
        ---------
        line: str
            A line of text.
 
        Result
        ------
        (1) A list of integers, corresponding to the numbers found in the line.
        (2) A list of integers, corresponding to the numberwords found in the line. 
        (3) a list of counts for approximator-numeral combinations
        '''
        match_objects = []
        numbers = []
        numberwords = []
        prec_round = 0
        prec_nonr = 0
        impr_round = 0
        impr_nonr = 0
        null_round = 0
        null_nonr = 0
        
        m_o_iterator = self._complex_regex.finditer(line)
        
        for m_o in m_o_iterator:
            match_objects.append(m_o)
        
        for m in match_objects:
            try:
                with open(r'C:\Users\P-geg\Desktop\Thesis\stats\all_matches.txt', 'a') as matches: # [p] look into environment
                    matches.write(str(m.group(0))+"\n") # instead of m.groups()
            except UnicodeEncodeError:
                print("couldn't be written to file:",m.groups())
            
            if m.group('number'):
                numberstring = m.group('number').replace(self.thousandsSeparator, "")
                try:
                    numbers.append(int(numberstring))
                
                    if (not int(numberstring)%5):
                        if m.group('precise'):
                            prec_round += 1
                            with open(r'C:\Users\P-geg\Desktop\Thesis\stats\num_round_prec.txt', 'a') as nrp:
                                nrp.write(m.group(0).casefold()+"\n")
                        elif m.group('imprecise'):
                            impr_round += 1
                            with open(r'C:\Users\P-geg\Desktop\Thesis\stats\num_round_impr.txt', 'a') as nri:
                                nri.write(m.group(0).casefold()+"\n")
                        elif m.group('approximator') == None:
                            null_round += 1
                            with open(r'C:\Users\P-geg\Desktop\Thesis\stats\num_round_null.txt', 'a') as nrn:
                                nrn.write(m.group(0).casefold()+"\n")
                        else: print("Something's weird here! Seems no approximator matched @ round numbers:",m.group(0))
                    elif int(numberstring)%5:
                        if m.group('precise'):
                            prec_nonr += 1
                            with open(r'C:\Users\P-geg\Desktop\Thesis\stats\num_nonr_prec.txt', 'a') as nnp:
                                nnp.write(m.group(0).casefold()+"\n")
                        elif m.group('imprecise'):
                            impr_nonr += 1
                            with open(r'C:\Users\P-geg\Desktop\Thesis\stats\num_nonr_impr.txt', 'a') as nni:
                                nni.write(m.group(0).casefold()+"\n")
                        elif m.group('approximator') == None:
                            null_nonr += 1
                            with open(r'C:\Users\P-geg\Desktop\Thesis\stats\num_nonr_null.txt', 'a') as nnn:
                                nnn.write(m.group(0).casefold()+"\n")
                        else: print("Something's weird here! Couldn't be matched w/ any approximator @ nonround numbers:",m.group(0))
                    else: print("A problem with the number has occurred - seems neither round nor nonround:",m.group(0))
                except ValueError:
                    print('Number seems to be no int:',m.group(0))
            elif m.group('numword'):
                #if type(digify.spelled_num_to_digits(m.group('unit'))) == int: # [p] AUSPROBIEREN OB DAS FUNKTIONIERT!
                    #pass
                try:
                    numberwords.append(self.convert_numberword(m.group('numword')))
                except NumberException:
                    print("couldn't convert numberword:",m.group('numword'))
                    
                if not digify.spelled_num_to_digits(m.group('numword'))%5:
                    if m.group('precise'):
                        prec_round += 1
                        with open(r'C:\Users\P-geg\Desktop\Thesis\stats\word_round_prec.txt', 'a') as wrp:
                            wrp.write(m.group(0).casefold()+"\n")
                    elif m.group('imprecise'):
                        impr_round += 1
                        with open(r'C:\Users\P-geg\Desktop\Thesis\stats\word_round_impr.txt', 'a') as wri:
                            wri.write(m.group(0).casefold()+"\n")
                    elif m.group('approximator') == None:
                        null_round += 1
                        with open(r'C:\Users\P-geg\Desktop\Thesis\stats\word_round_null.txt', 'a') as wrn:
                            wrn.write(m.group(0).casefold()+"\n")
                    else: print("Something's weird here! Couldn't be matched w/ any approximator @ round numwords:",m.group(0))
                elif digify.spelled_num_to_digits(m.group('numword'))%5:
                    if m.group('precise'):
                        prec_nonr += 1
                        with open(r'C:\Users\P-geg\Desktop\Thesis\stats\word_nonr_prec.txt', 'a') as wnp:
                            wnp.write(m.group(0).casefold()+"\n")
                    elif m.group('imprecise'):
                        impr_nonr += 1
                        with open(r'C:\Users\P-geg\Desktop\Thesis\stats\word_nonr_impr.txt', 'a') as wni:
                            wni.write(m.group(0).casefold()+"\n")
                    elif m.group('approximator') == None:
                        null_nonr += 1
                        with open(r'C:\Users\P-geg\Desktop\Thesis\stats\word_nonr_null.txt', 'a') as wnn:
                            wnn.write(m.group(0).casefold()+"\n")
                    else: print("Something's weird here! Couldn't be matched w/ any approximator @ nonround numwords:",m.group(0))
                else: print("A problem with the numberword has occurred - seems neither round nor nonround:",m.group(0))
            else: print("Expression has not been processed because neither int number nor numberword:",m.group(0)) 
               
        return [numbers,numberwords,(prec_round, prec_nonr, impr_round, impr_nonr, null_round, null_nonr)]



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
    
    # make sure that WordNet is available
    try:
        from nltk.corpus import wordnet as wn
        wn.synsets('dog') # try to use wordnet to see if it works
        #TODO only works if ~/nltk_data/corpora/wordnet/ exists and contains all files --> script!
    except Exception:
        wn = None
    
    def is_in_category(self, word, category):
        '''Checks whether 'word' is in 'category' according to the wordNet hierarchy.'''
        # NLTK wordnet tutorial: http://www.nltk.org/howto/wordnet.html
        if self.wn != None:
            word_synsets = self.wn.synsets(word)
            category_synsets = self.wn.synsets(category)
            for w in word_synsets:
                # for each word sense: get its recursive hierarchy of hypernyms
                closure = w.closure(lambda s: s.hypernyms())
                for c in category_synsets:
                    if c in closure:
                        # if any of the category synsets is in this list: bingo!
                        return True
            return False
        else:
            return False
    
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
        return [num2words.num2words(i,lang='en') for i in range(max,min-1, -1)] \
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

    # TODO: use https://github.com/wroberts/pygermanet ?
