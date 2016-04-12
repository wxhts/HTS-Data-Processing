__author__ = 'David Itenberg'

import pandas as pd
import sqlite3
import csv

conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\HTSCompounds.db')
conn.text_factory = str
c = conn.cursor()

hit_file = raw_input('Enter PATH for hit file: ')
output_path = raw_input('Enter PATH for output file: ')

with open(output_path, 'wb') as output_file:
    csvwriter = csv.writer(output_file)

    df = pd.read_csv(hit_file)
    comp_ser = pd.Series(df['CompoundID']).dropna()
    #effect_ser = pd.Series(df['% Well Effect']).dropna()

    for i in comp_ser:
        findcompound = c.execute("SELECT EchoSource.Barcode, EchoSource.Well, EchoSource.Client_ID, ChinaSource.SMILES FROM EchoSource INNER JOIN ChinaSource ON EchoSource.Client_ID=ChinaSource.Client_ID WHERE EchoSource.Client_ID=?", [i])
        csvwriter.writerow(findcompound.fetchone())

    #effect_ser.to_csv(output_file, index=False)

