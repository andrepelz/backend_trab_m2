from sqlalchemy.orm import Session
import exceptions
import bcrypt, models, schemas
from pydantic import BaseModel
from database import Base
from typing import List, Any

class CRUD:
    ...

class BaseCRUD(CRUD):
    @staticmethod
    def get(db : Session, id : int, model : Base, exception : exceptions.NotFoundException) -> Any:
        entity = db.query(model).get(id)
        if entity is None:
            raise exception
        return entity
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int, model : Base) -> List[Any]:
        return db.query(model).offset(offset).limit(limit).all()
    
    @staticmethod
    def create(db : Session, schema : BaseModel, model : Base, entity : Any = None) -> Any:
        if entity is None:
            entity = model(**schema.dict())
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    @staticmethod
    def update(db : Session, entity : Any, schema : BaseModel) -> Any:
        for key, value in schema.dict().items():
            setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        return entity

    @staticmethod
    def delete(db : Session, entity : Any) -> None:
        db.delete(entity)
        db.commit()
        return



class Usuario(CRUD):
    @staticmethod
    def check(db : Session, usuario : schemas.UsuarioLoginSchema):
        db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
        if db_usuario is None:
            return False
        return bcrypt.checkpw(usuario.senha.encode('utf8'), db_usuario.senha.encode('utf8'))
    
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Usuario, exceptions.UsuarioNotFoundError)
    
    @staticmethod
    def get_by_email(db : Session, email : str):
        return db.query(models.Usuario).filter(models.Usuario.email == email).first()
    
    @staticmethod
    def get_by_cpf(db : Session, cpf : str):
        return db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Usuario)

    @staticmethod
    def create(db : Session, usuario : schemas.UsuarioCreate):
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        if Usuario.get_by_email(db, usuario.email) is not None or Usuario.get_by_cpf(db, usuario.cpf) is not None:
            raise exceptions.UsuarioAlreadyExistError
        return BaseCRUD.create(db, usuario, models.Usuario)

    @staticmethod
    def update(db : Session, id : int, usuario : schemas.UsuarioCreate):
        db_usuario = Usuario.get(db, id)
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        usuario.senha = bcrypt.hashpw (
            usuario.senha.encode('utf8'), 
            bcrypt.gensalt()
        ).decode('utf8') if usuario.senha != "" else db_usuario.senha
        return BaseCRUD.update(db, db_usuario, usuario)

    @staticmethod
    def delete(db: Session, id: int):
        db_usuario = Usuario.get(db, id)
        BaseCRUD.delete(db, db_usuario)
        return

class Proprietario(CRUD):
    @staticmethod
    def check(db : Session, proprietario : schemas.UsuarioLoginSchema):
        db_proprietario = db.query(models.Proprietario).filter(models.Proprietario.email == proprietario.email).first()
        if db_proprietario is None:
            return False
        return bcrypt.checkpw(proprietario.senha.encode('utf8'), db_proprietario.senha.encode('utf8'))
    
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Proprietario, exceptions.ProprietarioNotFoundError)
    
    @staticmethod
    def get_by_email(db : Session, email : str):
        return db.query(models.Proprietario).filter(models.Proprietario.email == email).first()
    
    @staticmethod
    def get_by_cpf(db : Session, cpf : str):
        return db.query(models.Proprietario).filter(models.Proprietario.cpf == cpf).first()
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Proprietario)

    @staticmethod
    def create(db : Session, proprietario : schemas.ProprietarioCreate):
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        proprietario.senha = bcrypt.hashpw(proprietario.senha.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        if Usuario.get_by_email(db, proprietario.email) is not None or Usuario.get_by_cpf(db, proprietario.cpf) is not None:
            raise exceptions.ProprietarioAlreadyExistError
        return BaseCRUD.create(db, proprietario, models.Proprietario)

    @staticmethod
    def update(db : Session, id : int, proprietario : schemas.ProprietarioCreate):
        db_proprietario = Proprietario.get(db, id)
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        proprietario.senha = bcrypt.hashpw (
            proprietario.senha.encode('utf8'), 
            bcrypt.gensalt()).decode('utf8'
        ) if proprietario.senha != "" else db_proprietario.senha
        return BaseCRUD.update(db, db_proprietario, proprietario)

    @staticmethod
    def delete(db: Session, id: int):
        db_proprietario = Proprietario.get(db, id)
        BaseCRUD.delete(db, db_proprietario)
        return

class Corretor(CRUD):
    @staticmethod
    def check(db : Session, corretor : schemas.UsuarioLoginSchema):
        db_corretor = db.query(models.Corretor).filter(models.Corretor.email == corretor.email).first()
        if db_corretor is None:
            return False
        return bcrypt.checkpw(corretor.senha.encode('utf8'), db_corretor.senha.encode('utf8'))
    
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Corretor, exceptions.CorretorNotFoundError)
    
    @staticmethod
    def get_by_email(db : Session, email : str):
        return db.query(models.Corretor).filter(models.Corretor.email == email).first()
    
    @staticmethod
    def get_by_cpf(db : Session, cpf : str):
        return db.query(models.Corretor).filter(models.Corretor.cpf == cpf).first()
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Corretor)

    @staticmethod
    def create(db : Session, corretor : schemas.CorretorCreate):
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        corretor.senha = bcrypt.hashpw(corretor.senha.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        if Usuario.get_by_email(db, corretor.email) is not None or Usuario.get_by_cpf(db, corretor.cpf) is not None:
            raise exceptions.CorretorAlreadyExistError
        return BaseCRUD.create(db, corretor, models.Corretor)

    @staticmethod
    def update(db : Session, id : int, corretor : schemas.CorretorCreate):
        db_corretor = Corretor.get(db, id)
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        corretor.senha = bcrypt.hashpw (
            corretor.senha.encode('utf8'), 
            bcrypt.gensalt()).decode('utf8'
        ) if corretor.senha != "" else db_corretor.senha
        return BaseCRUD.update(db, db_corretor, corretor)

    @staticmethod
    def delete(db: Session, id: int):
        db_corretor = Corretor.get(db, id)
        BaseCRUD.delete(db, db_corretor)
        return



class Imovel(CRUD):
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Imovel, exceptions.ImovelNotFoundError)
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Imovel)
    
    @staticmethod
    def get_by_endereco_id(db : Session, id : int):
        return db.query(models.Imovel).filter(models.Imovel.id_endereco == id).first()

    @staticmethod
    def create(db : Session, imovel : schemas.ImovelCreate):
        db_imovel = models.Imovel(
            id_proprietario=imovel.id_proprietario,
            id_endereco=imovel.id_endereco,
            nome=imovel.nome,
            tipo=imovel.tipo,
            valor=imovel.valor,
            descricao=imovel.descricao,
            tamanho=imovel.tamanho,
            quartos=imovel.quartos,
            vagas=imovel.vagas,
            banheiros=imovel.banheiros,
            disponivel=True,
            path_foto=imovel.path_foto
        )

        try:
            db_imovel.proprietario = Imovel._check_member(db, imovel.id_proprietario, Proprietario, exceptions.ProprietarioNotFoundError)
            db_imovel.endereco = Imovel._check_member(db, imovel.id_endereco, Endereco, exceptions.EnderecoNotFoundError)
            db_imovel.tags = [ Tag.get(db, id) for id in imovel.id_tags ]
        except exceptions.NotFoundException as e:
            raise e
        
        if Imovel.get_by_endereco_id(db, imovel.id_endereco) is not None:
            raise exceptions.EnderecoAlreadyTakenError

        return BaseCRUD.create(db, imovel, models.Imovel, db_imovel)

    @staticmethod
    def update(db : Session, id : int, imovel : schemas.ImovelCreate):
        db_imovel = Imovel.get(db, id)
        try:
            db_imovel.proprietario = Imovel._check_member(db, imovel.id_proprietario, Proprietario, exceptions.ProprietarioNotFoundError)
            db_imovel.endereco = Imovel._check_member(db, imovel.id_endereco, Endereco, exceptions.EnderecoNotFoundError)
        except exceptions.NotFoundException as e:
            raise e
        
        return BaseCRUD.update(db, db_imovel, imovel)

    @staticmethod
    def delete(db: Session, id: int):
        db_imovel = Imovel.get(db, id)
        BaseCRUD.delete(db, db_imovel)
        return

    @staticmethod
    def _check_member(db : Session, id : int, member_class : CRUD, exception : exceptions.NotFoundException):
        if (entity := member_class.get(db, id)) is not None:
            return entity
        else:
            raise exception

class Tag(CRUD):
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Tag, exceptions.TagNotFoundError)
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Tag)

    @staticmethod
    def create(db : Session, tag : schemas.TagCreate):
        return BaseCRUD.create(db, tag, models.Tag)

    @staticmethod
    def update(db : Session, id : int, tag : schemas.TagCreate):
        db_tag = Tag.get(db, id)
        return BaseCRUD.update(db, db_tag, tag)

    @staticmethod
    def delete(db: Session, id: int):
        db_tag = Tag.get(db, id)
        BaseCRUD.delete(db, db_tag)
        return



class Telefone(CRUD):
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Telefone, exceptions.TelefoneNotFoundError)
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Telefone)

    @staticmethod
    def create(db : Session, telefone : schemas.TelefoneCreate):
        db_telefone = models.Telefone(**telefone.dict())
        try:
            db_telefone.usuario = Telefone._check_member(db, telefone.id_usuario, Usuario, exceptions.UsuarioNotFoundError)
        except exceptions.NotFoundException as e:
            raise e
        
        return BaseCRUD.create(db, telefone, models.Telefone, db_telefone)

    @staticmethod
    def update(db : Session, id : int, telefone : schemas.TelefoneCreate):
        db_telefone = Telefone.get(db, id)
        try:
            db_telefone.usuario = Telefone._check_member(db, telefone.id_usuario, Usuario, exceptions.UsuarioNotFoundError)
        except exceptions.NotFoundException as e:
            raise e
        
        return BaseCRUD.update(db, db_telefone, telefone)

    @staticmethod
    def delete(db: Session, id: int):
        db_telefone = Telefone.get(db, id)
        BaseCRUD.delete(db, db_telefone)
        return
    
    @staticmethod
    def _check_member(db : Session, id : int, member_class : CRUD, exception : exceptions.NotFoundException):
        if (entity := member_class.get(db, id)) is not None:
            return entity
        else:
            raise exception

class Endereco(CRUD):
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Endereco, exceptions.EnderecoNotFoundError)
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Endereco)

    @staticmethod
    def create(db : Session, endereco : schemas.EnderecoCreate):
        return BaseCRUD.create(db, endereco, models.Endereco)

    @staticmethod
    def update(db : Session, id : int, endereco : schemas.EnderecoCreate):
        db_endereco = Endereco.get(db, id)
        return BaseCRUD.update(db, db_endereco, endereco)

    @staticmethod
    def delete(db: Session, id: int):
        db_endereco = Endereco.get(db, id)
        BaseCRUD.delete(db, db_endereco)
        return



class Transacao(CRUD):
    @staticmethod
    def get(db : Session, id : int):
        return BaseCRUD.get(db, id, models.Transacao, exceptions.TransacaoNotFoundError)
    
    @staticmethod
    def get_all(db : Session, offset : int, limit : int):
        return BaseCRUD.get_all(db, offset, limit, models.Transacao)

    @staticmethod
    def create(db : Session, transacao : schemas.TransacaoCreate):
        db_transacao = models.Transacao(**transacao.dict())
        try:
            db_transacao.corretor = Transacao._check_member(db, transacao.id_corretor, Corretor, exceptions.CorretorNotFoundError)
            db_transacao.imovel = Transacao._check_member(db, transacao.id_imovel, Imovel, exceptions.ImovelNotFoundError)
        except exceptions.NotFoundException as e:
            raise e
        
        return BaseCRUD.create(db, transacao, models.Transacao, db_transacao)

    @staticmethod
    def update(db : Session, id : int, transacao : schemas.TransacaoCreate):
        db_transacao = Transacao.get(db, id)
        try:
            db_transacao.corretor = Transacao._check_member(db, transacao.id_corretor, Corretor, exceptions.CorretorNotFoundError)
            db_transacao.imovel = Transacao._check_member(db, transacao.id_imovel, Imovel, exceptions.ImovelNotFoundError)
        except exceptions.NotFoundException as e:
            raise e
        
        return BaseCRUD.update(db, db_transacao, transacao)

    @staticmethod
    def delete(db: Session, id: int):
        db_transacao = Transacao.get(db, id)
        BaseCRUD.delete(db, db_transacao)
        return
    
    @staticmethod
    def _check_member(db : Session, id : int, member_class : CRUD, exception : exceptions.NotFoundException):
        if (entity := member_class.get(db, id)) is not None:
            return entity
        else:
            raise exception
    