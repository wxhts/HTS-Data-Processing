import pandas as pd
from Bscore import Bscore

export_path = raw_input('Enter PATH of export file: ')
assay_path = raw_input('Enter PATH of assay barcode file: ')
final_path = raw_input('Enter PATH of output file: ')

df = pd.read_csv(export_path)
df1 = pd.read_csv(assay_path)
bcode_ser = pd.Series(df1['Compound Plate'])

# Calculate Bscores for each well in 1536 well plate on a per plate basis
bscore_ls = []
for z in bcode_ser:
    bcode_iso = df[(df['Compound Plate'] == z) & (df['Adj Well Literal'] == 'Sample')]
    scores = Bscore(bcode_iso)
    data1 = pd.DataFrame({'Compound Plate': bcode_iso['Compound Plate'], 'Bscore': scores.bscore(), 'Colnum': bcode_iso['Colnum'], 'Rownum': bcode_iso['Rownum']})
    bscore_ls.append(data1)

bscores = pd.concat(bscore_ls)
frame = pd.merge(df, bscores, on=['Compound Plate', 'Colnum', 'Rownum'])

control_hpe = df[(df['Adj Well Literal'] == 'HPE')]
control_zpe = df[(df['Adj Well Literal'] == 'ZPE')]

final_frame = pd.concat([frame, control_hpe, control_zpe])
final_frame.to_csv(final_path, index=False)
