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
    count2 = 0
    parsedData = open(output, 'wb')
    csvwriter = csv.writer(parsedData)

    for i in range(samples):
        for x in range(wells):
            if count1 == 0:
                hedr_data = data['results'][i]['wells'][0]
                header = hedr_data.keys()
                header.append(u'id')
                csvwriter.writerow(header)
                count1 += 1

            titr_data = data['results'][i]['wells'][x]
            showTitr = titr_data.values()
            showTitr.append(data['results'][i]['id'])
            csvwriter.writerow(showTitr)
    
    parsedData.close()
    
'''
    for j in range(samples):
        if count2 == 0:
            hedr_data = data['results'][0]
            header = hedr_data.keys()
            header.remove(u'wells')
            csvwriter.writerow(header)
            count2 += 1

        titr_data = data['results'][j]
        showTitr = titr_data.values()
        showTitr.pop(4)
        csvwriter.writerow(showTitr)
'''
