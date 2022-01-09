from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput

class NoNegtiveOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df


class NoNegative(Stage):
    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        for feature in ['sms_in', 'sms_out', 'call_in', 'call_out', 'internet']:
            df[feature] = df[feature] - min(df[feature])
        return NoNegtiveOutput(df)