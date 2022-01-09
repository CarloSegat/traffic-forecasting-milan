from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput

class AggregateTimestampOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df


class AggregateTimestamp(Stage):

    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data().groupby('timestamp').sum()
        return AggregateTimestampOutput(df)