from abc import ABC, abstractmethod

class McLiumTaskModule(ABC):
    @abstractmethod
    def create_task(self):
        pass
