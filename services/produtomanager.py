from models.produto import Produto
from database import Database
from util.logger_util import get_logger

class ProdutoService:
    """Classe responsável pelo gerenciamento de produtos no banco de dados"""
    
    logger = get_logger("ProdutoService")

    @classmethod
    def listar_produtos(cls, apenas_ativos=True):
        """Retorna a lista de produtos (ativos por padrão)"""
        session = Database.get_session()
        try:
            query = session.query(Produto)
            if apenas_ativos:
                query = query.filter_by(ativo=True)
            produtos = query.all()
            return [produto.to_dict() for produto in produtos]
        finally:
            session.close()

    @classmethod
    def criar_produto(cls, nome, preco, estoque, categoria_id):
        """Cria e adiciona um novo produto no banco de dados"""
        session = Database.get_session()
        try:
            if not nome or preco is None or estoque is None or not categoria_id:
                raise ValueError("Nome, preço, estoque e categoria são obrigatórios!")

            if preco < 0 or estoque < 0:
                raise ValueError("Preço e estoque devem ser valores positivos!")

            produto_existente = session.query(Produto).filter_by(nome=nome).first()
            if produto_existente:
                raise ValueError("Já existe um produto com esse nome!")

            novo_produto = Produto(
                nome=nome, preco=preco, quantidade_estoque=estoque, categoria_id=categoria_id, ativo=True
            )
            session.add(novo_produto)
            session.commit()
            session.refresh(novo_produto)

            cls.logger.info(f"Produto criado: {novo_produto.nome}, Preço: {novo_produto.preco}, Estoque: {estoque}")
            return novo_produto.to_dict()

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao criar produto: {e}")
            raise Exception("Erro ao criar produto")
        finally:
            session.close()

    @classmethod
    def atualizar_dados(cls, produto_id, nome=None, preco=None, estoque=None, ativo=None, categoria_id=None):
        """Atualiza um produto pelo ID"""
        session = Database.get_session()
        try:
            produto = session.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ValueError("Produto não encontrado!")

            if nome:
                produto.nome = nome
            if preco is not None:
                if preco < 0:
                    raise ValueError("O preço não pode ser negativo!")
                produto.preco = preco
            if estoque is not None:
                if estoque < 0:
                    raise ValueError("O estoque não pode ser negativo!")
                produto.quantidade_estoque = estoque
            if ativo is not None:
                produto.ativo = ativo
            if categoria_id:
                produto.categoria_id = categoria_id

            session.commit()
            return produto.to_dict()

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar produto: {e}")
        finally:
            session.close()

    @classmethod
    def desativar_produto(cls, produto_id):
        """Desativa um produto sem removê-lo"""
        session = Database.get_session()
        try:
            produto = session.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ValueError("Produto não encontrado!")

            if not produto.ativo:
                raise ValueError("O produto já está desativado!")

            produto.ativo = False
            session.commit()
            return {"mensagem": f"Produto '{produto.nome}' foi desativado!"}

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao desativar produto: {e}")
        finally:
            session.close()

    @classmethod
    def reativar_produto(cls, produto_id):
        """Reativa um produto inativo"""
        session = Database.get_session()
        try:
            produto = session.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                raise ValueError("Produto não encontrado!")

            if produto.ativo:
                raise ValueError("O produto já está ativo!")

            produto.ativo = True
            session.commit()
            return {"mensagem": f"Produto '{produto.nome}' foi reativado!"}

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao reativar produto: {e}")
        finally:
            session.close()
