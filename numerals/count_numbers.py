#!/usr/bin/env python

"""
Created on Thu Jun  8 16:16:12 2017

Simply count the number of occurrence for different numbers.

@author: lbechberger
"""

from __future__ import print_function

import os
import sys
import locale
import argparse

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
    args = parser.parse_args()

    # initialize the language object (language of the corpus
    # determines number separators (1,000 vs. 1.000), assume English
    # if not given
    try:
        language = Language.create(args.language)
    except LookupError:
        print("error: language \"{}\" is not supported.".
              format(args.language), file=sys.stderr)
        sys.exit(1)

    # now do the processing ...
    processor = Processor(language, min=args.min, max=args.max)
    processor.verbosity = 2
    if not args.file:
        processor.processFile(sys.stdin)
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

        if os.path.isdir(name):
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
            nums, numwords = processor.processFile(inputStream) # [p] modified to return counts

    # finally plot the results
    if args.plot:
        processor.plotBars(nums, numwords) # [p] modified to use counts for plotting
