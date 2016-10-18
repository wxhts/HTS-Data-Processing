from itertools import product
import pandas as pd
from createWellIndexBiomek import createWellIndexBiomek

filesource = raw_input('Enter the PATH to export file: ')
fileout = raw_input('Enter the PATH for output file:')
plate = createWellIndexBiomek(filesource)

boundx = range(1, 17)
boundy = range(3, 23)
barcodes = set(plate['Barcode'])
sampleRegion = []

for barcode in barcodes:
    for x, y in product(boundx, boundy):
        samples = plate[(plate['Barcode'] == barcode) & (plate['Row'] == x) & (plate['Column'] == y)]
        sampleRegion.append(samples)

samplesOnly = pd.concat(sampleRegion)
sortedSamples = samplesOnly.sort_values(by=['Name', 'Row', 'Column'])

sortedSamples.to_csv(fileout, index=False)
