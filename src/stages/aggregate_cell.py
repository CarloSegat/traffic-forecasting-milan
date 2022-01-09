from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
import numpy as np

class AggregateCellOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df


class AggregateCell(Stage):

    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data().sort_values(by='square_id')
        df = df.groupby('square_id', as_index=False).sum()
        df['mean'] = df.mean(axis=1) / min(df.mean(axis=1))
        df['mean'] = np.log(df['mean'] )
        return AggregateCellOutput(df[['square_id', 'mean']])