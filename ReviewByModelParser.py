import pandas as pd
from Erised_functions import lookup_by_model

REVIEW_BY_MODEL_LOG_FILE = r"data/review_by_model_logs.csv"
PRODUCT_LINE_BRAND_MODEL_TABLE = r"data/product_line_brand_model_table.csv"
OUTPUT_CSV_FILE = r"output/review_by_models.csv"

logs = pd.read_csv(REVIEW_BY_MODEL_LOG_FILE)
request_content = logs['request_content']
rows = request_content.to_list()
df = pd.DataFrame(columns=['Product Line', 'Brand-Model', 'Times'])
out_dict = {}
for item in rows:
    model = item[item.index('"')+1: len(item)-2]
    model = model.replace('\\', '')
    # print(model)
    try:
        out_dict[model] += 1
    except KeyError:
        out_dict[model] = 1

df_table = pd.read_csv(PRODUCT_LINE_BRAND_MODEL_TABLE)

for key in out_dict.keys():
    # lookup_by_model(df_table, key)
    pl, brand = lookup_by_model(df_table, key)
    brand_model = '-'.join([brand, key])
    l = [pl, brand_model, out_dict[key]]
    df.loc[len(df)] = l


df1 = df.sort_values(by=['Times'], ascending=False)
print(df1) 
df1.to_csv(OUTPUT_CSV_FILE)

