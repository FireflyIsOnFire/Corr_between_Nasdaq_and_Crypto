import numpy as np
import pandas as pd
import scipy.optimize as op

class Op_Portfolio():

    def __init__(self, data_input, an_rf):

        self.data_input = data_input
        self.an_rf = an_rf

    def find(self):
        number_of_asset = len(self.data_input.columns)
        interval = len(self.data_input)
        cov_i = self.data_input.cov() * interval
        re_i = self.data_input.mean(numeric_only=True) * interval
        weights  = []
        vola = []
        SPI = []
        op_to_find = []
        op_data = []
        for i in range(100000):
            next_i = False
            while True:
                weights = np.random.random(number_of_asset)
                weights = weights/np.sum(weights)
                vola = np.sqrt(np.dot(weights.T, np.dot(cov_i, weights)))
                re = np.dot(re_i, weights)
                sharpe = (re - self.an_rf*interval)/vola

                for returns, volatilities in op_to_find:
                    if (returns > re) & (volatilities < vola):
                        next_i = True
                        break

                if next_i:
                    break
                op_to_find.append([re, vola, sharpe, weights])

        op_to_find= pd.DataFrame(op_to_find)['returns', 'volatilities', 'SPI', 'weights']
        print(op_to_find)




