from __future__ import print_function

import sys
import locale

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
    
    showProgressBar = True
    verbosity = 1
    
    counts = {}

    def __init__(self, language):
        '''Create a new Processor.

        Arguments
        ---------
        language : Language
        '''
        self.language = language


    def setLimits(self, low, high):
        '''Set the limits.
        The limits specify the range of interest, i.e. the smallest
        and largest number we are interested in.

        Arguments
        ---------
        low : int
        high : int
        '''
        self.n_low = low
        self.n_high = high


    def reset(self):
        '''Reset this processor.
        Resetting will only affect the counters, but not the
        configuration (range of interest, verbosity, etc.).
        '''
        self.counts = {}


    def processFile(self, inputStream):
        num = {'lines': 0, 'matches': 0, 'numbers': 0, 'words': 0}
        
        if self.verbosity > 0:
            sys.stderr.write("Starting to process ")

        for line in inputStream:
            # manually remove everything before the tabulator
            sentence = line.split("\t")[1]

            # look for ALL occurences of numbers
            matches = self.language.regex.findall(sentence)
            if matches:
                num['matches'] += 1
                num['numbers'] += len(matches)

            wordMatches = self.language.words.findall(sentence)
            if wordMatches:
                num['words'] += len(wordMatches)

            for match in matches:
                text = match.replace(self.language.thousandsSeparator, "")
                number = int(text)

                if number >= self.n_low and number <= self.n_high:
                    # not yet in dictionary: new entry
                    if not number in self.counts:
                        self.counts[number] = 1
                    else:
                        # already in dictionary: increase
                        self.counts[number] += 1
           
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
                  format(locale.format("%d", sum(self.counts.values()),
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
            values = list(map(lambda x: self.counts[x] if x in self.counts else 0,
                              numbers))
            plt.bar(numbers, values)
            plt.show()


    def getCounts(self):
        '''Provide the counters.

        Returns
        -------
        dict : a dictionary holding as keys the numbers found in during
        processing and the corresponding counter as value.
        '''
        return self.counts
