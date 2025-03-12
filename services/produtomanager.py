from util.logger_util   import get_logger
from gestãoprodutos.tratamentolista import  guardar_lista, carregar_lista
from models.produto import Produto

class ProdutoManager:
    """classe para CRUD"""
    def __init__(self):
        self.listaprodutos=carregar_lista()
        self.logger=get_logger(self.__class__.__name__)

    def gerar_novo_id(self):
        """Gera um novo ID único baseado no maior ID existente"""
        if not self.listaprodutos:  # Se a lista estiver vazia, começa do 1
            return 1
        return max(produto["id"] for produto in self.listaprodutos) + 1  # Pega o maior ID e soma 1


    def _validar_produto(self, nome_produto):
        for produto in self.listaprodutos:
            if produto.nome == nome_produto:
                return produto
        return None
    
    def adicionar_produto(self, nome_produto, preco):
        """Adiciona um produto sem IDs duplicados"""
        try:
            novo_id = self.gerar_novo_id()  # Gera um ID automático
            novo_produto = Produto(novo_id, nome_produto, preco)
            self.listaprodutos.append(novo_produto.to_dict())  # Adiciona como dicionário
            guardar_lista(self.listaprodutos)  # Salva no JSON
            self.logger.info(f"Produto adicionado com sucesso: {novo_produto.nome}")
        except Exception as e:
            self.logger.error(f"Erro ao tentar adicionar produto: {e}")
            raise "Erro ao tentar adicionar produto"




    
    def mostrar_produtos(self):
        """lista de todos os produtos"""
        for produto in self.listaprodutos:
            print(f"Produto: {produto.nome} | Preço: {produto.preco}")


    def atualizar_produto(self, id, novo_nome=None, novo_preco=None):
        """Atualiza nome e/ou preço do produto pelo ID"""
        produto_encontrado = False
        for produto in self.listaprodutos:
            if produto["id"] == id:
                if novo_nome:
                    produto["nome"] = novo_nome
                if novo_preco:
                    produto["preco"] = novo_preco
                produto_encontrado = True
                break  # Produto encontrado, podemos sair do loop

        if not produto_encontrado:
            return False  # Retorna falso se o produto não for encontrado

        guardar_lista(self.listaprodutos)  # Salva a lista atualizada no JSON
        return True  # Retorna verdadeiro se foi atualizado


    def remover_produto_id(self, id):
        self.logger.info(f"Antes da remoção: {self.listaprodutos}")
        self.listaprodutos=[produto for produto in self.listaprodutos if produto["id"]!=id]
        self.logger.info(f"Depois da remoção: {self.listaprodutos}")
        guardar_lista(self.listaprodutos)

