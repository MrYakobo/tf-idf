#!/usr/bin/env python3

from itertools import chain
import math
import argparse
import re
import json


def tf(word, document):
    # term frequency: number of word occurances in document / amount of words in document
    return document.count(word) / len(document)


def df(word, documents):
    # document frequency: how many documents does this word appear in?
    s = 0
    for document in documents:
        if word in document:
            s += 1
    return s


def idf(word, documents):
    # inverse document frequency
    return math.log10(len(documents) / (df(word, documents)))


def tf_idf(word, document, documents):
    # increases if word is in document,
    # decreases if word is in other documents
    return tf(word, document) * idf(word, documents)


def split_and_lowercase(filename):
    with open(filename) as f:
        s = f.read()

    lst = []
    for word in s.split():
        # clean up word
        tmp = re.sub(r"\W+|\s", "", word).lower()
        if word:
            lst.append(tmp)

    return lst


def to_str(val):
    if type(val) == str:
        return val

    return f"{val:.3f}"


def print_table(data, keys):
    # https://stackoverflow.com/a/9989441
    padding = 5
    col_width = (
        max(len(to_str(val)) for row in data for val in chain(row, keys)) + padding
    )
    # header
    print("".join(to_str(val).ljust(col_width).upper() for val in keys))
    for row in data:
        print("".join(to_str(val).ljust(col_width) for val in row))


def print_dict_as_table(d):
    header = list(d[0].keys())
    vals = [f.values() for f in d]

    print_table(vals, header)


def main():
    parser = argparse.ArgumentParser(
        description="Calculates keywords in a document, using a word corpus."
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="get output as json",
    )
    parser.add_argument(
        "--min-df",
        default=2,
        type=int,
        help="if a word occurs less than this number of times in the corpus, it's not considered (default: 2)",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-n",
        type=int,
        default=10,
        help="limit output to this many words (default: 10)",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Don't limit the amount of words to output (default: false)",
    )
    parser.add_argument(
        "--input-document",
        "-i",
        required=True,
        help="document file to extract keywords from",
    )
    parser.add_argument(
        "corpus",
        default=[],
        nargs="*",
        help="corpus files (optional but highly reccommended)",
    )
    args = parser.parse_args()

    document = split_and_lowercase(args.document)

    # always include document file in corpus (if it's not already there)
    corpus_files = set(args.corpus + [args.document])
    corpus = [split_and_lowercase(file) for file in corpus_files]

    out = []
    for word in set(document):
        # skip too rare words
        if df(word, corpus) < args.min_df:
            continue

        row = {}
        row["word"] = word
        row["tf_idf"] = tf_idf(word, document, corpus)
        row["tf"] = tf(word, document)
        out.append(row)

    out = sorted(out, key=lambda x: [-x["tf_idf"], -x["tf"], x["word"]])
    n = args.n
    if not args.all:
        out = out[:n]

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=4))
        exit(0)

    print_dict_as_table(out)

    print("-----")
    num_words = len([word for doc in corpus for word in doc])
    print(f"num words in corpus: {num_words}")


if __name__ == "__main__":
    main()
