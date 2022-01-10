from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class PlotMeanDayOutput(StageOutput):

    def __init__(self, plot, df):
        self.plot = plot
        self.df = df

    def get_data(self):
        return self.plot


class PlotMeanDay(Stage):

    def __init__(self, how_many_days, begin=0):
        self.begin = begin
        self.how_many_days = how_many_days

    def compute(self, previous: StageOutput):

        df = previous.get_data()
        df['hour'] = df['timestamp'].apply(lambda t: 'd' + str(t.day) + ' h' + str(t.hour))

        result = df[self.begin * 24:(self.begin * 24) + self.how_many_days * 24]\
            .plot(x='hour',
                  y=['sms_in', 'sms_out', 'call_in', 'call_out', 'internet'])
        # arange = np.arange(0, len(result.axes.lines[0].get_xdata()), 3)
        result.set_xlabel("Hour")
        result.set_ylabel("Z-score")

        return PlotMeanDayOutput(result, df)




