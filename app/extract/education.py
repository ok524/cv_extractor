import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dotenv import load_dotenv
load_dotenv()

from util.util import group_line_to_para
from nltk import sent_tokenize



def do_edu(atext):
    items = []
    btext = group_line_to_para(atext)
    for idx, line in enumerate(btext.split('\n\n')):

        sents = sent_tokenize(line)

        for sidx, sent in enumerate(sents):
            if -1 != sent.lower().find('major'):
                items.append({
                    "text": sent,
                    "paragraph": idx + 1,
                    "sentence": sidx + 1,
                })
    return items
