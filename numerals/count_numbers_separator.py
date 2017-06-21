# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:16:12 2017

Count the number of occurrence for different numbers, taking into account separators like "1,000".

@author: lbechberger
"""

import sys, re
import matplotlib.pyplot as plt

in_filename = sys.argv[1]   # input file to read (i.e., corpus)
n_low = int(sys.argv[2])    # look at all numbers >= n_low
n_high = int(sys.argv[3])   # and <= n_high

# language of the corpus determines number separators (1,000 vs. 1.000), assume English if not given
language = sys.argv[4] if len(sys.argv) >= 5 else "en"    
separator = ","
if language == "de":
    separator = "."

counts = {}
# regex to search for numbers --> precompile for efficiency
regex = re.compile('^.*\t.*[ -\$"\[\(](\d+(\{0}\d\d\d)*)[ \.,\!\?:-€;\]\)"].*$'.format(separator))


print "starting to process..."
num_lines = 0
with open(in_filename, 'r') as f:
    for line in f:
        match = regex.search(line)
        if match != None:
            text = str(match.group(1)).replace(separator, "")
            number = int(text)        # found a number: add it to the dictionary if necessary
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

print counts[10]