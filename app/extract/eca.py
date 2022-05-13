import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dotenv import load_dotenv
load_dotenv()

import re
from util.util import group_line_to_para, str_contains
from nltk import sent_tokenize

def do_eca(atext):
    items = []
    btext = group_line_to_para(atext)
    for idx, line in enumerate(btext.split('\n\n')):

        sents = sent_tokenize(line)

        for sidx, sent in enumerate(sents):
            if str_contains(sent.lower(), ["committee", "member of", "members of", "officer of", "director of"]):
                items.append({
                    "text": sent,
                    "paragraph": idx + 1,
                    "sentence": sidx + 1,
                })
    return items

def do_year(atext):

    YEAR_REGEX = r"""([12]\d\d\d)[^\d]"""

    etext = atext.replace('\n\n', '___xxYxxYxx___').replace('\n', '').replace('___xxYxxYxx___', '\n\n')
    etext = etext.replace('tel num', '')
    etext = etext.replace('email address es', '')
    return [re_match.group(1) for re_match in re.finditer(YEAR_REGEX, etext)]


    items = []
    btext = group_line_to_para(atext)
    for idx, line in enumerate(btext.split('\n\n')):

        sents = sent_tokenize(line)

        for sidx, sent in enumerate(sents):
            if str_contains(sent.lower(), ["committee", "member of", "members of", "officer of", "director of"]):
                items.append({
                    "text": sent,
                    "paragraph": idx + 1,
                    "sentence": sidx + 1,
                })
    return items