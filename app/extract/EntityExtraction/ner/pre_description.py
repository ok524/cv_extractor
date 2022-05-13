#!/usr/bin/env python
# coding: utf8

import re


def preprocess(pin):
    with open(pin, 'r') as fin:
        content = fin.read()
        content = content.strip('\r').strip('\n').replace('\t', ' ').replace('\n', '. ').replace('\r', '. ').replace('\u0009', ' ')
        content = re.sub('(\. |\.){2,}', '. ', content)
        return content


def read(pin):
    with open(pin, 'r') as fin:
        content = fin.read()
        return content