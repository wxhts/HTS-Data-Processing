import pandas as pd
import sqlite3
import csv


def stringify(identifier):
    return "'{}'".format(identifier)


def build_query(dataframe):
    query = ''
    count = 0
    for x in dataframe:
        count += 1
        if count == 1:
            query = '(' + stringify(x) + ','
        elif count == len(dataframe):
            query = query + stringify(x) + ')'
        else:
            query = query + stringify(x) + ','
    return query


conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\InceptionHits.db')
conn.text_factory = str
c = conn.cursor()

hit_file = raw_input('Enter PATH for hit file: ')
output_path = raw_input('Enter PATH for output file: ')

with open(output_path, 'wb') as output_file:
    csvwriter = csv.writer(output_file)

    df = pd.read_csv(hit_file)
    compounds = df['CompoundID'].dropna()
    cmpd = build_query(compounds)

    findcompound = c.execute("SELECT Barcode, Well, CompoundID FROM `384Plates` WHERE CompoundID IN " + cmpd)
    csvwriter.writerows(findcompound.fetchall())
