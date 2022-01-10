import pandas as pd

from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.output.prediction_output import PredictionOutput


class PerformAugmentedLinearRegression(Stage):
    def __init__(self, model):
        self.model = model

    def compute(self, previous: StageOutput) -> StageOutput:

        x = previous.get_data().x_train
        y = previous.get_data().y_train
        self.model.fit(x, y)

        x_test = previous.get_data().x_test.reset_index(drop=True)
        y_test = previous.get_data().y_test
        y_test = y_test.reset_index(drop=True)

        last_pred = self.model.predict(x_test.loc[[0], :])
        last_pred = pd.DataFrame(last_pred, columns=TRAFFIC_TYPES)

        predictions = last_pred

        for t in range(1, len(y_test)):
            for i in range(0, 24):
                for f in TRAFFIC_TYPES:
                    x_test.at[t+i, f"{f}_{23-i}"] = last_pred[f].values[0]
            last_pred = self.model.predict(x_test.loc[[t], :])
            last_pred = pd.DataFrame(last_pred, columns=TRAFFIC_TYPES)
            predictions = predictions.append(last_pred)

        return PredictionOutput(y_test, predictions.reset_index(drop=True))