import json
import csv

# Converts JSON data exported from Analyze Dose Response to CSV format

path = raw_input('Enter the PATH of the JSON file: ')
samples = int(raw_input('How many samples are in this file?: '))
wells = int(raw_input('How many wells are used per titration? (including duplicates): '))
output = raw_input('Enter the PATH of the CSV file: ')

with open(path, 'r') as data_file:
    data = json.load(data_file)
    count1 = 0
    parsedData = open(output, 'wb')
    csvwriter = csv.writer(parsedData)
    addHeaders = [u'id', u'IP', u'Max', u'Min', u'Slope']

    for i in range(samples):
        if count1 == 0:
            hedr_data = data['results'][i]['wells'][0]
            header = hedr_data.keys() + addHeaders
            csvwriter.writerow(header)
            count1 += 1

        allCurveData = data['results'][i]
        curveDataKeys = allCurveData.values()
        curveDataSplit = ['', '', '', '', '', '', '', '', '', curveDataKeys[18], curveDataKeys[13], curveDataKeys[5],
                          curveDataKeys[3], curveDataKeys[0]]
        csvwriter.writerow(curveDataSplit)
        
        for x in range(wells):
            titr_data = data['results'][i]['wells'][x]
            showTitr = titr_data.values()
            showTitr.append(data['results'][i]['id'])
            csvwriter.writerow(showTitr)

    parsedData.close()

