import ast
import copy

import numpy as np
import openpyxl
import pandas as pd

from Erised_functions import (lookup_by_asin_id, get_log_column, product_line_names,
                              sites_db_name, sites_ext_name)

#TODO 1: Get export file data path=/api/v1/market/list
SALES_PERFORMANCE_LOG_FILE = r"data/sales_performance_logs.csv"
PRODUCT_LINE_BRAND_MODEL_TABLE = r"data/product_line_brand_model_table.csv"
OUTPUT_CSV_FILE = r"output/sales_performance.csv"
PRODUCT_LINE_COUNTS = 8
sp_sites   = ["None", {},   {},   {},   {},   {},   {},   {},   {},   {},   {},     {},   {},   {},   {},   {},   {},   {}]
sp_models_by_sites = ["None", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
sp_pdls_by_sites = ["None", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
sp_sites_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# for v1 onlypi
sp_pdls = ["None"]

def one_row_parser(in_data):
    items = in_data.split('\n')
    items.remove("")
    a_dict = dict((k.strip(), v.strip()) for k, v in (item.split(':') for item in items))
    
    sites = a_dict['country_ids'].strip("[]\"").split(",")
    product_line = a_dict['product_line_ids'].strip("[]\"").split(",")
    for s in sites:
        sp_sites_count[int(s.strip("\""))] += 1
        for p in product_line:
            try:
                sp_pdls_by_sites[int(s.strip("\""))][int(p.strip("\""))] += 1
            except KeyError:
                sp_pdls_by_sites[int(s.strip("\""))][int(p.strip("\""))] = 1

    models = a_dict['model_ids'].strip("[]\"").split(",")
    # print(models)
    # print(f"sp sites count={sp_sites_count}")
    # print(f"sp proudc line count by site = {sp_pdls_by_sites}")

    for ctry in sites:
        # model_filter_df = lookup_by_asin_id(models, sites_db_name)
        # for mdl in model_filter_df['id'].to_list():
        for mdl in models:
            try:
                sp_models_by_sites[int(ctry.strip("\""))][int(mdl.strip("\""))] += 1
            except KeyError:
                sp_models_by_sites[int(ctry.strip("\""))][int(mdl.strip("\""))] = 1


def find_the_most_one():
    max = 0
    n = 0
    ctry = 0
    for idx in range(1, len(sp_models_by_sites)):
        for k, v in sp_models_by_sites[idx].items():
            if v > max:
                max = v
                n = k
                ctry = idx
    
    print(f"max = {max}, model={n} in countyr site:{ctry}")

def sales_performance_analysis(data):
    rows = get_log_column(data, 'request_content')
    for record in rows:
        one_row_parser(record)

    # find_the_most_one()


def output_sites_usage_count(w):
    df = pd.DataFrame({'Sites':sites_ext_name, 'Counts':sp_sites_count})
    df = df.sort_values(by=['Counts'], ascending=False)
    df = df.drop([0, 10])  #Remove useless rows
    df.to_excel(w, sheet_name='SiteCounts')
    

def output_product_line_usage_count_by_site(w):
    src_dict = {}
    for i in range(len(sp_pdls_by_sites)):
        src_dict[i] = sp_pdls_by_sites[i]

    df = pd.DataFrame(src_dict)
    df.fillna(0, inplace=True)
    df = df.transpose()
    df.rename(columns={1:'PRJ', 2:'LCD', 3:'GGP', 4:'WTG', 5:'ESD', 6:'ADO', 7:'LTV', 8:'IFP'}, inplace=True)
    df = df.drop([0, 10])  #Remove useless rows
    df.to_excel(w, sheet_name='ProductLineCountsBySites')

def output_models_usage_count_by_site(w):
    src_dict = {}
    for i in range(len(sp_models_by_sites)):
        src_dict[i] = sp_models_by_sites[i]

    df = pd.DataFrame(src_dict)

    for i in range(len(sp_models_by_sites)):
        if i != 0 and i != 10:
            one_site = df[i].dropna()
            one_site = one_site.sort_values(ascending=False)
            model_info_df = lookup_by_asin_id(list(one_site.index.values))
            one_site_df = pd.DataFrame({'id':one_site.index, 'count':one_site.values}) 
            one_site_df = one_site_df.merge(model_info_df.drop(['product_line_id'], axis=1))
            one_site_df = one_site_df[one_site_df.country == sites_db_name[i]]
            one_site_df.to_excel(w, sheet_name=sites_db_name[i])

    df.fillna(0, inplace=True)
    df.to_excel(w, sheet_name='ModelsCountsBySites')

def sales_performance_analysis_v1(data):
    request_content = data['request_content']
    rows = request_content.to_list()
    items = rows[0].split('\n')
    items.remove("")
    print(items)
    a_dict = dict((k.strip(), v.strip()) for k, v in (item.split(':') for item in items))
    countrys = a_dict['country_ids'].strip("[]\"").split(",")
    print(countrys)
    product_line = a_dict['product_line_ids'].strip("[]\"").split(",")
    print(product_line)
    models = a_dict['model_ids'].strip("[]\"").split(",")
    print(models)

    for ctry in countrys:
        for mdl in models:
            try:
                sp_pdls[int(product_line[0])][int(ctry)][int(mdl)] += 1
            except KeyError:
                sp_pdls[int(product_line[0])][int(ctry)][int(mdl)] = 1

    print(sp_pdls)

logs = pd.read_csv(SALES_PERFORMANCE_LOG_FILE)
out_dict = {}
sales_performance_analysis(logs)
with pd.ExcelWriter("output/sp_usage_report.xlsx") as writer:
    output_sites_usage_count(writer)
    output_product_line_usage_count_by_site(writer)
    output_models_usage_count_by_site(writer)
