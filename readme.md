# File-based TF-IDF

*Calculates keywords in a document, using a word corpus.*

## Why?

Because I found myself with hundreds of plain text files, with no way to know what each one contains. I then recalled this thing called TF-IDF from university, but found no utility that operates on files. Hence, here we are.

## How?

Basically, each word in the current document gets a score. The score increases each time the word it appears in this document, and decreases each time it appears in another document. The words with the highest scores will thus (theoretically) be the keywords.

Of course, this requires you to have many other documents (the corpus) to compare with. They should contain approximately the same language. For example, it makes sense to split chapters in a book and use those as the corpus. Use your senses.

## Installation

Copy `tfidf.py` to some location on `$PATH`

## Usage

```
usage: tfidf [-h] [--json] [--min-df MIN_DF] [-n N | --all] --input-document INPUT_DOCUMENT [corpus ...]

Calculates keywords in a document, using a word corpus.

positional arguments:
  corpus                corpus files (optional but highly reccommended)

options:
  -h, --help            show this help message and exit
  --json, -j            get output as json
  --min-df MIN_DF       if a word occurs less than this number of times in the corpus, it's not considered (default: 2)
  -n N                  limit output to this many words (default: 10)
  --all                 Don't limit the amount of words to output (default: false)
  --input-document INPUT_DOCUMENT, -i INPUT_DOCUMENT
                        document file to extract keywords from
```

# Examples

To get the top 10 keywords for chapter 1 of Moby Dick:

```
# assume that *.txt matches all other chapters of mobydick
$ tfidf -n 10 -i mobydick_chapter1.txt *.txt

WORD             TF_IDF           TF               
passenger        0.003            0.002            
whenever         0.003            0.002            
money            0.003            0.002            
passengers       0.002            0.001            
purse            0.002            0.001            
me               0.002            0.011            
image            0.002            0.001            
hunks            0.002            0.001            
respectfully     0.002            0.001            
robust           0.002            0.001            
-----
num words in corpus: 208425
```

```
$ tfidf --all -j -i mobydick_chapter1.txt *.txt
[
    {
        "word": "lazarus",
        "tf_idf": 0.0052818627137794375,
        "tf": 0.0028169014084507044
    },
    {
        "word": "frost",
        "tf_idf": 0.004433890895007659,
        "tf": 0.0028169014084507044
    },
    {
        "word": "bedford",
        "tf_idf": 0.0037492766733561254,
        "tf": 0.0028169014084507044
    },
    ...
]
```

## TF-IDF equations

```
t — term (word)
d — document (set of words)
corpus — (set of documents)
N — number of documents in corpus

tf(t,d) = count of t in d / number of words in d
df(t) = occurrence of t in N documents
idf(t) = N/df(t)

tf_idf(t, d) = tf(t, d) * idf(t)
```