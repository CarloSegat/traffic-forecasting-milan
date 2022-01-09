from abc import ABC, abstractmethod


class StageOutput(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass
