import pandas as pd


def lookup_by_model(df_table, model):
    # print(model)
    df1 = df_table[df_table.model == model].reset_index(drop=True)
    print(df1)
    # print(f"model= {model} => {df1.iat[0, 2]}, {df1.iat[0, 3]}")
    return df1.iat[0, 1], df1.iat[0, 2]

