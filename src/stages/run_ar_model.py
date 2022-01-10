from statsmodels.tsa.arima_model import ARMA

from settings import TRAFFIC_TYPES, end_training, end_timestamp
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
import pandas as pd

from src.stages.output.prediction_output import PredictionOutput


class RunARModel(Stage):

    def __init__(self, order, cell_id):
        self.cell_id = cell_id
        self.order = order

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.set_index('timestamp')
        cell_df = df.loc[df['square_id'] == self.cell_id]

        training_hours = cell_df[:end_training]
        test_hours = cell_df[end_training:]

        result = pd.DataFrame(columns=TRAFFIC_TYPES)

        for f in TRAFFIC_TYPES:
            temp_ = training_hours[f]
            mf = ARMA(temp_, order=(self.order, 0)).fit()
            # print(mf.summary())
            predictions = mf.predict(start=end_training, end=end_timestamp)
            assert len(predictions) == len(test_hours[f])
            result[f] = predictions
        return PredictionOutput(test_hours[TRAFFIC_TYPES], result)
            # residuals = test_hours[f] - predictions
            # rmse = mean_squared_error(test_hours[f], predictions, squared=False)
            # mean_abs_percent_error = round(np.mean(abs(residuals / test_hours[f])), 4)

            # plt.figure(figsize=(10, 4))
            # plt.plot(test_hours[f])
            # plt.plot(predictions)
            # plt.legend(("Data", "Predictions"))
            # plt.show()
            # print(mean_abs_percent_error)