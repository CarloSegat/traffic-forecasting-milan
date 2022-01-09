from settings import ID_TRAFFIC_MAP_FILE, Z_NORMALISED_HOUR_FILE
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.load_data import LoadData


class MergeFilesOutput(StageOutput):

    def __init__(self, df):
        self.df = df

    def get_data(self):
        return self.df


class MergeFiles(Stage):

    def __init__(self):
        self.z_norm_stage = LoadData(Z_NORMALISED_HOUR_FILE)
        self.square_traffic = LoadData(ID_TRAFFIC_MAP_FILE)

    def compute(self, previous: StageOutput) -> StageOutput:
        z_norm_df = self.z_norm_stage.compute(None).get_data()
        square_traffic_df = self.square_traffic.compute(None).get_data()
        result = z_norm_df.merge(square_traffic_df, on='square_id', how='left')
        print("result.shape ", result.shape)
        return MergeFilesOutput(result)
