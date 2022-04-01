from abc import ABC, abstractmethod


class BaseSerializer(ABC):
    @abstractmethod
    def dumps(self, obj: any) -> str:
        pass
    @abstractmethod
    def dump(self, obj: any, file_path: str):
        pass
    @abstractmethod
    def loads(self, source: str) -> any:
        pass
    @abstractmethod
    def load(self, file_path: str) -> any:
        pass