import csv
from bokeh.charts import HeatMap, output_file, show
from bokeh.io import gridplot
from bokeh.palettes import RdYlBu5
import pandas as pd
from createWellIndex import createWellIndex
from EnVisualize import EnVisualize


def tuplize(alist):
    """Generates a list of 2-element lists"""
    tuped = []
    for i in range(0, len(alist), 2):
        tuped.append([alist[i], alist[i+1]])
    return tuped

input_file = raw_input('Please enter the PATH of the input file: ')
log_file = raw_input('Please enter the PATH of the log file: ')
project_code = raw_input('Please enter your project code: ')
project_date = raw_input('Please enter the date: ')
stats_output = raw_input('Please enter the PATH of the plate statistics file: ')
inhibitions_output = raw_input('Please enter the PATH of the percent inhibitions file: ')
viz_output = raw_input('Please enter the PATH of the visualization file: ')

plate_stats = open(stats_output + ' ' + project_code + ' ' + project_date + '.csv', 'wb')
csvwriter = csv.writer(plate_stats)
headers = ['Barcode', 'HPE CV', 'ZPE CV', 'Z-Prime', 'S/B']
csvwriter.writerow(headers)

collection = createWellIndex(input_file)
log = pd.read_csv(log_file)
barcodes = set(collection['Barcode'])

# Calculates the plate statistics and outputs to one file. Calculates the percent inhibitions and outputs to another file.
list_inhibitions = []
for plate1 in log.itertuples():

    assayplate = plate1[1]
    compoundplate = plate1[2]
    subset = collection[(collection['Barcode'] == assayplate)]
    workit = EnVisualize(subset)

    stats = [assayplate, workit.CV('hpe'), workit.CV('zpe'), workit.zPrime(), workit.signalToBackground()]
    csvwriter.writerow(stats)

    workit.percentInhibition()
    compound_add = workit.compoundAdder(compoundplate)
    list_inhibitions.append(compound_add)

all_inhibitions = pd.concat(list_inhibitions)
all_inhibitions.to_csv(inhibitions_output + ' ' + project_code + ' ' + project_date + '.csv', index=False)


# Generate HeatMap visualizations using Bokeh library for each plate in percent inhibitions Dataframe.
output_file(viz_output + ' ' + project_code + ' ' + project_date + '.html')
graphs = []
for plate2 in barcodes:
    aplate = all_inhibitions[(all_inhibitions['Barcode_x'] == plate2)]
    hm = HeatMap(aplate, x='Column', y='Reverse Row', values='Percent Inhibition', palette=RdYlBu5, title=plate2, stat=None, hover_tool=True)
    graphs.append(hm)

arranged_graphs = tuplize(graphs)
visualization = gridplot(arranged_graphs)
show(visualization)
