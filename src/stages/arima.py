from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARIMA

from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
import matplotlib.pyplot as plt

class TestIntegratedARIMA(Stage):
    def __init__(self, cell_id):
        self.cell_id = cell_id

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.loc[df['square_id'] == self.cell_id].reset_index()
        for f in TRAFFIC_TYPES:

            # I term: intergrated 1 and 2
            # do I need this? I do not have trend
            df[f'1_difference_{f}'] = df[f][0:-1].reset_index(drop=True) - df[f][1:].reset_index(drop=True)
            df[f'2_difference_{f}'] = df[f'1_difference_{f}'][0:-1].reset_index(drop=True) - df[f'1_difference_{f}'][1:].reset_index(drop=True)

            temp_0 = df.set_index('timestamp')[f].dropna()
            plot_acf(temp_0, lags=48).show()

            plt.plot(df[f'1_difference_{f}'][0:24*8])
            plt.show()
            temp_1 = df.set_index('timestamp')[f'1_difference_{f}'].dropna()
            plot_acf(temp_1, lags=48).show()

            plt.plot(df[f'2_difference_{f}'][0:24*8])
            plt.show()
            temp_2 = df.set_index('timestamp')[f'2_difference_{f}'].dropna()
            plot_acf(temp_2, lags=48).show()

            # SEASONAL DIFFERENCES & I 1

            df[f'1_difference_seasonal{f}'] = (df[f][0:].reset_index(drop=True) - df[f][24:].reset_index(drop=True)).dropna() \
                - (df[f][1:].reset_index(drop=True) - df[f][25:].reset_index(drop=True)).dropna()
            df[f'1_difference_seasonal{f}'] = df[f'1_difference_seasonal{f}'].dropna()
            plt.plot(df[f'1_difference_seasonal{f}'][0:24*8])
            plt.show()

            temp_3 = df.set_index('timestamp')[f'1_difference_seasonal{f}'].dropna()
            plot_acf(temp_3, lags=48).show()

            # SEASONAL DIFFERENCE & I 2
            df[f'2_difference_seasonal{f}'] = df[f'1_difference_seasonal{f}'][0:].reset_index(drop=True) - df[f'1_difference_seasonal{f}'][1:].reset_index(drop=True)
            df[f'2_difference_seasonal{f}'] = df[f'2_difference_seasonal{f}'].dropna()
            plt.plot(df[f'2_difference_seasonal{f}'][0:24 * 8])
            plt.show()

            temp_4 = df.set_index('timestamp')[f'2_difference_seasonal{f}'].dropna()
            plot_acf(temp_4, lags=48).show()

            # SEASONAL DAILY DIFFERENCE ALONE
            df[f'difference_seasonal{f}'] = df[f][0:].reset_index(drop=True) - df[f][24:].reset_index(drop=True)
            df[f'difference_seasonal{f}'] = df[f'difference_seasonal{f}'].dropna()
            plt.plot(df[f'difference_seasonal{f}'][0:24 * 14])
            plt.show()

            temp_5 = df.set_index('timestamp')[f'difference_seasonal{f}'].dropna()
            plot_acf(temp_5, lags=48).show()

            # SEASONAL DAILY + WEEKLY DIFFERENCE
            df[f'difference_seasonal_W_D{f}'] = df[f][0:].reset_index(drop=True) - df[f][24:].reset_index(drop=True)
            df[f'difference_seasonal_W_D{f}'] = df[f'difference_seasonal_W_D{f}'].dropna()
            df[f'difference_seasonal_W_D{f}'] = df[f'difference_seasonal_W_D{f}'][0:].reset_index(drop=True) - df[f'difference_seasonal_W_D{f}'][24*7:].reset_index(drop=True)
            plt.plot(df[f'difference_seasonal{f}'][0:24 * 14])
            plt.show()

            temp_6 = df.set_index('timestamp')[f'difference_seasonal_W_D{f}'].dropna()
            plot_acf(temp_6, lags=48).show()
            print(4)


        arima = ARIMA(1, 1, 1)
        # arima.fit()
