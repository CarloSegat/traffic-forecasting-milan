from settings import TRAFFIC_TYPES
from src.abstract.stage_output import StageOutput
import numpy as np

class PredictionOutput(StageOutput):

    def __init__(self, y_test, predictions):
        self.y_test = y_test
        self.predictions = predictions
        self.residuals = predictions - y_test
        self.rmse = {}

        for f in TRAFFIC_TYPES:
            if f in y_test.columns and f in predictions.columns:
                squared = np.sqrt(np.sum(np.square((y_test[f] - predictions[f]))) / len(y_test[f]))
                self.rmse[f] = squared

    def get_data(self):
        return self