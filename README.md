# CorpusStudyNumerals
Some scripts for a corpus study on numerals


## Installation

The package is more or less self contained. There are no hard
requirements to run the programs. However, to actually use it in a
reasonable way, you need the following:
* [num2words](https://pypi.python.org/pypi/num2words)
* [digify](https://pypi.python.org/pypi/Digify)
* [matplotlib](https://matplotlib.org/)  (if you want to create plots)
* some corpus, i.e. a plain text file containing example sentences --
  you may use data from the Leipzig [Wortschatz](http://wortschatz.uni-leipzig.de)
  project


## The program `count_numbers.py`

The program `count_numbers.py` (in the subdirectory `numerals/`)is the
main program of the package.  It can be used as follows:

```shell
python count_numbers.py --plot path/to/corpus/file.txt
```

The script then plots the number of occurrences for each number from
1 to 100 (including both borders). To change the range of interest,
you can specify the boundaries on the command line:

```shell
python count_numbers.py --plot --min=10 --max=1000 path/to/corpus/file.txt
```

The script usually assumes English texts and behaves accordingly
(e.g., using "," as a thousands separator "1,000" = "1000"). The
language can be changed using a command line option:

```shell
python count_numbers.py --plot --language=de path/to/corpus/file.txt
```

### Processing Wortschatz data

If you work on the Leipzig
[Wortschatz](http://wortschatz.uni-leipzig.de) data, you may set the
environemnt variable `WORTSCHATZ_ROOT` to point to the directory where
the Wortschatz data have been unpacked. With this setting it is
sufficent to provide only the name of the corpus on the command line,
i.e.

```shell
export WORTSCHATZ_ROOT=/path/to/the/wortschatz/data
python count_numbers.py --plot eng_news_2015_1M
```

should behave identical to

```shell
python count_numbers.py --plot /path/to/the/wortschatz/data/eng_news_2015_1M/eng_news_2015_1M-sentences.txt
```

### The Processor

The `Processor` (implemented in `processor.py`) does the actual
work. It provides methods for searching numerals in the input stream
(`processFile()`) and for plotting the results (`plotBars()`).


### The Languages

The `Language`s implemented in `languages.py` provide language
specific information to be used during processing.


## Plots

For the plots under `plots/`, the file `eng_news_2015_3M-sentences.txt`
from the Leipzig corpus was used.


## Tests

There are some (necessarily) incomplete unit tests in the `tests/`
directory (see the [Python documentation on unit
testing](https://docs.python.org/3/library/unittest.html) to learn how
to add more tests).  You may run the tests by typing (being in the
project root directory):

```shell
python -m unittest tests.test_languages
```
and
```shell
python -m unittest tests.test_regex
```

The file `tests/test_regex.py` does not actually test parts of this
package but is intended for experimenting with regular expressions.


## Compatibility

We try to make the code compatible with (recent vesions of) Python 2
and Python 3. If you experience any problems, please let as know!
