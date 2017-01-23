import pandas as pd

export_path = raw_input('Enter PATH of export file: ')
assay_path = raw_input('Enter PATH of assay barcode file: ')
final_path = raw_input('Enter PATH of output file: ')
stat_path = raw_input('Enter the PATH of the plate statistics file: ')

df = pd.read_csv(export_path)
df1 = pd.read_csv(assay_path)


substance = pd.Series(df['Substance ID'])

# Replace all Control* Substance IDs with general name
plate_stats = []
new_substance = []
for w in substance:
    if 'High' in w:
        sample = w.replace(w, 'High')
        new_substance.append(sample)
    elif 'Low' in w:
        sample = w.replace(w, 'Low')
        new_substance.append(sample)
    elif 'Inhibitor' in w:
        sample = w.replace(w, 'STD')
        new_substance.append(sample)
    elif 'WXHTS' in w:
        sample = w.replace(w, 'Sample')
        new_substance.append(sample)
    else:
        new_substance.append(w)
        plate_stats.append(w)

stat_list = []
for p in plate_stats:
    stats = df[(df['Substance ID'] == p)]
    trimmed_stats = pd.DataFrame({'Substance ID': stats['Substance ID'], 'Z-Factor': stats['Z-Factor'],
                                  'X/Y': stats['X/Y']})
    stat_list.append(trimmed_stats)

stat_table = pd.concat(stat_list)

# Add new column to the original DataFrame
df['Adj Substance ID'] = new_substance

# Merge Barcode information from barcode file into working DataFrame and write to file
final_frame = pd.merge(df, df1, left_on='Plate', right_on='Plate Number')
stat_frame = pd.merge(stat_table, df1, left_on='Substance ID', right_on='Plate Name')
final_frame.to_csv(final_path, index=False)
stat_frame.to_csv(stat_path, index=False)
