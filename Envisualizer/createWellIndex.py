import pandas as pd


def createWellIndex(file_path):

    df = pd.read_csv(file_path)
    wells = pd.Series(df['Well'])
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
    df['Column'] = colnum
    df['Row'] = rownums

    return df
