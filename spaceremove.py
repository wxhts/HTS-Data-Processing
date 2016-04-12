import pandas as pd

df = pd.read_csv('C:\Users\IVtB Lab\Desktop\LOPAC_Ver-384.csv').dropna(subset=['Name'])

df.to_csv('C:\Users\IVtB Lab\Desktop\LOPAC_Ver-384clean.csv', index=False)


