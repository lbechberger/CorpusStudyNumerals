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
regexes = []
for i in range(int(n)):     # pre-compile regexes to save some execution time
    regexes.append(re.compile('[ -\$"\[\(]'+str(i) +'[ \.,\!\?:-€;\]\)"]'))

with open(in_filename, 'r') as f:
    for line in f:
        match = re.search('^.*%(.*)$', line)  
        if (match != None):
            sentence = match.group(1)
            for i in range(int(n)):
                match_numeral = regexes[i].search(sentence)
                if match_numeral != None:
                    counts[i] += 1

print counts