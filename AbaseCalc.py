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
cnums = range(1, 45)
rnums = range(1, 33)

export_path = raw_input('Enter PATH of export file: ')
assay_path = raw_input('Enter PATH of assay barcode file: ')
final_path = raw_input('Enter PATH of output file: ')

df = pd.read_csv(export_path)
df1 = pd.read_csv(assay_path)
bcode_ser = pd.Series(df1['Compound Plate'])


# Column medians and standard deviations
col_med = []
for x, i in product(bcode_ser, cnums):
        colnum_iso = df[(df['Compound Plate'] == x) & (df['Adj Well Literal'] == 'Sample') & (df['Colnum'] == i)]
        data1 = pd.DataFrame({'Compound Plate': colnum_iso['Compound Plate'], 'Colnum': colnum_iso['Colnum'], 'Col_Med': calc_median(colnum_iso, '% Well Effect'), 'Col_STD': calc_std(colnum_iso, '% Well Effect'), 'Rownum': colnum_iso['Rownum']})
        col_med.append(data1)

# Row medians and standard deviations
row_med = []
for y, i in product(bcode_ser, rnums):
        rownum_iso = df[(df['Compound Plate'] == y) & (df['Adj Well Literal'] == 'Sample') & (df['Rownum'] == i)]
        data2 = pd.DataFrame({'Compound Plate': rownum_iso['Compound Plate'], 'Rownum': rownum_iso['Rownum'], 'Row_Med': calc_median(rownum_iso, '% Well Effect'), 'Row_STD': calc_std(rownum_iso, '% Well Effect'), 'Colnum': rownum_iso['Colnum']})
        row_med.append(data2)

# Plate medians and standard deviations AND Calculation of modified Z-score for each sample well in a plate for all plates
bcode_med = []
zscore = []
for z in bcode_ser:
    bcode_iso = df[(df['Compound Plate'] == z) & (df['Adj Well Literal'] == 'Sample')]
    data3 = pd.DataFrame({'Compound Plate': bcode_iso['Compound Plate'], 'Plate_Med': calc_median(bcode_iso, '% Well Effect'), 'Plate_STD': calc_std(bcode_iso, '% Well Effect'), 'Colnum': bcode_iso['Colnum'], 'Rownum': bcode_iso['Rownum']})
    bcode_med.append(data3)
    madder = mad(bcode_iso, 'Data')
    for i,r in bcode_iso.iterrows():
        data5 = pd.DataFrame({'Compound Plate': r['Compound Plate'], 'Modified ZScore': mod_zscore(r['Data'], madder, bcode_iso, 'Data'), 'Colnum': r['Colnum'], 'Rownum': r['Rownum']}, index=[i])
        zscore.append(data5)

# Well medians and standard deviations
well_med = []
for c, r in product(cnums, rnums):
        well_iso = df[(df['Colnum'] == c) & (df['Rownum'] == r)]
        data4 = pd.DataFrame({'Compound Plate': well_iso['Compound Plate'], 'Well_Med': calc_median(well_iso, '% Well Effect'), 'Well_STD': calc_std(well_iso, '% Well Effect'), 'Colnum': well_iso['Colnum'], 'Rownum': well_iso['Rownum']})
        well_med.append(data4)

# Dataframes containing each median calculations for each plate
column_medians = pd.concat(col_med)
row_medians = pd.concat(row_med)
bcode_medians = pd.concat(bcode_med)
well_medians = pd.concat(well_med)
zscores = pd.concat(zscore)

# Multiple joins to merge original dataframe with those containing median/SD calculations
frame1 = pd.merge(df, column_medians, on=['Compound Plate', 'Colnum', 'Rownum'])
frame2 = pd.merge(frame1, row_medians, on=['Compound Plate', 'Colnum', 'Rownum'])
frame3 = pd.merge(frame2, bcode_medians, on=['Compound Plate', 'Colnum', 'Rownum'])
frame4 = pd.merge(frame3, well_medians, on=['Compound Plate', 'Colnum', 'Rownum'])
frame5 = pd.merge(frame4, zscores, on=['Compound Plate', 'Colnum', 'Rownum'])

# Appending of control wells for each plate to the final frame
control_hpe = df[(df['Adj Well Literal'] == 'HPE')]
control_zpe = df[(df['Adj Well Literal'] == 'ZPE')]

final_frame = pd.concat([frame5, control_hpe, control_zpe])

final_frame.to_csv(final_path, index=False)
