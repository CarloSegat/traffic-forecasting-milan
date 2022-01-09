from src.abstract.stage_output import StageOutput
from abc import ABC, abstractmethod


class Stage(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def compute(self, previous: StageOutput) -> StageOutput:
        pass
