__author__ = 'David Itenberg'

import pandas as pd

export_path = raw_input('Enter PATH of export file: ')
assay_path = raw_input('Enter PATH of assay barcode file: ')
final_path = raw_input('Enter PATH of output file: ')

df = pd.read_csv(export_path)
df1 = pd.read_csv(assay_path)
wells = pd.Series(df['Well Reference'])
well_lit = pd.Series(df['Well Literal'])
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'

# Split row and column sequentially and append to lists
colnum = []
letters = []
for i in wells:
    nums = int(i.strip(alpha))
    lett = i.strip(num)
    colnum.append(nums)
    letters.append(lett)

# Map row number to alpha index and some logic
rownums = []
for l in letters:
    if l == 'AA':
        n = 27
    elif l == 'AB':
        n = 28
    elif l == 'AC':
        n = 29
    elif l == 'AD':
        n = 30
    elif l == 'AE':
        n = 31
    elif l == 'AF':
        n = 32
    elif l in alpha:
        n = alpha.index(l) + 1
    rownums.append(n)

# Replace all Obj* Well Literal with 'Sample'
new_lit = []
for w in well_lit:
    if 'Obj' in w:
        sample = w.replace(w, 'Sample')
        new_lit.append(sample)
    else:
        new_lit.append(w)

# Add lists as new columns to dataframe
df['Colnum'] = colnum
df['Rownum'] = rownums
df['Adj Well Literal'] = new_lit

# Join Assay Plate barcodes to working DataFrame using Compound Plate barcode as key
final_frame = pd.merge(df, df1, left_on='Plate Id', right_on='Compound Plate')

final_frame.to_csv(final_path, index=False)

