from src.abstract.stage_output import StageOutput


class DfOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df