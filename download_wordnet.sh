if [ ! -e $HOME/nltk_data/ ]
then
    mkdir $HOME/nltk_data
fi
if [ ! -e $HOME/nltk_data/corpora/ ]
then
    mkdir $HOME/nltk_data/corpora
fi
if [ ! -e $HOME/nltk_data/corpora/wordnet/ ]
then
    mkdir $HOME/nltk_data/corpora/wordnet
fi
PATH_TO_NLTK_DATA=$HOME/nltk_data/
wget https://github.com/nltk/nltk_data/raw/gh-pages/packages/corpora/wordnet.zip
unzip ./wordnet.zip
mv wordnet/ $HOME/nltk_data/corpora/
rm wordnet.zip