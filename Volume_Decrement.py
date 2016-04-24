import pandas as pd
import sqlite3

def stringify(identifier):
    return "'{}'".format(identifier)

def build_query(dataframe):
    query = ''
    for x in dataframe:
        if x == dataframe[0]:
            query = '(' + stringify(x) + ','
        elif x == dataframe[-1]:
            query = query + stringify(x) + ')'
        else:
            query = query + stringify(x) + ','
    return query


conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\HTSCompounds.db')
c = conn.cursor()

input_path = raw_input('Enter the PATH of compound file: ')

df = pd.read_csv(input_path)
compound = df['CompoundID']
cmpd = build_query(compound)

c.execute('UPDATE EchoSource SET Volume = Volume - 1.5 WHERE Client_ID IN ' + cmpd)
conn.commit()

