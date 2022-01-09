from statsmodels.tsa.stattools import adfuller

from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class PerformDickeyFuller(Stage):

    def __init__(self, square_id):
        self.square_id = square_id

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.loc[df['square_id'] == self.square_id]
        df = df[['timestamp', *TRAFFIC_TYPES]]
        df = df.set_index('timestamp')
        for f in TRAFFIC_TYPES:
            if adfuller(df[f])[1] > 0.499:
                print(f"\tDickey-Fuller failed for square_id={self.square_id} and traffic feature {f}, P value is not < .5")
                exit(1)
        print(f"\tSquare_id {self.square_id} traffic measurments have all passed the Dickey-FUller test")
        return previous