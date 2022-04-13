from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class ZNormaliseTraffics(Stage):

    def __init__(self, remove_square_id=True):
        self.remove_square_id = remove_square_id

    def compute(self, previous: StageOutput) -> StageOutput:
        result = previous.get_data()

        for f in TRAFFIC_TYPES:
            mean = previous.get_data()[f].mean()
            std = previous.get_data()[f].std()
            result[f] = (result[f] - mean) / std

        if 'square_id' in result.columns and self.remove_square_id:
            result = result.drop(columns=['square_id'])

        return NormaliseHourAggregationOutput(result)


class NormaliseHourAggregationOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df
