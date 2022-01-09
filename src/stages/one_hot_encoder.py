import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class OneHotEncoderOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df

class OneHotEncode(Stage):
    def __init__(self, categorical_features=[]):
        self.categorical_features = categorical_features


    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()

        one_hot_encoder = OneHotEncoder(handle_unknown='ignore')

        frame = pd.DataFrame(one_hot_encoder.fit_transform(df[self.categorical_features]).toarray())
        print("frame.shape after 1hot ", frame.shape)
        result = df.join(frame)
        result = result.drop(columns=self.categorical_features)
        renamings = {}
        for i in range(0,7):
            renamings[i] = 'day_' + str(i+1)
        for i in range(0,25):
            renamings[i+7] = 'hour_' + str(i)
        renamings[7+25] = 'national_holiday'

        result = result.rename(columns=renamings)

        return OneHotEncoderOutput(result)