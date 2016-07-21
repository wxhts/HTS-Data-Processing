import pandas as pd

rawpath = raw_input('Enter the PATH of the Echo log file: ')
cleanpath = raw_input('Enter the PATH of the output file: ')

raw_echo = pd.read_csv(rawpath)

clean_echo = pd.DataFrame({'Barcode': raw_echo['Destination Plate Barcode'], 'Well': raw_echo['Destination Well'],
                           'CompoundID': raw_echo['Sample ID'], 'SourceBC': raw_echo['Source Plate Barcode']})

clean_echo.to_csv(cleanpath, index=False)
