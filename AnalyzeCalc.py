import pandas as pd
import numpy as np
from itertools import product
import warnings


# Median calculation
def calc_median(dataframe, column):
    medians = dataframe[column].median()
    return medians

# Standard deviation calculation
def calc_std(dataframe, column):
    stds = dataframe[column].std()
    return stds

# Numpy median calculation with error handling
def np_median(lst):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return np.median(np.array(lst))

# Calculate median absolute deviation (MAD)
def mad(dataframe, column):
    median_list = []
    median = dataframe[column].median()
    for i in dataframe[column]:
        dev = abs(i - median)
        median_list.append(dev)
    return np_median(median_list)

# Calculate modified Z-score
def mod_zscore(i, mad, dataframe, column):
    median = dataframe[column].median()
    score = ((i - median)/mad)
    return score

# Column and row ranges
cnums = range(1, 25)
rnums = range(1, 17)

export_path = raw_input('Enter PATH of export file: ')
assay_path = raw_input('Enter PATH of assay barcode file: ')
final_path = raw_input('Enter PATH of output file: ')
include_std = raw_input('Do you have standard control wells? [Y/N] ').upper()

df = pd.read_csv(export_path)
df1 = pd.read_csv(assay_path)
bcode_ser = pd.Series(df1['Plate Barcode'])


# Column medians and standard deviations
col_med = []
for x, i in product(bcode_ser, cnums):
        colnum_iso = df[(df['Plate Barcode'] == x) & (df['Adj Substance ID'] == 'Sample') & (df['Column'] == i)]
        data1 = pd.DataFrame({'Plate Barcode': colnum_iso['Plate Barcode'], 'Column': colnum_iso['Column'], 'Col_Med': calc_median(colnum_iso, 'Unknown %Inh'), 'Col_STD': calc_std(colnum_iso, 'Unknown %Inh'), 'Row': colnum_iso['Row']})
        col_med.append(data1)

# Row medians and standard deviations
row_med = []
for y, i in product(bcode_ser, rnums):
        rownum_iso = df[(df['Plate Barcode'] == y) & (df['Adj Substance ID'] == 'Sample') & (df['Row'] == i)]
        data2 = pd.DataFrame({'Plate Barcode': rownum_iso['Plate Barcode'], 'Row': rownum_iso['Row'], 'Row_Med': calc_median(rownum_iso, 'Unknown %Inh'), 'Row_STD': calc_std(rownum_iso, 'Unknown %Inh'), 'Column': rownum_iso['Column']})
        row_med.append(data2)

# Plate medians and standard deviations AND Calculation of modified Z-score for each sample well in a plate for all plates
bcode_med = []
zscore = []
for z in bcode_ser:
    bcode_iso = df[(df['Plate Barcode'] == z) & (df['Adj Substance ID'] == 'Sample')]
    data3 = pd.DataFrame({'Plate Barcode': bcode_iso['Plate Barcode'], 'Plate_Med': calc_median(bcode_iso, 'Unknown %Inh'), 'Plate_STD': calc_std(bcode_iso, 'Unknown %Inh'), 'Column': bcode_iso['Column'], 'Row': bcode_iso['Row']})
    bcode_med.append(data3)
    madder = mad(bcode_iso, 'Unknown Data')
    for i,r in bcode_iso.iterrows():
        data5 = pd.DataFrame({'Plate Barcode': r['Plate Barcode'], 'Modified ZScore': mod_zscore(r['Unknown Data'], madder, bcode_iso, 'Unknown Data'), 'Column': r['Column'], 'Row': r['Row']}, index=[i])
        zscore.append(data5)

# Well medians and standard deviations
well_med = []
for c, r in product(cnums, rnums):
        well_iso = df[(df['Column'] == c) & (df['Row'] == r)]
        data4 = pd.DataFrame({'Plate Barcode': well_iso['Plate Barcode'], 'Well_Med': calc_median(well_iso, 'Unknown %Inh'), 'Well_STD': calc_std(well_iso, 'Unknown %Inh'), 'Column': well_iso['Column'], 'Row': well_iso['Row']})
        well_med.append(data4)

# Dataframes containing each median calculations for each plate
column_medians = pd.concat(col_med)
row_medians = pd.concat(row_med)
bcode_medians = pd.concat(bcode_med)
well_medians = pd.concat(well_med)
zscores = pd.concat(zscore)

# Multiple joins to merge original dataframe with those containing median/SD calculations
frame1 = pd.merge(df, column_medians, on=['Plate Barcode', 'Column', 'Row'])
frame2 = pd.merge(frame1, row_medians, on=['Plate Barcode', 'Column', 'Row'])
frame3 = pd.merge(frame2, bcode_medians, on=['Plate Barcode', 'Column', 'Row'])
frame4 = pd.merge(frame3, well_medians, on=['Plate Barcode', 'Column', 'Row'])
frame5 = pd.merge(frame4, zscores, on=['Plate Barcode', 'Column', 'Row'])

# Appending of control wells for each plate to the final frame
if include_std == 'N':
    control_hpe = df[(df['Adj Substance ID'] == 'High')]
    control_zpe = df[(df['Adj Substance ID'] == 'Low')]
    final_frame = pd.concat([frame5, control_hpe, control_zpe])
    final_frame.to_csv(final_path, index=False)
elif include_std == 'Y':
    control_hpe = df[(df['Adj Substance ID'] == 'High')]
    control_zpe = df[(df['Adj Substance ID'] == 'Low')]
    control_std = df[(df['Adj Substance ID'] == 'STD')]
    final_frame = pd.concat([frame5, control_hpe, control_zpe, control_std])
    final_frame.to_csv(final_path, index=False)
