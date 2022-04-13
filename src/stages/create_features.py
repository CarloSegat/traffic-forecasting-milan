from settings import national_holidays
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.output.df_output import DfOutput


class CreateFeatures(Stage):
    def __init__(self, features=None):
        if features is None:
            features = ['weekend', 'day', 'hour']
        self.features = features

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        if 'hour' in self.features:
            df['hour'] = df['timestamp'].apply(
                lambda t: t.hour)

        if 'day' in self.features:
            df['day'] = df['timestamp'].apply(
                lambda t: t.weekday())

        if 'weekend' in self.features:
            df['weekend'] = df['timestamp'].apply(
                lambda t: t.weekday() >= 5) # sat & sun are 5 & 6 resp.
        if 'national_holidays' in self.features:
            df['national_holiday'] = df['timestamp'].apply(
                lambda t: any(map(lambda n_hol : n_hol[0] == t.day and n_hol[1] == t.month, national_holidays))

            )

        return DfOutput(df)
