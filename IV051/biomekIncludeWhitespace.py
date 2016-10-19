from itertools import product
import pandas as pd
from createWellIndexBiomek import createWellIndexBiomek


filesource = raw_input('Enter the PATH to export file: ')
fileout = raw_input('Enter the PATH for output directory: ')
plate = createWellIndexBiomek(filesource)

boundx = range(1, 17)
boundy = range(3, 23)
barcodes = sorted(list(set(plate['Barcode'])))
namefile = barcodes[-1]
barcode_iter = barcodes[:-1]

sampleRegion = []
for barcode in barcode_iter:
    for x, y in product(boundx, boundy):
        samples = plate[(plate['Barcode'] == barcode) & (plate['Row'] == x) & (plate['Column'] == y)]
        sampleRegion.append(samples)

samplesOnly = pd.concat(sampleRegion)
samplesOnly['Concentration'] = 7.5
SamplesOnly['1536Plate'] = namefile
sortedSamples = samplesOnly.sort_values(by=['Name', 'Row', 'Column'])

sortedSamples.to_csv(fileout + '/' + namefile + '.csv', index=False)
