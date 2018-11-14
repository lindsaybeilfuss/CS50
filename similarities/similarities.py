import sys
from nltk.tokenize import sent_tokenize


def lines(a, b):
    linesa = set()
    linesb = set()

    for a in (a.splitlines( )):
        linesa.add(a)
    for b in (b.splitlines( )):
        linesb.add(b)
    linesa = linesa & linesb
    return list(linesa)


def sentences(a, b):
    sentencea = set(sent_tokenize(a))
    sentenceb = set(sent_tokenize(b))
    sentencea = sentencea & sentenceb
    return list(sentencea)



def substrings(a, b, n):
    substringseta = list()
    for i in range(len(a)):
        substringa = a[i:i+n]
        if len(substringa) == n:
            substringseta.append(substringa)

    substringsetb = list()
    for j in range(len(b)):
        substringb = b[j:j+n]
        if len(substringb) == n:
            substringsetb.append(substringb)
    substringcommon = set(substringseta).intersection(substringsetb)
    return substringcommon






