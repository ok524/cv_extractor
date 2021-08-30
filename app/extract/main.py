import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dotenv import load_dotenv
load_dotenv()

import re
from util.util import lower, vars, lines_has_name
from extract.education import do_edu
from extract.eca import do_eca, do_year

import spacy

import extract.EntityExtraction.utils
from extract.EntityExtraction.ner import pre_description
from extract.EntityExtraction.ner import convert_brat
from extract.EntityExtraction.ner.ner_builder import NER

path_model = os.environ.get('ENTITY_MODEL')
ner_model = spacy.load(path_model)

def extract(textpath):
    return lower("hEllo ")

class Extractor():
    path_txt = 'aaa'
    atext = ''

    def __init__(self, path_txt):
        self.path_txt = path_txt
        with open(self.path_txt, mode='r') as f:
            self.atext = f.read()

    def run_all(self):
        entity = self.entity_extract()
        name_lines, name, gender = self.name_extract()
        skill_sets = {}
        for item in entity:
            if item['label'] not in skill_sets.keys():
                skill_sets[item['label']] = []
            skill_sets[item['label']].append(item['text'])
        for key in skill_sets:
            skill_sets[key] = list(set(skill_sets[key]))

        edus = self.edu_extract()
        ecas = self.eca_extract()
        emails = self.email_extract()
        years = self.year_extract()

        return {
            "name_lines": name_lines,
            "name": name,
            "gender": gender,
            "edus": edus,
            "skill_sets": skill_sets,
            "ecas": ecas,
            "emails": emails,
            "years": years,
            "entity": entity,
        }

    def entity_extract(self):
        txt_in = pre_description.preprocess(self.path_txt)
        doc = ner_model(txt_in)
        # print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

        entity = []
        for ent in doc.ents:
            # print(f"Entities {ent.text}, {ent.label_}")
            entity.append({
                'text': ent.text,
                'label': ent.label_,
            })
        return entity

    def name_extract(self):
        return lines_has_name(self.atext)

    def edu_extract(self):
        return do_edu(self.atext)

    def eca_extract(self):
        return do_eca(self.atext)

    def email_extract(self):
        EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

        etext = self.atext.replace('\n\n', '___xxYxxYxx___').replace('\n', '').replace('___xxYxxYxx___', '\n\n')
        return [re_match.group() for re_match in re.finditer(EMAIL_REGEX, etext)]

    def year_extract(self):
        return do_year(self.atext)


if __name__ == '__main__':
    instance = Extractor('a')

    path_txt = os.environ.get('TEXTPATH')
    entity = instance.entity_extract(path_txt)
    print(entity)

    extract(path_txt)
