import pandas as pd
from src.abstract.stage import Stage

from src.abstract.stage_output import StageOutput


class LoadData(Stage):

    def __init__(self, file_name, headers=None, offset_hour=False):
        self.offset_hour = offset_hour
        self.file_name = file_name
        self.headers = headers
        self.data: StageOutput = None

    def compute(self, previous: StageOutput) -> StageOutput:
        if self.headers != None:
            self.data = pd.read_csv(self.file_name,
                                    sep='\t',
                                    header=None,
                                    names=self.headers)
        else:
            self.data = pd.read_csv(self.file_name)

        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = self.data['timestamp'].values.astype(dtype='datetime64[ms]')
            if self.offset_hour:
                self.data['timestamp'] = self.data['timestamp'] + pd.DateOffset(hours=1)

            self.data = self.data.sort_values(by='timestamp')

        return LoadDataOutput(self.data)


class LoadDataOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df
