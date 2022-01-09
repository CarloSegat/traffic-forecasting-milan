from typing import List

from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class Pipeline:

    def __init__(self, name):
        self.name = name
        self.first_stage: Stage = None
        self.stages: List[Stage] = []
        self.result = None

    def add_stage(self, stage: Stage):
        if self.first_stage == None:
            self.first_stage = stage
        else:
            self.stages.append(stage)

    def run(self) -> StageOutput:
        print(f"Pipeline <{self.name}> started")
        output = self.first_stage.compute(None) # first stage doesnt depend on previous output
        for stage in self.stages:
            output = stage.compute(output)
        self.result = output

    def get(self):
        return self.result.get_data()




