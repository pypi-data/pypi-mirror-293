import pandas as pd
def read_excel_custom(path):
    df=pd.read_excel(path)
    print(df)
    return df

def add_numbers(a,b):
    return a+b