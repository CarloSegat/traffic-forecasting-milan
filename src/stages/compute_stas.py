from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.load_data import LoadDataOutput
import pandas as pd


class ComputeStats(Stage):

    def __init__(self):
        pass

    def compute(self, previous: LoadDataOutput) -> StageOutput:
        raw = previous.get_data()
        describe = raw.describe()
        return ComputeStatsOutput(describe, raw)


class ComputeStatsOutput(StageOutput):

    def __init__(self, stats, raw):
        self.raw = raw
        self.stats = stats


    def get_data(self):
        return self.stats

    def get_raw_data(self):
        return self.raw
