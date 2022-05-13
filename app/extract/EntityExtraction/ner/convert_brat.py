#!/usr/bin/env python
# coding: utf-8

import os
import re
import json


def process(pin, pout):

    reg_tail = re.compile('\.ann$')

    train_data = []
    for (dirpath, _, filenames) in os.walk(pin):
        for fname in filenames:
            if reg_tail.search(fname) is not None:
                pann = ''.join((dirpath, fname))
                list_ann = []
                with open(pann, 'r') as fann:
                    for line in fann:
                        items = line.split('\t')[1].split(' ')
                        try:
                            list_ann.append((int(items[1]), int(items[2]), items[0]))
                        except:
                            print(pann)

                if len(list_ann) != 0:
                    ptxt = ''.join((dirpath, fname[:-4] + '.txt'))
                    ftxt = open(ptxt, 'r')
                    job_txt = ftxt.read()
                    ftxt.close()
                    train_data.append((job_txt, {'entities': list_ann}))

    train_data_str = json.dumps(train_data)

    with open(pout, 'w') as fout:
        fout.write(train_data_str)
