from models.produto import Produto
from database import get_session  # ✅ Importar a função para obter uma sessão
import logging

class ProdutoService:
    """Classe responsável pelo gerenciamento de produtos no banco de dados"""
    
    logger = logging.getLogger("ProdutoService")

    @classmethod
    def listar_produtos(cls):
        """Retorna a lista de produtos como dicionário"""
        session = get_session()  # 🔥 Criar sessão dentro do método
        try:
            produtos = session.query(Produto).all()
            return [produto.to_dict() for produto in produtos]  # Retorna JSON
        finally:
            session.close()  # 🔥 Fechar sessão após uso

    @classmethod
    def adicionar_produto(cls, nome_produto, preco):
        """Adiciona um produto ao banco de dados se não existir um com o mesmo nome"""
        session = get_session()  # 🔥 Criar sessão dentro do método
        try:
            produto_existente = session.query(Produto).filter_by(nome=nome_produto).first()
            if produto_existente:
                cls.logger.warning(f"Produto já existe: {nome_produto}")
                raise ValueError("Já existe um produto com esse nome!")

            if not nome_produto or preco is None:
                cls.logger.warning("Tentativa de adicionar produto com dados inválidos.")
                raise TypeError("Tentativa de adicionar dados inválidos.")

            # Criar novo produto
            novo_produto = Produto(nome=nome_produto, preco=preco)
            session.add(novo_produto)
            session.commit()
            session.refresh(novo_produto)  # 🔥 Atualizar produto com ID gerado pelo banco
            cls.logger.info(f"Produto adicionado: {novo_produto.nome}, Preço: {novo_produto.preco}")

            return novo_produto.to_dict()  # Retorna um dicionário!

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao adicionar produto: {e}")
            raise Exception("Erro ao tentar adicionar produto")
        finally:
            session.close()  # 🔥 Fechar sessão após uso

    @classmethod
    def atualizar_dados(cls, produto_id, produto_nome=None, produto_preco=None):
        """Atualiza nome e/ou preço de um produto pelo ID"""
        session = get_session()
        try:
            produto = session.query(Produto).filter_by(id=produto_id).first()

            if not produto:
                raise ValueError("Produto não encontrado!")

            if produto_nome:
                produto.nome = produto_nome
            if produto_preco:
                produto.preco = produto_preco

            session.commit()
            return produto.to_dict()

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar produto: {e}")
        finally:
            session.close()

    @classmethod
    def remover_produto(cls, produto_id):
        """Remove um produto pelo ID"""
        session = get_session()
        try:
            produto = session.query(Produto).filter_by(id=produto_id).first()

            if not produto:
                raise ValueError("Produto não encontrado!")

            session.delete(produto)
            session.commit()
            return {"mensagem": f"Produto '{produto.nome}' removido com sucesso!"}

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao tentar remover produto: {e}")
        finally:
            session.close()
