import numpy as np
import pandas as pd
import openpyxl
import ast
from Erised_functions import lookup_by_asin_id, get_log_column, sites_db_name, sites_ext_name, product_line_names


PRODUCT_PAGE_LOG_FILE = r"data/product_page_logs.csv"
PRODUCT_LINE_BRAND_MODEL_TABLE = r"data/product_line_brand_model_table.csv"
OUTPUT_CSV_FILE = r"output/product_go.csv"
site_query_count = {'com':0, 'co.uk':0, 'fr':0, 'de':0, 'it':0, 'es':0, 'co.jp':0, 'ca':0, 'com.mx':0, 'in':0, 'com.au':0, 'com.br':0, 'ae':0, 'nl':0, 'se':0, 'sg':0}
pd_models_by_sites = [ {},      {},   {},   {},   {},   {},      {},   {},       {},   {},       {},       {},   {},   {},   {},  {}]
pd_sites_db_name = ['com', 'co.uk', 'fr', 'de', 'it', 'es', 'co.jp', 'ca', 'com.mx', 'in', 'com.au', 'com.br', 'ae', 'nl', 'se', 'sg']
pd_sites_ext_name = ['US', 'UK',    'FR', 'DE', 'IT', 'ES', 'JP',    'CA', 'MX',     'IN', 'AU',     'BR',     'AE', 'NL', 'SE', 'SG']


def one_row_pd_log_parser(row_data):
    items = row_data.split('\n')
    items.remove("")
    a_dict = dict((k.strip(), v.strip()) for k, v in (item.split(':') for item in items))
    asins = a_dict['asin_ids'].strip("[]\"").split(",")
    for idx in range(len(asins)):
        asins[idx] = int(asins[idx].strip("\""))
    print(asins)
    model_info_df = lookup_by_asin_id(asins)
    print(f"DataType is: {type(model_info_df)}")
    if type(model_info_df) == pd.core.frame.DataFrame:
        model_info_df = model_info_df.reset_index()
        # print(model_info_df)
        # for idx in range(model_info_df.count()):
        the_site = "NONE"
        for idx in range(len(model_info_df.index)):
            model_data = model_info_df.iloc[idx]
            if idx == 0:
                site_query_count[model_data['country']] += 1
                the_site = model_data['country']
            try:
                pd_models_by_sites[pd_sites_db_name.index(the_site)][model_data['model']][0] += 1
            except KeyError:
                pd_models_by_sites[pd_sites_db_name.index(the_site)][model_data['model']] = [1, model_data['name'], model_data['brand']]
        
    # print(site_query_count)

def product_page_analysis(data):
    rows = get_log_column(data, 'request_content')
    for record in rows:
        one_row_pd_log_parser(record)


def pd_output_sites_usage_count(w):
    df = pd.DataFrame({'Sites':site_query_count.keys(), 'Counts':site_query_count.values()})
    print(f"df count is: {df.count()['Sites']}")
    for i in range(df.count()['Sites']):
         df.iat[i, 0] = pd_sites_ext_name[pd_sites_db_name.index(df.iat[i, 0])]

    df = df.sort_values(by=['Counts'], ascending=False)
    df.to_excel(w, sheet_name='SiteQueryCounts')
 

def pd_output_models_usage_count(w):
    for idx in range(len(pd_sites_db_name)):
        ctry_models = pd_models_by_sites[idx]
        model_keys = ctry_models.keys()
        counts = []
        product_lines = []
        brands = []
        for k in model_keys:
            c = ctry_models[k][0]
            pl = ctry_models[k][1]
            b = ctry_models[k][2]
            counts.append(c)
            product_lines.append(pl)
            brands.append(b)
        df = pd.DataFrame({'Brand':brands, 'Product Line': product_lines, 'Models':ctry_models.keys(), 'Counts': counts})
        df = df.sort_values(by=['Counts'], ascending=False)
        df.to_excel(w, sheet_name=pd_sites_ext_name[idx])
    

#TODO: Parsing log
logs = pd.read_csv(PRODUCT_PAGE_LOG_FILE)
product_page_analysis(logs)


#TODO: Get sites count
with pd.ExcelWriter("output/pd_usage_report.xlsx") as writer:
    pd_output_sites_usage_count(writer)
    pd_output_models_usage_count(writer)
#TODO: Get model count
# print(pd_models_by_sites)