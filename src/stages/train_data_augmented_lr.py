from settings import TRAFFIC_TYPES
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.output.df_output import DfOutput


class MakeTrainDataAugmentedLR(Stage):

    def __init__(self, cell_id):
        self.cell_id = cell_id

    def compute(self, previous: StageOutput) -> StageOutput:
        df = previous.get_data()
        df = df.loc[df['square_id'] == self.cell_id].reset_index()
        k = 24

        import warnings
        warnings.filterwarnings("ignore")

        for f in TRAFFIC_TYPES:
            for i in range(0, k):
                df[f"{f}_{i}"] = None

        # adj_dfs = {}

        # for adj_cell in get_adjacent_cell_ids(self.cell_id):
        #     adj_dfs[adj_cell] = previous.get_data().loc[previous.get_data()['square_id'] == adj_cell].reset_index()
            # for f in TRAFFIC_TYPES:
            #     df[f"adj_{adj_cell}_{f}"] = None

        for datapoint in range(k, len(df)):
            for f in TRAFFIC_TYPES:
                for i in range(0, k):
                    df.at[datapoint, f"{f}_{i}"] = df.at[datapoint - 1 - i, f]
                # for adj_cell in get_adjacent_cell_ids(self.cell_id):
                #     df.at[datapoint, f"adj_{adj_cell}_{f}"] = adj_dfs[adj_cell].at[datapoint-1, f]
        return DfOutput(df[k:])