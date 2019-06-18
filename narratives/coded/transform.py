import pandas
import numpy

def clean(text):
    for ch in [' ','\\','`','*','{','}','[',']','(',')','>','#','+','-','.','!','$','\'','/']:
        if ch in text:
            text = text.replace(ch,'_')
    return text

def transform(df, code):
    df[code + '_clean'] = df[code].apply(clean)

    for elem in df[code + '_clean'].unique():
        df[str(elem)] = (df[code + '_clean'] == elem)*1
    return df.drop(columns=[code, code + '_clean']).drop_duplicates()

