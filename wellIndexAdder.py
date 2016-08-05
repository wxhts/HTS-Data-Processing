import pandas as pd

export_path = raw_input('Enter PATH of export file: ')
final_path = raw_input('Enter PATH of output file: ')

df = pd.read_csv(export_path)
wells = pd.Series(df['Destination Well'])
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

# Add lists as new columns to dataframe
df['Colnum'] = colnum
df['Rownum'] = rownums

df.to_csv(final_path, index=False)
