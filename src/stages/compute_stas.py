from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.load_data import LoadDataOutput
import pandas as pd

from src.stages.output.df_output import DfOutput


class ComputeStats(Stage):

    def __init__(self):
        pass

    def compute(self, previous: LoadDataOutput) -> StageOutput:
        raw = previous.get_data()
        describe = raw.describe()
        return DfOutput(describe)
