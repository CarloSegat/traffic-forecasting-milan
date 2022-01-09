from settings import training_days, test_days
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class RunTBATS(Stage):
    def __init__(self, cell_id):
        self.cell_id = cell_id

    def compute(self, previous: StageOutput) -> StageOutput:
        from tbats import TBATS, BATS
        df = previous.get_data()

        df = df.loc[df['square_id'] == self.cell_id].reset_index()
        y_to_train = df.set_index('timestamp')['sms_in'][0:training_days*24]
        estimator = TBATS(seasonal_periods=(24, 24*7))
        model = estimator.fit(y_to_train)
        # Forecast 365 days ahead
        y_forecast = model.forecast(steps=test_days)
        print(4)