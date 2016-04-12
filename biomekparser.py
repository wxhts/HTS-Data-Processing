__author__ = 'theendless219'

import pandas as pd
import glob
import sqlite3
import csv


report_files = glob.glob('C:\Users\IVtB Lab\Desktop\Hit1536\Raw\*.csv')

count1 = 0
for files in report_files:
    count1 += 1

    conn = sqlite3.connect('C:\Users\IVtB Lab\Desktop\Hit1536\Database\Destinations' + str(count1) + '.sql')
    c = conn.cursor()

    bigframe = pd.read_csv(files, keep_default_na=True, error_bad_lines=False).dropna(subset=['Client_ID'])

    ### For concatenated destination files
    ''''
    destinationframes = []
    for x in range(1, 3):
        destinationplate = bigframe[bigframe['Name'] == 'Destination' + str(x)]
        destinationframes.append(destinationplate)
    '''

    destinationplate1 = bigframe[bigframe['Name'] == 'Destination']
    # destinationplate1.to_csv('/Users/theendless219/Desktop/HTSReports/ParsedReports/1536Report/destination' + str(count1) + '.csv', index=False)
    destinationplate1.to_sql('Destination', conn, index=False)


    symbs = ['[', r"'\'", ']', '^', '_', '`']
    letters = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF']

    count2 = -1
    for x in symbs:
        count2 += 1
        letter = letters[count2]
        for i in range(5, 45):
            if x == r"'\'":
                c.execute('UPDATE Destination SET Well = ? WHERE Well = ?', (letter + str(i), x[1] + str(i)))
                conn.commit()
            else:
                c.execute('UPDATE Destination SET Well = ? WHERE Well = ?', (letter + str(i), x + str(i)))
                conn.commit()

    with open('C:\Users\IVtB Lab\Desktop\Hit1536\Clean\Destinations\Destination' + str(count1) + '.csv', 'wb') as f:
        destination = c.execute('SELECT * FROM Destination')
        writer = csv.writer(f)
        writer.writerow(['SequentialID', 'Name', 'Barcode', 'Well', 'Volume', 'CompoundID', 'SourceBC', 'SourceWell', 'SourcePlateBarcode', 'Liquid'])
        writer.writerows(destination)


    ### For concatenated destination files
    '''
    destinationresult = pd.concat(destinationframes)
    destinationresult.to_csv('/Users/theendless219/Desktop/HTSReports/ParsedReports/1536Report/destinationfile' + str(count) + '.csv', index=False)
    '''