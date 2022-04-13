import glob

from settings import RAW_HOUR_AGGREGATION_FILE
from src.abstract.pipeline import Pipeline
from src.abstract.stage import Stage

from src.abstract.stage_output import StageOutput
from src.stages.output.df_output import DfOutput
from src.stages.single_aggregation_hour import AggregateHourly
from src.stages.load_data import LoadData

class FullHourAggregation(Stage):

    def __init__(self, folder, file_regex):
        self.file_regex = file_regex
        self.folder = folder
        self.pipelines: list[Pipeline] = []
        self.day = 0
        for filename in glob.iglob(self.folder + '/**/' + self.file_regex, recursive=True):
            p = Pipeline(f"Processing: {filename}")
            p.add_stage(LoadData(filename, ['square_id', 'timestamp', 'country_code', 'sms_in', 'sms_out', 'call_in', 'call_out',
                        'internet'], offset_hour=True))
            p.add_stage(AggregateHourly())
            self.pipelines.append(p)

    def compute(self, previous: StageOutput):

        with open(RAW_HOUR_AGGREGATION_FILE, 'a') as f:
            f.write('square_id,timestamp,sms_in,sms_out,call_in,call_out,internet\n')
        for p in self.pipelines:
            self._print_progress()
            p.run()
            result = p.get()
            with open(RAW_HOUR_AGGREGATION_FILE, 'a') as f:
                f.write(result.to_csv(index=True, header=False))

        return DfOutput(result)

    def _print_progress(self):
        m = f"{self.day + 1} / {len(self.pipelines)} completed"
        print("\r", m, end="", flush=True)
        self.day += 1
