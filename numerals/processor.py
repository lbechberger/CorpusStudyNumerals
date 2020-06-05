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

        # if self._match_number_words_flag:
            # self.language.precompile_numberwords(min,max)
        self.language.precompile_regex(min,max)


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
        nums = (self.n_high+1)*[0] # [p] initialise number count
        numwords = (self.n_high+1)*[0] # [p] initialise numberword count
        asym = 0
        tripleMatches = [0,0,0,0,0,0,0,0,0,0,0,0] # [p] initialise triple count
        unit_info = {}
        
        if self.verbosity > 0:
            sys.stderr.write("Starting to process ")

        for sentence in inputStream:

            # Remove everything before the first tabulator.
            # This is relevant for lines from the "Wortschatz" corpus,
            # as these lines have the format running_number-TAB-sentence.
            if "\t" in sentence:
                sentence = sentence.split("\t")[1]

            # look for ALL occurences of numbers (digits)
            info = self.language.match_expression(sentence)
            self._counter(info[0]) # occurrences of numbers
            self._counter(info[1]) # occurrences of numberwords

            if info[0]:
                num['matches'] += 1 # increase if at least one match is found in line
                num['numbers'] += len(info[0])
                for i in info[0]: # [p]
                    if i in range(len(nums)):
                        nums[i] += 1
            if info[1]: # look for occurences of number words
                num['words'] += len(info[1])
                for i in info[1]: #[p]
                    if i in range(len(numwords)):
                        numwords[i] += 1

            # look for occurences of number words
            # if self._match_number_words_flag:
                # wordMatches = self.language.match_number_words(sentence)
                # self._counter(wordMatches)

                # if wordMatches:
                    # num['words'] += len(wordMatches)
                    # for i in wordMatches: #[p]
                        # if i in range(len(numwords)):
                            # numwords[i] += 1
                    
            
            # [p]
            tripleMatches = [tripleMatches[i]+info[2][i] for i in range(len(tripleMatches))]
            
            asym += info[3] # count modified numerals besides imprecise/precise approximators
            
            for key in info[4]:
                if not key in unit_info:
                    unit_info[key] = info[4][key]
                else: unit_info[key] += info[4][key]
            
            # output progress information (if desired)
            if self._show_progress_flag and (num['lines'] % 100000 == 0):
                sys.stderr.write('.' if self.verbosity > 0 else
                                 r'{}\r'.format(num['lines']))
                sys.stderr.flush()
            num['lines'] += 1
        
        #sort unit counts in descending order
        unit_list = []
            
        for unit in unit_info.items(): # retrieve key-value-pairs as tuple
            item_list = list(unit) # turn tuple into list
            item_list.reverse() # reverse order such that sorting is w.r.t. counts
            unit_list.append(item_list)
        unit_list.sort(reverse=True) # sort list

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
                  format(locale.format("%d", sum(nums[1:]),
                                       grouping=True),
                         self.n_low,self.n_high)) # [p] modified - replaced self._counter.sum() by sum(nums[1:])
            print(" * there were also {0} occurences of number words (not used yet!)".
                  format(locale.format("%d", num['words'], grouping=True)))
            print(' * number words of interest: {0}'.
                  format(locale.format("%d", sum(numwords[1:]), grouping=True)))
            print(' * total amount of numerals between {1} and {2} (used for plot in fig1): {0}'.
                  format(locale.format("%d", (self._counter.sum() - self._counter[0]), grouping=True),
                         self.n_low,self.n_high)) # [p] modified to subtract the occurrences of 0
            print(' * occurrences of approx-num-combinations \n prec-round-dis: {0} \n prec-round-cont: {1} \
                  \n prec-nonr-dis: {2} \n prec-nonr-cont: {3} \n impr-round-dis: {4} \n impr-round-cont: {5} \
                  \n impr-nonr-dis: {6} \n impr-nonr-cont: {7} \n null-round-dis: {8} \n null-round-cont: {9} \
                  \n null-nonr-dis: {10} \n null-nonr-cont: {11}'.
                  format(locale.format("%d",tripleMatches[0],grouping=True),locale.format("%d",tripleMatches[1],grouping=True),locale.format("%d",tripleMatches[2],grouping=True), \
                                       locale.format("%d",tripleMatches[3],grouping=True), locale.format("%d",tripleMatches[4],grouping=True), locale.format("%d",tripleMatches[5],grouping=True), locale.format("%d",tripleMatches[6],grouping=True), \
                                       locale.format("%d",tripleMatches[7],grouping=True), locale.format("%d",tripleMatches[8],grouping=True), locale.format("%d",tripleMatches[9],grouping=True), locale.format("%d",tripleMatches[10],grouping=True), \
                                       locale.format("%d",tripleMatches[11],grouping=True)))
            print('number of asymmetrically modified numerals:',asym)
                    
        return nums,numwords # [p]

    def plotBars(self, nums, numwords): # [p] modified
        '''Plot a bar chart.
        '''
        # print('num array len:',len(nums))
        # print('numword array len:',len(numwords))
        # print('numword occurrences of 500:',numwords[500])
        
        if plt is None:
            print("error: no matplotlib seems to be installed. Install it before trying to plot.", file=sys.stderr)
            print("info: matplotlib is available for free from https://matplotlib.org/", file=sys.stderr)
        else:
            numbers = range(self.n_low, self.n_high + 1)
            # print('x axis len:',len(numbers))
            values = list(map(lambda x: self._counter[x], numbers))
            # print('values len:',len(values))
            plt.figure(1)
            plt.title('numbers + numberwords frequency')
            plt.bar(numbers, values) # num+numwords
            
            plt.figure(2)
            plt.title('numbers frequency')
            plt.bar(numbers, nums[1:]) # numbers
            
            plt.figure(3)
            plt.title('numberwords frequency')
            plt.bar(numbers, numwords[1:]) # numwords
            
            plt.show()
