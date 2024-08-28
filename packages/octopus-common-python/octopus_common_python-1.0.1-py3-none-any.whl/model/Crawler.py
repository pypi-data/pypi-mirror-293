from abc import abstractmethod

from model import ResultDetail


class Crawler:
    @abstractmethod
    def crawl(self) -> ResultDetail:
        pass
