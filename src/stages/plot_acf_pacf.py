import os

from statsmodels.graphics.tsaplots import plot_acf

from settings import TRAFFIC_TYPES, COMPUTEDDIR
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from statsmodels.graphics.tsaplots import plot_pacf


class PlotACF(Stage):
    def __init__(self, square_id):
        self.square_id = square_id

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.loc[df['square_id'] == self.square_id]
        df = df[['timestamp', *TRAFFIC_TYPES]]
        df = df.set_index('timestamp')
        for f in TRAFFIC_TYPES:
            # df['first_difference'] = df[f].values[1:] - df[f].values[:-1]
            plot_acf(df[f].values, lags=48, title=f'acf_{f}_cell_{self.square_id}').savefig(
                os.path.join(COMPUTEDDIR, 'correlation_plots', str(self.square_id), 'acf_' + f + '.png'))
            plot_pacf(df[f].values, lags=48, title=f'pacf_{f}_cell_{self.square_id}').savefig(
                os.path.join(COMPUTEDDIR, 'correlation_plots', str(self.square_id), 'pacf_' + f + '.png'))
        print(4)

