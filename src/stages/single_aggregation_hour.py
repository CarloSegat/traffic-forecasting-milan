from settings import DATADIR
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
import pandas as pd
import numpy as np

class AggregateHourlyOutput(StageOutput):

    def __init__(self, df_agg_hourly):
        self.df_agg_hourly = df_agg_hourly

    def get_data(self):
        return self.df_agg_hourly

class AggregateHourly(Stage):

    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        # previous.df['timestamp'] = previous.df['timestamp'].values.astype(dtype='datetime64[ms]')
        df = previous.get_data().drop(columns=['country_code'])

        result = df.groupby('square_id').resample('H', on='timestamp').sum()
        result = result.drop(columns=['square_id'])

        # result = previous.get_data().resample('H', on='timestamp').sum()

        # np.count_nonzero(result['square_id'] == 45)

        return AggregateHourlyOutput(result)

