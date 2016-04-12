
# FIX ISSUE WHEN SQL QUERY RETURNS NULL VALUE. THIS CAUSES A PROBLEM WHEN WRITING TO A CSV USING CSV.WRITEROW()

import pandas as pd
import sqlite3
import csv

conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\IncyteConfirmationScreenData.db')
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
        findcompound = c.execute("SELECT CompoundID, PercentInhibition FROM Data WHERE CompoundID=?", [i])
		
		if findcompound = 
        csvwriter.writerow(findcompound.fetchone())


