# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:16:12 2017

Simply count the number of occurrence for different numbers.

@author: lbechberger
"""

import sys, re
import matplotlib.pyplot as plt

in_filename = sys.argv[1]   # input file to read (i.e., corpus)
n = int(sys.argv[2])             # look at all numbers between 0 and n-1

counts = [0] * n
# regex to search for numbers --> precompile for efficiency
regex = re.compile('^.*\t.*[ -\$"\[\(](\d+)[ \.,\!\?:-€;\]\)"].*$')

print "starting to process..."
num_lines = 0
with open(in_filename, 'r') as f:
    for line in f:
        match = regex.search(line)
        if match != None:
            number = int(match.group(1))        # found a number: add it to list if necessary
            if number >= 0 and number < n:
                counts[number] += 1
        num_lines += 1
        if num_lines % 500000 == 0: # progress bar
            print "...{0} lines".format(num_lines)

print "processed {0} lines".format(num_lines)

# plot a bar chart
plt.bar(range(n), counts)
plt.show()