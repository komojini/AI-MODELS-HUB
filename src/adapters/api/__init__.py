from abc import ABC, abstractmethod


class APIAdapter(ABC):
    @abstractmethod
    def get(self, url):
        pass