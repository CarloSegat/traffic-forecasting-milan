from typing import List

from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput


class Pipeline:

    def __init__(self, name):
        self.name = name
        self.first_stages: List[Stage] = None
        self.stages: List[List[Stage]] = []
        self.result = None
        self.stage_index = 1

    def add_stage(self, stage: type, zip_like: List):
        if self.first_stages == None:
            for args_group in zip_like:
                self.first_stages.add(stage(args_group))
        else:
            self.stages[self.stage_index] = []
            for args_group in zip_like:
                self.stages[self.stage_index].add(stage(args_group))
            self.stage_index += 1

    def run(self) -> StageOutput:
        print(f"Pipeline <{self.name}> started")
        outputs = []
        for first_stage in self.first_stages:
            outputs.add(self.first_stages.compute(None)) # first stage doesnt depend on previous output
        for stages in self.stages:
            temp_outputs = []
            assert len(stages) == len(outputs)
            for stage, output in zip(stages, outputs):
                temp_outputs.add(stage.compute(output))
            outputs = temp_outputs
        self.result = output

    def get(self):
        return self.result.get_data()




