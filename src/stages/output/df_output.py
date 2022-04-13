from src.abstract.stage_output import StageOutput


class DfOutput(StageOutput):

    """
    The output of a stage that simply outputs a pandas dataframe
    """

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df