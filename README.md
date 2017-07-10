# CorpusStudyNumerals
Some scripts for a corpus study on numerals

## count_numbers.py

count_numbers.py can be used as follows:
```python
python count_numbers.py path/to/corpus/file.txt 100 200 en
```

This script plots the number of occurrences for each number from 100 to 200 (including both borders), assuming English separators (i.e., "1,000" = "1000"). The last parameter can also be set to "de" (which results in using points to separate digits: "1.000" = "1000").
For the plots under /plots, the file eng_news_2015_3M-sentences.txt from the Leipzig corpus was used.

