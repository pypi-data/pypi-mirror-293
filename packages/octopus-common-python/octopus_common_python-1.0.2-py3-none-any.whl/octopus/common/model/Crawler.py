from abc import abstractmethod

from octopus.common.model import ResultDetail


class Crawler:
    @abstractmethod
    def crawl(self) -> ResultDetail:
        pass
