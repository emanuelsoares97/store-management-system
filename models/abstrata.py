from abc import ABC, abstractmethod

class EntidadeBase(ABC):
    @abstractmethod
    def __init__(self, id):
        self._id=id

    @property
    def id(self):
        """O ID da entidade não pode ser alterado depois de criado"""
        return self._id

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod #de forma a não ser usado o self, e assim não requer propriamente da classe
    @abstractmethod
    def from_dict(cls, data):
        pass