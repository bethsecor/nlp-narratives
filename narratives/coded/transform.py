import pandas
import numpy

def transform(df, code):
    for elem in df[code].unique():
        df[str(elem)] = (df[code] == elem)*1
    return df.drop(columns=[code]).drop_duplicates()

