from models.categoria import Categoria
from database import Database
import logging

class CategoriaService:
    """Gerencia as categorias no banco de dados"""

    logger = logging.getLogger("CategoriaService")

    @classmethod
    def listar_categorias(cls):
        """Retorna a lista de todas as categorias"""
        session = Database.get_session()
        try:
            categorias = session.query(Categoria).all()
            return [categoria.to_dict() for categoria in categorias]
        finally:
            session.close()

    @classmethod
    def criar_categoria(cls, nome):
        """Cria uma nova categoria"""
        session = Database.get_session()
        try:
            if not nome:
                raise ValueError("Nome da categoria é obrigatório!")

            categoria_existente = session.query(Categoria).filter_by(nome=nome).first()
            if categoria_existente:
                raise ValueError("Já existe uma categoria com esse nome!")

            nova_categoria = Categoria(nome=nome)
            session.add(nova_categoria)
            session.commit()
            session.refresh(nova_categoria)

            cls.logger.info(f"Categoria criada: {nova_categoria.nome}")
            return nova_categoria.to_dict()

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao criar categoria: {e}")
            raise Exception("Erro ao criar categoria")
        finally:
            session.close()

    @classmethod
    def atualizar_categoria(cls, categoria_id, nome):
        """Atualiza o nome de uma categoria"""
        session = Database.get_session()
        try:
            categoria = session.query(Categoria).filter_by(id=categoria_id).first()
            if not categoria:
                raise ValueError("Categoria não encontrada!")

            categoria.nome = nome
            session.commit()
            return categoria.to_dict()

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar categoria: {e}")
        finally:
            session.close()
