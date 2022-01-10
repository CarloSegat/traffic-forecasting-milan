from settings import training_days, test_days
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
import matplotlib.pyplot as plt
import pandas as pd
from src.stages.output.prediction_output import PredictionOutput


class RunTBATS(Stage):
    def __init__(self, cell_id):
        self.cell_id = cell_id

    def compute(self, previous: StageOutput) -> StageOutput:
        from tbats import TBATS
        df = previous.get_data()

        df = df.loc[df['square_id'] == self.cell_id].reset_index()
        y_to_train = df.set_index('timestamp')['sms_in'][0:training_days*24]
        y_true = df.set_index('timestamp')['sms_in'][training_days * 24:]
        estimator = TBATS(seasonal_periods=(24, 24*7), use_box_cox=False, use_arma_errors=True, n_jobs=1)
        model = estimator.fit(y_to_train)
        # Forecast 365 days ahead
        y_forecast = model.forecast(steps=test_days*24)
        plt.plot(y_forecast)
        plt.plot(y_true.values)
        plt.show()
        prediction_frame = pd.DataFrame(y_forecast, columns=['sms_in']).reset_index()
        true_frame = pd.DataFrame(y_true, columns=['sms_in']).reset_index()
        output = PredictionOutput(true_frame, prediction_frame)
        print(4)