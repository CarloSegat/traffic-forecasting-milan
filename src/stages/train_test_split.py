from sklearn.model_selection import train_test_split

from settings import end_training, training_days
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class TestTrainSplitOutput(StageOutput):
    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def get_data(self):
        return self



class TestTrainSplit(Stage):
    def __init__(self, target_column_names, cell_id):
        self.cell_id = cell_id
        self.target_column_names = target_column_names

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.loc[df['square_id'] == self.cell_id]
        if 'index' in df.columns:
            df = df.drop(columns='index')
        y = df[self.target_column_names]
        x = df.drop(columns=self.target_column_names)
        x = x.drop(columns=['square_id'])
        x = x.drop(columns=['timestamp'])
        x_train = x[:training_days*24]
        y_train = y[:training_days*24]
        x_test = x[training_days*24:]
        y_test = y[training_days*24:]
        # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=self.test_percentage, random_state=434)
        return TestTrainSplitOutput(x_train, x_test, y_train, y_test)