from __future__ import print_function

import sys
import locale
import re # [p]

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

class Counter:
    '''The Counter class is a collection of individual counters.  It is
    intended to count the occurences of numerals (integers), but it
    may also be used to count other things.

    '''
    
    _min_value = 0
    _max_value = 1
    _counters = {}

    def __init__(self, min=0, max=100):
        '''Create a new counter.

        Arguments
        ---------
        min : int
            The minimal value to count. All smaller values will be ignored.
        max : int
            The maximal value to count. All larger values will be ignored.
        '''
        self._max_value = max
        self.reset()
        
    def __call__(self, number):
        if number >= self._min_value and number <= self._max_value:
            # not yet in dictionary: new entry
            if not number in self._counters:
                self._counters[number] = 1
            else:
                # already in dictionary: increase
                self._counters[number] += 1


    def __getitem__(self, number):
        return self._counters[number] if number in self._counters else 0

    def sum(self):
        '''Get the sum of all element counters.

        Result
        ------
        The sum of all element counters.
        '''
        return sum(self._counters.values())
    
    def reset(self):
        '''Reset this counter object.
        This will just set all counters to 0
        but will keep all other parameters.
        '''
        self._counters = {}

class Processor:
    '''A Processor can process a single text file from a corpus.  It is
    initialized using a Language object, providing language specific
    knowledge for processing.

    The Processor can be customized to 
    '''

    n_low = 1
    n_high = 100

    _match_number_words_flag = True
    showProgressBar = True
    verbosity = 1

    _counter = None


    def __init__(self, language, min=0, max=100):
        '''Create a new Processor.

        Arguments
        ---------
        language : Language
        min : int
            The minimal value to count. All smaller values will be ignored.
        max : int
            The maximal value to count. All larger values will be ignored.
        '''
        self.language = language
        self._counter = Counter(min=min, max=max)

        if self._match_number_words_flag:
            self.language.precompile_numberwords(min,max)


    def reset(self):
        '''Reset this processor.
        Resetting will only affect the counters, but not the
        configuration (range of interest, verbosity, etc.).
        '''
        self._counter = Counter()


    def processFile(self, inputStream):
        num = {'lines': 0, 'matches': 0, 'numbers': 0, 'words': 0}
        
        if self.verbosity > 0:
            sys.stderr.write("Starting to process ")

        for sentence in inputStream:

            # Remove everything before the first tabulator.
            # This is relevant for lines from the "Wortschatz" corpus,
            # as these lines have the format running_number-TAB-sentence.
            if "\t" in sentence:
                sentence = sentence.split("\t")[1]

            # look for ALL occurences of numbers (digits)
            matches = self.language.match_numbers(sentence)
            if matches:
                num['matches'] += 1
                num['numbers'] += len(matches)

            for number in matches:
                self._counter(number)


            # look for occurences of number words
            if self._match_number_words_flag:
                wordMatches = self.language.match_number_words(sentence)

                if wordMatches:
                    num['words'] += len(wordMatches)

                for number in wordMatches:
                    self._counter(number)


            if self.showProgressBar and (num['lines'] % 100000 == 0):
                sys.stderr.write('.' if self.verbosity > 0 else
                                 r'{}\r'.format(num['lines']))
                sys.stderr.flush()
            num['lines'] += 1

        if self.verbosity > 0:
            print(" processed {0} lines.".
                  format(locale.format("%d", num['lines'], grouping=True)),
                  file=sys.stderr)
        elif self.showProgressBar:
            print(file=sys.stderr)

        if self.verbosity > 1:
            print("Some statistics:")
            print(" * {0} of these lines ({1}%) contain numbers".
                  format(locale.format("%d", num['matches'], grouping=True),
                         num['matches']*100//num['lines'] if num['lines'] > 0 else 100))
            print(" * in total we found {0} numbers".
                  format(locale.format("%d", num['numbers'], grouping=True)))
            print(" * {0} of these numbers are in the range of interest ({1}-{2})".
                  format(locale.format("%d", self._counter.sum(),
                                       grouping=True),
                         self.n_low,self.n_high))
            print(" * there were also {0} occurences of number words (not used yet!)".
                  format(locale.format("%d", num['words'], grouping=True)))


    def plotBars(self):
        '''Plot a bar chart.
        '''

        if plt is None:
            print("error: no matplotlib seems to be installed. Install it before trying to plot.", file=sys.stderr)
            print("info: matplotlib is available for free from https://matplotlib.org/", file=sys.stderr)
        else:
            numbers = range(self.n_low, self.n_high + 1)
            values = list(map(lambda x: self._counter[x], numbers))
            plt.bar(numbers, values)
            plt.show()


    # FIXME[question]: seems not to be used? If so, just remove ...
    def getCounts(self):
        '''Provide the counters.

        Returns
        -------
        dict : a dictionary holding as keys the numbers found in during
        processing and the corresponding counter as value.
        '''
        return self._counter._counters # FIXME[hack]
