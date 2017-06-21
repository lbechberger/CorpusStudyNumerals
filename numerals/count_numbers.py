# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:16:12 2017

Simply count the number of occurrence for different numbers.

@author: lbechberger
"""

import sys, re
import matplotlib.pyplot as plt

in_filename = sys.argv[1]   # input file to read (i.e., corpus)
n_low = int(sys.argv[2])    # look at all numbers >= n_low
n_high = int(sys.argv[3])   # and <= n_high

counts = {}
# regex to search for numbers --> precompile for efficiency
regex = re.compile('^.*\t.*[ \-\$"\[\(](\d+)[ \.,\!\?:\-€;\]\)"].*$')

print "starting to process..."
num_lines = 0
with open(in_filename, 'r') as f:
    for line in f:
        match = regex.search(line)
        if match != None:
            number = int(match.group(1))        # found a number: add it to the dictionary if necessary
            if number >= n_low and number <= n_high:
                if not number in counts:    # not yet in dictionary: new entry
                    counts[number] = 1
                else:                       # already in dictionary: increase
                 counts[number] = counts[number] + 1
        num_lines += 1
        if num_lines % 500000 == 0: # progress bar
            print "...{0} lines".format(num_lines)

print "processed {0} lines".format(num_lines)

# plot a bar chart
numbers = range(n_low, n_high + 1)
values = map(lambda x: counts[x] if x in counts else 0, numbers)
plt.bar(numbers, values)
plt.show()