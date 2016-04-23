import pandas as pd
import sqlite3

def stringify(identifier):
    return "'{}'".format(identifier)

conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\HTSCompounds.db')
c = conn.cursor()

input_path = raw_input('Enter the PATH of compound file: ')

df = pd.read_csv(input_path)
cmpd = df['CompoundID']

query = ''
for x in cmpd:
    if x == cmpd[0]:
        query = '(' + stringify(x) + ','
    elif x == cmpd[-1]:
        query = query + stringify(x) + ')'
    else:
        query = query + stringify(x) + ','

c.execute('UPDATE EchoSource SET Volume = Volume - 1.5 WHERE Client_ID IN ' + query)
conn.commit()

