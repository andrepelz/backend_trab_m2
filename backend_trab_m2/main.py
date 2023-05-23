from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from exceptions import *
from database import get_db, engine
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class BaseREST:
    @staticmethod
    def get(id: int, entity_class: crud.CRUD, exception: Exception, db: Session = Depends(get_db)):
        try:
            return entity_class.get(db, id)
        except exception as cie:
            raise HTTPException(**cie.__dict__)

    @staticmethod
    def get_all(entity_class: crud.CRUD, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
        entity = entity_class.get_all(db, offset, limit)
        response = {"limit": limit, "offset": offset, "data": entity}
        return response

    @staticmethod
    def create(schema: schemas.BaseModel, entity_class: crud.CRUD, exception: Exception, db: Session = Depends(get_db)):
        try:
            return entity_class.create(db, schema)
        except exception as cie:
            raise HTTPException(**cie.__dict__)

    @staticmethod
    def update(id: int, schema: schemas.BaseModel, entity_class: crud.CRUD, exception: Exception, db: Session = Depends(get_db)):
        try:
            return entity_class.update(db, id, schema)
        except exception as cie:
            raise HTTPException(**cie.__dict__)

    @staticmethod
    def delete(id: int, entity_class: crud.CRUD, exception: Exception, db: Session = Depends(get_db)):
        try:
            return entity_class.delete(db, id)
        except exception as cie:
            raise HTTPException(**cie.__dict__)

# cadastro e login
class Signup:
    @app.post("/api/signup", tags=["usuario"])
    async def usuario_signup(usuario: schemas.UsuarioCreate = Body(...), db: Session = Depends(get_db)):
        try:
            crud.Usuario.create(db, usuario)
            return signJWT(usuario.email)
        except UsuarioException as cie:
            raise HTTPException(**cie.__dict__)
        
    @app.post("/api/login", tags=["usuario"])
    async def usuario_login(usuario: schemas.UsuarioLoginSchema = Body(...), db: Session = Depends(get_db)):
        if crud.Usuario.check(db, usuario):
            return signJWT(usuario.email)
        raise HTTPException(status_code=400, detail="USUARIO_INCORRETO")

# usuario
class Usuario:
    API_STRING = '/api/usuarios/'
    DEFAULT_RESPONSE_MODEL = schemas.Usuario
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedUsuario
    ENTITY_CLASS = crud.Usuario
    EXCEPTION_TYPE = UsuarioException
    CREATE_SCHEMA = schemas.UsuarioCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)

# Proprietario
class Proprietario:
    API_STRING = '/api/proprietarios/'
    DEFAULT_RESPONSE_MODEL = schemas.Proprietario
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedProprietario
    ENTITY_CLASS = crud.Proprietario
    EXCEPTION_TYPE = ProprietarioException
    CREATE_SCHEMA = schemas.ProprietarioCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)

# Corretor
class Corretor:
    API_STRING = '/api/corretores/'
    DEFAULT_RESPONSE_MODEL = schemas.Corretor
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedCorretor
    ENTITY_CLASS = crud.Corretor
    EXCEPTION_TYPE = CorretorException
    CREATE_SCHEMA = schemas.CorretorCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)



# Imovel
class Imovel:
    API_STRING = '/api/imoveis/'
    DEFAULT_RESPONSE_MODEL = schemas.Imovel
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedImovel
    ENTITY_CLASS = crud.Imovel
    EXCEPTION_TYPE = ImovelException
    CREATE_SCHEMA = schemas.ImovelCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)

# Tag
class Tag:
    API_STRING = '/api/tags/'
    DEFAULT_RESPONSE_MODEL = schemas.Tag
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedTag
    ENTITY_CLASS = crud.Tag
    EXCEPTION_TYPE = TagException
    CREATE_SCHEMA = schemas.TagCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)



# Telefone
class Telefone:
    API_STRING = '/api/telefones/'
    DEFAULT_RESPONSE_MODEL = schemas.Telefone
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedTelefone
    ENTITY_CLASS = crud.Telefone
    EXCEPTION_TYPE = TelefoneException
    CREATE_SCHEMA = schemas.TelefoneCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)
    
# Endereco
class Endereco:
    API_STRING = '/api/enderecos/'
    DEFAULT_RESPONSE_MODEL = schemas.Endereco
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedEndereco
    ENTITY_CLASS = crud.Endereco
    EXCEPTION_TYPE = EnderecoException
    CREATE_SCHEMA = schemas.EnderecoCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)
   


# Transacao
class Transacao:
    API_STRING = '/api/transacoes/'
    DEFAULT_RESPONSE_MODEL = schemas.Transacao
    PAGINATED_RESPONSE_MODEL = schemas.PaginatedTransacao
    ENTITY_CLASS = crud.Transacao
    EXCEPTION_TYPE = TransacaoException
    CREATE_SCHEMA = schemas.TransacaoCreate

    @app.get(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def get(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.get(id, entity_class, exception, db)

    @app.get(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=PAGINATED_RESPONSE_MODEL)
    def get_all(entity_class=ENTITY_CLASS, db : Session = Depends(get_db), offset : int = 0, limit : int = 10):
        return BaseREST.get_all(entity_class, db, offset, limit)

    @app.post(f"{API_STRING}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def create(schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.create(schema, entity_class, exception, db)

    @app.put(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())], response_model=DEFAULT_RESPONSE_MODEL)
    def update(id : int, schema : CREATE_SCHEMA, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.update(id, schema, entity_class, exception, db)

    @app.delete(f"{API_STRING}{{id}}", dependencies=[Depends(JWTBearer())])
    def delete(id : int, entity_class=ENTITY_CLASS, exception=EXCEPTION_TYPE, db : Session = Depends(get_db)):
        return BaseREST.delete(id, entity_class, exception, db)
   