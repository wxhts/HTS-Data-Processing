from __future__ import division
from itertools import product
import pandas as pd


class EnVisualize:
    # Methods to calculate plate statistics such as HPE and ZPE percent CVs, signal to background ratio, and Z-prime
    # from Envision plate reader data. Input "plate" should be a pandas Dataframe with row(1 - 32) and column(1-48)
    #  indexes.

    def __init__(self, plate):

        self.plate = plate
        self.avg_hpe = 0
        self.avg_zpe = 0
        self.std_hpe = 0
        self.std_zpe = 0

    def HPE_CV(self):
        """Calculates percent CV of HPE plate regions"""

        leftHPEX = range(1, 17)
        leftHPEY = range(1, 5)

        rightHPEX = range(17, 33)
        rightHPEY = range(45, 49)

        leftHPE = []
        for x, y in product(leftHPEX, leftHPEY):
            well = self.plate[(self.plate['Row'] == x) & (self.plate['Column'] == y)]
            leftHPE.append(well)

        rightHPE = []
        for x, y in product(rightHPEX, rightHPEY):
            well = self.plate[(self.plate['Row'] == x) & (self.plate['Column'] == y)]
            rightHPE.append(well)

        HPE = pd.concat([pd.concat(leftHPE), pd.concat(rightHPE)])

        seriesHPE = pd.Series(HPE['Result'])

        self.avg_hpe = seriesHPE.mean()
        self.std_hpe = seriesHPE.std()

        percentHPECV = round(100*(self.std_hpe/self.avg_hpe), 2)

        return percentHPECV

    def ZPE_CV(self):
        """Calculates percent CV of ZPE plate regions"""

        leftZPEX = range(17, 33)
        leftZPEY = range(1, 5)

        rightZPEX = range(1, 17)
        rightZPEY = range(45, 49)

        leftZPE = []
        for x, y in product(leftZPEX, leftZPEY):
            well = self.plate[(self.plate['Row'] == x) & (self.plate['Column'] == y)]
            leftZPE.append(well)

        rightZPE = []
        for x, y in product(rightZPEX, rightZPEY):
            well = self.plate[(self.plate['Row'] == x) & (self.plate['Column'] == y)]
            rightZPE.append(well)

        ZPE = pd.concat([pd.concat(leftZPE), pd.concat(rightZPE)])

        seriesZPE = pd.Series(ZPE['Result'])

        self.avg_zpe = seriesZPE.mean()
        self.std_zpe = seriesZPE.std()

        percentZPECV = round(100*(self.std_zpe/self.avg_zpe), 2)

        return percentZPECV

    def signalToBackground(self):
        """Calculates the signal to background ratio of the plate"""

        sob = round((self.avg_zpe/self.avg_hpe), 2)
        return sob

    def zPrime(self):
        """Calculates the Z-prime of the plate"""

        numerator = 3 * (self.std_zpe - self.std_hpe)
        denominator = abs(self.avg_zpe - self.avg_hpe)
        prime = 1 - (numerator/denominator)

        zprime = round(prime, 2)
        return zprime
        
        
