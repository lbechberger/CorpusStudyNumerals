from __future__ import print_function

import sys
import locale

from counter import Counter

# FIXME[hack]: should only be needed in language ...
import re

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


class bcolors:
    '''
    Inspired from
    https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        if not sys.stdout.isatty():
            self.HEADER = ''
            self.OKBLUE = ''
            self.OKGREEN = ''
            self.WARNING = ''
            self.FAIL = ''
            self.ENDC = ''

        
class Processor:
    '''A Processor can process a single text file from a corpus.  It is
    initialized using a Language object, providing language specific
    knowledge for processing.

    The Processor can be customized to 
    '''

    _match_numbers_flag = True
    _match_number_words_flag = True
    _match_dates_flag = True
    _match_time_flag = False
    _show_progress_flag = True
    _show_matches_flag = True
    _verbosity = 0

    _counter = None

    _bc = bcolors()

    
    def __init__(self, language, min=0, max=100, verbosity=0,
                 show_progress=False,
                 show_matches=False,
                 match_numberwords=True,
                 match_dates=False):
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

        self._verbosity = verbosity
        self._show_progress_flag = show_progress
        self._show_matches_flag = show_matches
        self._match_number_words_flag = match_numberwords
        
        if self._match_number_words_flag:
            self.language.precompile_numberwords(min,max)

            
        if self._match_dates_flag:
            # FIXME[hack]: should be done in language
            year = '(?:^|[^\d])(?:18|19|20|21)\d\d(?:$|[^\d])'
            month = 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
            date = '(?:' + year + '|' + month + ')'
            self._dates_regex = re.compile(date)

    def reset(self):
        '''Reset this processor.
        Resetting will only affect the counters, but not the
        configuration (range of interest, verbosity, etc.).
        '''
        self._counter.reset()


    def process(self, inputStream):
        '''Process an input stream. This is the main function of
        this class. It will read the stream line by line,
        look for numerals, either provided as numbers, or
        in words, and count the occurences.

        Arguments
        ---------
        inputStream
            The input stream to read.
        '''
        self.num = {'lines': 0, 'matches': 0, 'numbers': 0, 'words': 0}
        
        if self._verbosity > 0:
            sys.stderr.write("Starting to process ")

        for sentence in inputStream:

            # Remove leading and trailing whitespaces
            sentence = sentence.strip()

            # Remove everything before the first tabulator.
            # This is relevant for lines from the "Wortschatz" corpus,
            # as these lines have the format running_number-TAB-sentence.
            if "\t" in sentence:
                sentence = sentence.split("\t")[1]

            self.process_sentence(sentence)

            # output progress information (if desired)
            if self._show_progress_flag and (self.num['lines'] % 100000 == 0):
                sys.stderr.write('.' if self._verbosity > 0 else
                                 r'{}\r'.format(self.num['lines']))
                sys.stderr.flush()
            self.num['lines'] += 1

        if self._verbosity > 0:
            print(" processed {0} lines.".
                  format(locale.format("%d", self.num['lines'], grouping=True)),
                  file=sys.stderr)
        elif self._show_progress_flag:
            print(file=sys.stderr)

        if self._verbosity > 1:
            print("Some statistics:")
            print(" * {0} of these lines ({1}%) contain numbers".
                  format(locale.format("%d", self.num['matches'], grouping=True),
                         self.num['matches']*100//self.num['lines'] if self.num['lines'] > 0 else 100))
            print(" * in total we found {0} numbers".
                  format(locale.format("%d", self.num['numbers'], grouping=True)))
            print(" * {0} of these numbers are in the range of interest ({1}-{2})".
                  format(locale.format("%d", self._counter.sum(),
                                       grouping=True),
                         self._counter._min_value, # FIXME[hack]: private
                         self._counter._max_value)) # FIXME[hack]: private
            print(" * there were also {0} occurences of self.number words (not used yet!)".
                  format(locale.format("%d", self.num['words'], grouping=True)))


    def _replace_matches(self, matchobj):
        match = matchobj.group(0)
        #FIXME[hack]: should have a language method to do conversion!
        #number = int(match.replace(self.language.thousandsSeparator, ""))
        number = match.replace(self.language.thousandsSeparator, "")
        return self._bc.UNDERLINE + match + self._bc.ENDC + self._bc.OKGREEN + '(' + str(number) + ')' + self._bc.ENDC

    def _replace_numberwords(self, matchobj):
        match = matchobj.group(0)
        number = self.language.convert_numberword(match)
        return self._bc.UNDERLINE + match + self._bc.ENDC + self._bc.WARNING + '(' + str(number) + ')' + self._bc.ENDC

    def _replace_dates(self, matchobj):
        match = matchobj.group(0)
        return self._bc.FAIL + match + self._bc.ENDC


    def process_sentence(self, sentence):
        # look for ALL occurences of numbers (digits)

        # FIXME[hack]:
        if self._match_dates_flag:
            result, count = self._dates_regex.subn(self._replace_dates, sentence)
            if count:
                print(result)

        if self._match_numbers_flag:
            matches = self.language.match_numbers(sentence)
            self._counter(matches)

            if matches:
                self.num['matches'] += 1
                self.num['numbers'] += len(matches)

            if matches and self._show_matches_flag:
                # FIXME[hack]: should not access private element of language
                print(self.language._numbers_regex.sub(self._replace_matches, sentence))

        # look for occurences of number words
        if self._match_number_words_flag:
            matches = self.language.match_number_words(sentence)
            self._counter(matches)

            if matches:
                self.num['words'] += len(matches)

            if matches and self._show_matches_flag:
                # FIXME[hack]: should not access private element of language
                print(self.language._number_words_regex.sub(self._replace_numberwords, sentence))


    def plotBars(self):
        '''Plot a bar chart.
        '''

        if plt is None:
            print("error: no matplotlib seems to be installed. Install it before trying to plot.", file=sys.stderr)
            print("info: matplotlib is available for free from https://matplotlib.org/", file=sys.stderr)
        else:
            numbers = range(self._counter._min_value, # FIXME[hack]: private
                            self._counter._max_value + 1) # FIXME[hack]: private
            values = list(map(lambda x: self._counter[x], numbers))
            plt.bar(numbers, values)
            plt.show()
