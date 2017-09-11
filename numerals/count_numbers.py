#!/usr/bin/env python
# command: python ./CorpusStudyNumerals-master/numerals/count_numbers.py --plot --min=0 
# --max=100000 ./eng_news_2015_100K/eng_news_2015_100K-sentences.txt

"""
Created on Thu Jun  8 16:16:12 2017

Simply count the number of occurrence for different numbers.

@author: lbechberger
"""

from __future__ import print_function

import os
import sys
import locale
import argparse # [p] sets up the parser for the input from the command line

from languages import Language
from processor import Processor

locale.setlocale(locale.LC_ALL, '')

__version__ = '0.1'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Numerals extractor')
    parser.add_argument("--min", default = 1, type = int,
                        help = 'minimal numeral to count')
    parser.add_argument("--max", default = 100, type = int,
                        help = 'maximal numeral to count')
    parser.add_argument("--language", default = 'en',
                        help = 'the corpus language (en, de, ...)')
    parser.add_argument('-p', '--plot', action="store_true",
                        help = 'provide a bar plot of the results')
    parser.add_argument("--version", action='version',
                        version='%(prog)s version ' + __version__,
                        help = 'output version information and exit')
    parser.add_argument("file", nargs='*',
                        help = 'the file(s) to process')
    args = parser.parse_args() # [p] args is arguments min, max, language, [...] and file to process
# -----------------------------------------------------------------------------
    # initialize the language object (language of the corpus
    # determines number separators (1,000 vs. 1.000), assume English
    # if not given
    try:
        language = Language.create(args.language)
    except LookupError:
        print("error: language \"{}\" is not supported.".
              format(args.language), file=sys.stderr)
        sys.exit(1)
# -----------------------------------------------------------------------------
    # now do the processing ...
    processor = Processor(language) # [p] Processor object constructed from input 'language'
    processor.setLimits(args.min, args.max)  # [p] method setLimits specified
    processor.verbosity = 2 # [p] such a talkative program
    if not args.file:
        processor.processFile(sys.stdin) # [p] what does sys.stdin do here :'(
    for name in args.file:
        if name == '-':
            processor.processFile(sys.stdin)
            continue

        # try to find determine the path to the name ...
        if not os.path.exists(name):
            if ('WORTSCHATZ_ROOT' in os.environ and
                os.path.exists(os.path.join(os.environ['WORTSCHATZ_ROOT'],
                                            name))):
                name = os.path.join(os.environ['WORTSCHATZ_ROOT'], name)
            else:
                print("error: no file called \"{}\"".
                      format(name),file=sys.stderr)
                sys.exit(1)

        if os.path.isdir(name): # [p] NOTIMPORTANT nice foresightful stuff l did there
            guess = os.path.join(name, os.path.basename(name)+"-sentences.txt")
            if os.path.isfile(guess):
                name = guess
            else:
                print("error: directory \"{}\" does not contain a valid file".
                      format(name),file=sys.stderr)
                sys.exit(1)

        # ... and run the processor
        print("Using \"{}\"".format(name), file=sys.stderr)
        with open(name, 'r', encoding="utf8") as inputStream:
            processor.processFile(inputStream)

    # finally plot the results
    if args.plot:
        processor.plotBars()
