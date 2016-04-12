__author__ = 'IVtB Lab'

import pandas as pd
import sqlite3
import csv

conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\INCYTE_Primary_data.db')
conn.text_factory = str
c = conn.cursor()

hit_file = raw_input('Enter PATH for hit file: ')
output_path = raw_input('Enter PATH for output file: ')

with open(output_path, 'wb') as output_file:
    csvwriter = csv.writer(output_file)

    df = pd.read_csv(hit_file)
    comp_ser = pd.Series(df['CompoundId']).dropna()


    for i in comp_ser:
        findcompound = c.execute("SELECT CompoundId, AVG(WellEffect) FROM ConfirmationScreen WHERE CompoundId=?", [i])
        csvwriter.writerow(findcompound.fetchone())



