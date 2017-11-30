from __future__ import print_function

import sys
import locale

from counter import Counter


try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


class Processor:
    '''A Processor can process a single text file from a corpus.  It is
    initialized using a Language object, providing language specific
    knowledge for processing.

    The Processor can be customized to 
    '''

    n_low = 1
    n_high = 100

    _match_number_words_flag = True
    _show_progress_flag = True
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
        self._counter.reset()


    def processFile(self, inputStream):
        '''Process an input stream. This is the main function of
        this class. It will read the stream line by line,
        look for numerals, either provided as numbers, or
        in words, and count the occurences.

        Arguments
        ---------
        inputStream
            The input stream to read.
        '''
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
            self._counter(matches)

            if matches:
                num['matches'] += 1
                num['numbers'] += len(matches)


            # look for occurences of number words
            if self._match_number_words_flag:
                wordMatches = self.language.match_number_words(sentence)
                self._counter(wordMatches)

                if wordMatches:
                    num['words'] += len(wordMatches)


            # output progress information (if desired)
            if self._show_progress_flag and (num['lines'] % 100000 == 0):
                sys.stderr.write('.' if self.verbosity > 0 else
                                 r'{}\r'.format(num['lines']))
                sys.stderr.flush()
            num['lines'] += 1

        if self.verbosity > 0:
            print(" processed {0} lines.".
                  format(locale.format("%d", num['lines'], grouping=True)),
                  file=sys.stderr)
        elif self._show_progress_flag:
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
