import os

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from settings import COMPUTEDDIR, TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class PlotGlobalCF(Stage):

    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.set_index('timestamp')
        for f in TRAFFIC_TYPES:
            plot_acf(df[f].values, lags=48).savefig(
                os.path.join(COMPUTEDDIR, 'correlation_plots', 'global', f'{f}_acf.png'))
            plot_pacf(df[f].values, lags=48).savefig(
                os.path.join(COMPUTEDDIR, 'correlation_plots', 'global', f'{f}_pacf.png'))