# CorpusStudyNumerals
Some scripts for a corpus study on numerals

## count_numbers.py

count_numbers.py can be used as follows:

`python count_numbers.py path/to/corpus/file.txt 100 200`

It will plot the number of occurrences for each number from 100 to 200 (including both borders).
For the plots under /plots, the file eng_news_2015_3M-sentences.txt from the Leipzig corpus was used.

## count_numbers_separator.py

Same as count_numbers.py, but it also takes into account separators:
"1,000" is interpreted as "1000", not as "1".
