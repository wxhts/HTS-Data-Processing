import pandas as pd
import glob

dir_path = raw_input('Enter PATH of directory: ')
output_path = raw_input('Enter PATH of output directory: ')
num_destination = int(raw_input('Enter how many destination plates: '))

report_files = glob.glob(dir_path + '\*.csv')

count = 0
for files in report_files:
    count += 1
    bigframe = pd.read_csv(files, keep_default_na=True, error_bad_lines=False).dropna(subset=['CompoundID'])

    for x in range(1, num_destination + 1):
        destinationplate = bigframe[bigframe['Name'] == 'Destination_' + str(x)]
        if destinationplate.empty == False:
            destinationplate.to_csv(output_path + '\destination' + str(count) + '.csv', index=False)











