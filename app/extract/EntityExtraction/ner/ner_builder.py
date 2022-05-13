#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals, print_function

import re
import json
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


class NER:

    def __init__(self):
        self._train_data = []
        self._path_in = ''
        self._path_out = ''
        self._path_log = ''
        self._model = None

    def _trim_entity_spans(self, data: list) -> list:
        """Removes leading and trailing white spaces from entity spans.

        Args:
            data (list): The data to be cleaned in spaCy JSON format.

        Returns:
            list: The cleaned data.
        """
        invalid_span_tokens = re.compile(r'\s')

        cleaned_data = []
        for text, annotations in data:
            entities = annotations['entities']
            valid_entities = []
            for start, end, label in entities:
                valid_start = start
                valid_end = end
                while valid_start < len(text) and invalid_span_tokens.match(
                        text[valid_start]):
                    valid_start += 1
                while valid_end > 1 and invalid_span_tokens.match(text[valid_end - 1]):
                    valid_end -= 1
                valid_entities.append([valid_start, valid_end, label])
            cleaned_data.append([text, {'entities': valid_entities}])

        return cleaned_data

    def initialize(self, path_in, path_out, path_log, model='en_core_web_sm'):
        self._path_in = path_in
        self._path_out = path_out
        self._path_log = path_log
        # Loading training data
        with open(self._path_in, 'r') as fin:
            self._train_data = self._trim_entity_spans(json.loads(fin.read()))

        if model is not None:
            self._model = spacy.load(model)  # load existing spaCy model
        else:
            self._model = spacy.blank("en")  # create blank Language class

    def train(self, n_iter=100):
        """Load the model, set up the pipeline and train the entity recognizer."""
        flog = open(self._path_log, 'w')

        # create the built-in pipeline components and add them to the pipeline
        # self._model.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in self._model.pipe_names:
            ner = self._model.create_pipe("ner")
            self._model.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = self._model.get_pipe("ner")

        # add labels
        for _, annotations in self._train_data:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in self._model.pipe_names if pipe not in pipe_exceptions]

        # only train NER
        with self._model.disable_pipes(*other_pipes) and warnings.catch_warnings():
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module='spacy')

            for itn in range(n_iter):
                random.shuffle(self._train_data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(self._train_data, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self._model.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # droself._path_in - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses, file=flog)

        # save model to output directory
        if self._path_out is not None:
            self._path_out = Path(self._path_out)
            if not self._path_out.exists():
                self._path_out.mkdir()
            self._model.to_disk(self._path_out)
            print("Saved model to", self._path_out, file=flog)

        flog.close()

    def check_trained(self):
        # test the trained model
        for text, _ in self._train_data:
            doc = self._model(text)
            print(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

