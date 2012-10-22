#!/usr/bin/python
#encoding=utf-8
#
# Afinn files: http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip

import math
import re

# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = '../media/AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence.
    """
    words = pattern_split.split(text.lower())
    features = [(word, afinn.get(word)) for word in words if word in afinn]
    sentiments = [afinn.get(word, 0) for word in words]

    if sentiments:
        # How should you weight the individual word sentiments?
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
    else:
        sentiment = 0
    return sentiment, features



if __name__ == '__main__':
    # Single sentence example:
    input_ = '1'
    while input_:
        input_ = raw_input('text: ')
        print("%6.2f %s" % (sentiment(input_)[0], input_))
