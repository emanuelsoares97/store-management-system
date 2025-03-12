from models.abstrata import EntidadeBase
from util.logger_util import get_logger

class Produto(EntidadeBase):
    def __init__(self, id, nome, preco):
        super().__init__(id)  # ID já vem da EntidadeBase
        self._nome = nome
        self._preco = preco
        self.logger = get_logger(self.__class__.__name__)

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome):
        if not novo_nome.strip():
            raise ValueError("O nome do produto não pode estar vazio!")
        self._nome = novo_nome

    @property
    def preco(self):
        return self._preco
    
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco > 0:
            self._preco = novo_preco
            self.logger.info(f"Preço alterado: {self._preco}")
        else:
            self.logger.warning("Tentativa de definir preço negativo!")
            raise ValueError("O preço deve ser positivo.")
        
    def to_dict(self):
        """transforma em um dicionario"""
        try:
            self.logger.info(f"Produto convertido para dicionario, {self.nome} | {self.preco}")
            return {
                "id": self.id, 
                "nome":self.nome, 
                "preco":self.preco
                }
            
        except Exception as e:
            self.logger.error(f"Erro ao tentar converter para um dicionario, erro: {e}")
    
    @classmethod
    def from_dict(cls, data):
        """retorna um dicionario"""
        return cls(data["id"], data["nome"], data["preco"])