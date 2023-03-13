import pandas as pd

PRODUCT_LINE_BRAND_MODEL_TABLE = r"data/product_line_brand_model_table.csv"

sites_db_name = ['None', 'com', 'co.uk', 'fr', 'de', 'it', 'es', 'co.jp', 'ca', 'com.mx', 'NONE2', 'in', 'com.au', 'com.br', 'ae', 'nl', 'se', 'sg']
sites_ext_name = ['None', 'US', 'UK', 'FR', 'DE', 'IT', 'ES', 'JP', 'CA', 'MX', 'NONE2', 'IN', 'AU', 'BR', 'AE', 'NL', 'SE', 'SG']
product_line_names = ['None', 'PRJ', 'LCD', 'GGP', 'WTG', 'ESD', 'ADO', 'LTV', 'IFP']


def lookup_by_model(df_table, model):
    print(f"lbm={model}")
    df1 = df_table[df_table.model == model].reset_index(drop=True)
    print(df1)
    if df1.empty:
        return 'None', 'None'
    else:
        print(f"model= {model} => {df1.iat[0, 2]}, {df1.iat[0, 3]}")
        return df1.iat[0, 3], df1.iat[0, 4]

def lookup_by_asin_id(id_list):
    df_table = pd.read_csv(PRODUCT_LINE_BRAND_MODEL_TABLE)
    idxl = []
    for i in id_list:
        idx = df_table[df_table.id == i].index[0]
        idxl.append(idx)
    # print(f"idxl={idxl}")
    df1 = df_table.iloc[idxl]
    return df1

def get_log_column(logs, col):
    request_content = logs['request_content']
    return request_content.to_list()