# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:16:12 2017

Simply count the number of occurrence for different numbers.

@author: lbechberger
"""

import sys, re

in_filename = sys.argv[1]   # input file to read (i.e., corpus)
n = sys.argv[2]             # look at all numbers between 0 and n-1

counts = [0] * int(n)
# regex to search for numbers --> precompile for efficiency
regex = re.compile('^.*\t.*[ -\$"\[\(](\d+)[ \.,\!\?:-€;\]\)"].*$')

num_lines = 0
with open(in_filename, 'r') as f:
    for line in f:
        match = regex.search(line)
        if match != None:
            number = int(match.group(1))        # found a number: add it to list if necessary
            if number >= 0 and number < int(n):
                counts[number] += 1
        num_lines += 1
        if num_lines % 500000 == 0: # progress bar
            print num_lines

print counts
print num_lines