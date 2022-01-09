from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
import pandas as pd
import datetime

class PlotHourlyWeekendOutput(StageOutput):

    def __init__(self, plot):
        self.plot = plot

    def get_data(self):
        return self.plot


class PlotHourlyWeekend(Stage):

    FIRST_SATURDAY = datetime.datetime(2013, 11, 2)
    FIRST_SUNDAY = datetime.datetime(2013, 11, 3)

    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:

        weekday = previous.get_data().groupby(by=['weekend', 'hour']).mean()[0:24]
        weekday = weekday.reset_index()
        aggregated_weekday = weekday[TRAFFIC_TYPES].mean(axis=1)

        weekend = previous.get_data().groupby(by=['weekend', 'hour']).mean()[24::]
        weekend = weekend.reset_index()
        aggregated_weekend = weekend[TRAFFIC_TYPES].mean(axis=1)

        result = pd.DataFrame(columns=['weekday', 'weekend'])
        result['weekday'] = aggregated_weekday
        result['weekend'] = aggregated_weekend

        return PlotHourlyWeekendOutput(result.plot())


