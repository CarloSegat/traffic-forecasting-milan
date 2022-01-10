from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from sklearn.linear_model import LinearRegression

import pandas as pd

from src.stages.output.prediction_output import PredictionOutput


class PerformLinearRegression(Stage):

    def __init__(self):
        self.model = None

    def compute(self, previous: StageOutput) -> StageOutput:
        self.model = LinearRegression()
        x = previous.get_data().x_train
        y = previous.get_data().y_train

        self.model.fit(x, y)

        x_test = previous.get_data().x_test
        y_test = previous.get_data().y_test
        y_test = y_test.reset_index(drop=True)
        predictions = self.model.predict(x_test)
        predictions = pd.DataFrame(predictions, columns=TRAFFIC_TYPES)

        return PredictionOutput(y_test, predictions)


