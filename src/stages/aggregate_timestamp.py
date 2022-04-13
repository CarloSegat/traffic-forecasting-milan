from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.output.df_output import DfOutput


class CellAggregationByTimestamp(Stage):

    """
    Sums the hourly aggregated traffic at each cell.
    I.e. it takes 100*100 parallel time series and merges them into one
    (for each traffic measurment)
    """

    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data().groupby('timestamp').sum()
        return DfOutput(df)