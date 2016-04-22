import pandas as pd
import sqlite3

conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\HTSCompounds1.db')
c = conn.cursor()

input_path = raw_input('Enter the PATH of compound file: ')

df = pd.read_csv(input_path)

cmpd = df['CompoundID']

for i in cmpd:
    c.execute('UPDATE EchoSource SET Volume = Volume - 1.5 WHERE Client_ID = ?', (i,))

conn.commit()
