#!/usr/bin/env python
# coding: utf-8

import sys
import os
import traceback
import json
import re
import random

import pandas as pd


def get_items_interacted(uid, interactions_indexed_df):
    # Get interacted items for a given user
    interacted_items = interactions_indexed_df.loc[uid]['pid']
    return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])


def get_value(obj, key):
    if obj is None:
        return None
    else:
        return obj.get(key)


def extract_fields(path_in, path_out):
    fields = ('oid', 'id', 'salary_max', 'salary_min', 'salaryOnDisplay', 'jobTitle', 'company_name', 'isInternship',
              'companyWebsite', 'summary', 'jobDescription', 'careerLevel', 'yearsOfExperience', 'qualification',
              'industry_value', 'industry_label', 'employmentType', 'languages', 'postedDate', 'closingDate',
              'jobFunctionValue', 'location', 'locationId', 'pageUrl', 'jobTitleSlug')

    with open(path_in, 'r') as fin, open(path_out, 'w') as ftxt:
        print('\t'.join(fields), file=ftxt)
        for line in fin:
            line = line.strip('\r').strip('\n').replace(r'\t', ' ').replace(r'\n', ' ').replace(r'\r', ' ').replace(
                r'\u0009', ' ')
            data = {}
            for field in fields:
                data[field] = None
            try:
                obj_json = json.loads(line)
                data['oid'] = get_value(obj_json.get('_id'), '$oid')
                data['id'] = obj_json.get('id')
                header = obj_json.get('header')
                companyDetail = obj_json.get('companyDetail')
                jobDetail = obj_json.get('jobDetail')
                locationInfo = obj_json.get('location')
                if type(locationInfo) is list:
                    locationInfo = locationInfo[0]
                data['pageUrl'] = obj_json.get('pageUrl')
                data['jobTitleSlug'] = obj_json.get('jobTitleSlug')
                salary = get_value(header, 'salary')
                data['jobTitle'] = get_value(header, 'jobTitle')
                company = get_value(header, 'company')
                data['isInternship'] = get_value(header, 'isInternship')
                data['salary_max'] = get_value(salary, 'max')
                data['salary_min'] = get_value(salary, 'min')
                data['salaryOnDisplay'] = get_value(salary, 'salaryOnDisplay')
                data['company_name'] = get_value(company, 'name')
                data['companyWebsite'] = get_value(companyDetail, 'companyWebsite')
                data['summary'] = get_value(jobDetail, 'summary')
                if data['summary'] is not None:
                    data['summary'] = '. '.join(data['summary'])
                data['jobDescription'] = get_value(jobDetail, 'jobDescription')
                jobRequirement = get_value(jobDetail, 'jobRequirement')
                data['careerLevel'] = get_value(jobRequirement, 'careerLevel')
                data['yearsOfExperience'] = get_value(jobRequirement, 'yearsOfExperience')
                data['qualification'] = get_value(jobRequirement, 'qualification')
                industryValue = get_value(jobRequirement, 'industryValue')
                data['employmentType'] = get_value(jobRequirement, 'employmentType')
                data['languages'] = get_value(jobRequirement, 'languages')
                data['postedDate'] = get_value(jobRequirement, 'postedDate')
                data['closingDate'] = get_value(jobRequirement, 'closingDate')
                data['jobFunctionValue'] = get_value(jobRequirement, 'jobFunctionValue')
                if data['jobFunctionValue'] is not None:
                    data['jobFunctionValue'] = json.dumps(data['jobFunctionValue'])
                data['industry_value'] = get_value(industryValue, 'value')
                data['industry_label'] = get_value(industryValue, 'label')
                data['location'] = get_value(locationInfo, 'location')
                data['locationId'] = get_value(locationInfo, 'locationId')

                for field, value in data.items():
                    if value is None:
                        data[field] = ''
                    else:
                        data[field] = str(data[field]).strip()
                print('\t'.join(data.values()), file=ftxt)

            except Exception as err:
                print(traceback.print_exc())
                print('{} \n {} \n\n'.format(line, str(err)), sys.stderr)


def extract_desc_ann(path_in, path_out, num):
    dict_desc = {}
    with open(path_in, 'r') as fin:
        for line in fin:
            if not contain_ch(line):
                obj_json = json.loads(line)
                head = obj_json.get('head')
                if not head:
                    continue
                oid = get_value(obj_json.get('_id'), '$oid')
                if oid is not None:
                    desc_str = get_value(obj_json.get('jobDetail'), 'jobDescription')
                    desc_str = desc_str.strip('\r').strip('\n').replace('\t', ' ').replace('\n', '. ').replace('\r',
                                                                                                               '. ').replace(
                        '\u0009', ' ')
                    desc_str = re.sub('(\. |\.){2,}', '. ', desc_str)
                    dict_desc[oid] = desc_str

    for oid in random.sample(dict_desc.keys(), num):
        ptxt = path_out + '/' + oid + '.txt'
        pann = path_out + '/' + oid + '.ann'
        with open(ptxt, 'w') as ftxt:
            ftxt.write(dict_desc.get(oid))
        with open(pann, 'w'):
            pass


def contain_ch(word):
    ch_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = ch_pattern.search(word)
    if match is not None:
        return True
    else:
        return False


def filter_non_en(path_in, path_out):
    with open(path_in, 'r') as fin, open(path_out, 'w') as ftxt:
        for line in fin:
            try:
                if not contain_ch(line):
                    ftxt.write(line)
            except Exception as err:
                print(traceback.print_exc())
                print('[{}], [{}].'.format(line, str(err)), sys.stderr)


# Format salary
def remove_tail(salary_str):
    return re.sub(' \(.*$', '', salary_str)


def cut_by_reg(reg_obj, title):
    if reg_obj is not None:
        loc = reg_obj.start()
        title_head = title[:loc].strip()
        tester = title_head.split(' ')
        if len(tester) >= 2 or (len(tester) == 1 and len(tester[0]) >= 5):
            title = title_head
    return title


def title_normalize(title):
    title = title.lower()
    title = cut_by_reg(re.search(r'\(', title), title)
    title = cut_by_reg(re.search(r'/', title), title)
    title = cut_by_reg(re.search(r',', title), title)
    title = cut_by_reg(re.search(r'-', title), title)
    title = cut_by_reg(re.search(r'–', title), title)
    return title.strip()


def translate_types(old_str, dict_type):
    list_new_types = []
    for type_tmp in old_str.split(','):
        type_tmp = type_tmp.strip()
        list_new_types.append(str(dict_type.get(type_tmp)))
    return ','.join(list_new_types)
