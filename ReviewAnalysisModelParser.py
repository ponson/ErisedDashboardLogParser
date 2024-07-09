#TODO 1: Got export file data
import pandas as pd
from Erised_functions import lookup_by_model

COUNTRY_NAMES = {'1':'US', '2':'UK', '3':'FR', '4':'DE', '5':'IT', '6':'ES', '7':'JP',  '8':'CA', '9':'MX', '11':'IN', '12':'AU', '13':'BR', '14':'AE', '15':'NL', '16':'SE', '17':'SG', '18':'SA'} 
REVIEW_ANALYSIS_LOG_FILE = r"data/review_analysis_logs.csv"
PRODUCT_LINE_BRAND_MODEL_TABLE = r"data/product_line_brand_model_table.csv"
OUTPUT_CSV_FILE = r"output/review_analysis_models.csv"


def filter_content_str(line_str):
    item_list = line_str[line_str.index("[")+1:line_str.index("]")]
    item_list = item_list.replace('"', '')
    return item_list.split(',')

logs = pd.read_csv(REVIEW_ANALYSIS_LOG_FILE)
request_content = logs['request_content']
rows = request_content.to_list()
df = pd.DataFrame(columns=['Product Line', 'Site-Brand-Model', 'Times'])
print(f"df = {df}")
out_dict = {}
for item in rows:
    lines = item.split('\n')
    country_line = filter_content_str(lines[0])
    model = filter_content_str(lines[1])[0]
    # print(f"country: {country_line}, model: {model_line}")
    if model == 'null':
        continue
    for country in country_line:
        key = country + '&' + model
        try:
            out_dict[key] += 1
        except KeyError:
            out_dict[key] = 1


df_table = pd.read_csv(PRODUCT_LINE_BRAND_MODEL_TABLE)

for key_bind in out_dict.keys():
    c, m = key_bind.split('&')
    print(f"{c}, {m} = {out_dict[key_bind]}")
    names = COUNTRY_NAMES[c]
    pl, brand = lookup_by_model(df_table, m)
    site_brand_model = '-'.join([COUNTRY_NAMES[c], brand, m])
    l = [pl, site_brand_model, out_dict[key_bind]]
    df.loc[len(df)] = l

df1 = df.sort_values(by=['Times'], ascending=False)
print(df1) 
df1.to_csv(OUTPUT_CSV_FILE)
#TODO 4: add to table
#TODO 5: output data


