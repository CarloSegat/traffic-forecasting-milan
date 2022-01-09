from settings import COMPUTEDDIR
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from matplotlib import pyplot as plt
import numpy as np

class PlotGeo(Stage):
    def __init__(self):
        pass

    def compute(self, previous: StageOutput) -> StageOutput:
        # setup the figure and axes
        df = previous.get_data()
        df = df.sort_values('square_id')

        data = np.reshape(df['mean'].values, (100,100))

        fig, ax = plt.subplots()
        im = ax.imshow(data)
        ax.set_xlabel("X cell")
        ax.set_ylabel("Y cell")
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Log aggregated traffic', rotation=-90, va="bottom")
        plt.savefig(COMPUTEDDIR + '/gep_pot.png')