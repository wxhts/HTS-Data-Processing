import pandas as pd
import numpy as np


class MedianPolish:
    """ Fits an additive model using Tukey's median polish algorithm. Code referenced from
    https://github.com/borisvish/Median-Polish/blob/master/AdditiveModelFitByMedianPolish.py"""

    def __init__(self, dataframe):
        """ Takes a pandas dataframe for each compound plate using Abase formatted fields as input"""
        self.frame = dataframe

    def average(self):
        """ Calculate the average counts on the plates"""
        plate_average = self.frame['Data'].mean()
        return plate_average

    def mad(self, residuals):
        """ Calculate the Median Absolute Deviation (MAD) of the residuals from the B-score calculation"""
        median_list = []
        median = np.median(residuals)
        for i in residuals:
            dev = abs(i - median)
            median_list.append(dev)
        return np.median(np.array(median_list))

    def median_polish(self, max_iter=5):
        """ Tukey's median polish algorithm performed on a plate. Returns arrays for the row and column effects for
         each well"""
        cnums = range(5, 45)
        rnums = range(1, 33)
        count1 = 0
        count2 = 0
        row_effects = np.zeros(shape=32)
        col_effects = np.zeros(shape=44)

        while count1 <= 2 and count2 <= 2:
        #for i in range(max_iter):
            for r in rnums:
                dfr = self.frame[self.frame['Rownum'] == r]
                row_median = dfr['Data'].median()
                self.frame.ix[self.frame.Rownum == r, 'Data'] = self.frame.ix[self.frame.Rownum == r, 'Data'] - row_median
                row_effects[r-1] += row_median
            median_row_effect = np.median(row_effects)
            row_effects -= median_row_effect
            if median_row_effect == 0:
                count1 += 1

            for c in cnums:
                dfc = self.frame[self.frame['Colnum'] == c]
                col_median = dfc['Data'].median()
                self.frame.ix[self.frame.Colnum == r, 'Data'] = self.frame.ix[self.frame.Colnum == r, 'Data'] - col_median
                col_effects[c-5] += col_median
            median_col_effect = np.median(col_effects)
            col_effects -= median_col_effect
            if median_col_effect == 0:
                count2 += 1

        return row_effects, col_effects


class Bscore:
    """ Fit the B-score of a well using the B-score algorithm from
    Malo, N., Hanley, J. A., Cerquozzi, S., Pelletier, J., & Nadon, R. (2006). Statistical practice in high-throughput
    screening data analysis. Nature biotechnology, 24(2), 167-175.
    Brideau, C., Gunter, B., Pikounis, B.,
    & Liaw, A. (2003). Improved statistical methods for hit selection in high-throughput screening.
    Journal of biomolecular screening, 8(6), 634-647. """

    def __init__(self, dataframe):
        self.data = dataframe

    def bscore(self):
        inst = MedianPolish(self.data)
        effects = inst.median_polish()
        avg = inst.average()

        row_eff = effects[0]
        col_eff = effects[1]

        cnums = range(5, 45)
        rnums = range(1, 33)

        residualz = []
        for c in cnums:
            df = self.data[self.data['Colnum'] == c]
            for r in rnums:
                df2 = df[df['Rownum'] == r]
                res = int(df2['Data']) - (avg + row_eff[r-1] + col_eff[c-5])
                residualz.append(res)

        madder = inst.mad(residualz)
        bscores = []
        for i in residualz:
            score = (i/madder)
            bscores.append(score)

        return bscores
        
        
