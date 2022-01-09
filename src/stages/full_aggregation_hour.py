import glob

from settings import DATADIR
from src.abstract.pipeline import Pipeline
from src.abstract.stage import Stage
import pandas as pd

from src.abstract.stage_output import StageOutput
from src.stages.single_aggregation_hour import AggregateHourly
from src.stages.compute_stas import ComputeStats
from src.stages.load_data import LoadData


class FullAggregationHourOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df


class FullHourAggregation(Stage):

    def __init__(self, folder, file_regex):
        self.file_regex = file_regex
        self.folder = folder
        self.pipelines: list[Pipeline] = []
        self.day = 0
        for filename in glob.iglob(self.folder + '/**/' + self.file_regex, recursive=True):
            p = Pipeline("Process one day")
            p.add_stage(LoadData(filename, ['square_id', 'timestamp', 'country_code', 'sms_in', 'sms_out', 'call_in', 'call_out',
                        'internet'], offset_hour=True))
            p.add_stage(AggregateHourly())
            self.pipelines.append(p)

    def compute(self, previous: StageOutput):
        result = pd.DataFrame()
        for p in self.pipelines:
            self._print_progress()
            p.run()
            result = result.append(p.get())
        return FullAggregationHourOutput(result)

    def _print_progress(self):
        m = f"{self.day + 1} / {len(self.pipelines)} completed"
        print("\r", m, end="", flush=True)
        self.day += 1
