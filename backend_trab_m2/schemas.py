from datetime import date
from typing import List
from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nome : str
    email : str
    path_foto : str = ""

class UsuarioCreate(UsuarioBase):
    senha : str
    cpf : str # sem mascara

class Usuario(UsuarioBase):
    id : int

    class Config:
        orm_mode = True

class UsuarioLoginSchema(BaseModel):
    email : str
    senha : str
    class Config:
        schema_extra = {
            "example": {
                "email" : "x@x.com",
                "senha" : "pass"
            }
        }

class PaginatedUsuario(BaseModel):
    limit : int
    offset : int
    data : List['Usuario']



class ProprietarioBase(UsuarioBase):
    pass

class ProprietarioCreate(UsuarioCreate):
    pass

class Proprietario(ProprietarioBase):
    id : int

    class Config:
        orm_mode = True

class PaginatedProprietario(BaseModel):
    limit : int
    offset : int
    data : List['Proprietario']



class CorretorBase(UsuarioBase):
    percentual_comissao : float

class CorretorCreate(UsuarioCreate):
    percentual_comissao : float

class Corretor(CorretorBase):
    id : int

    class Config:
        orm_mode = True

class PaginatedCorretor(BaseModel):
    limit : int
    offset : int
    data : List['Corretor']



class TagBase(BaseModel):
    nome : str
    tipo : bool

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id : int

    class Config:
        orm_mode = True

class PaginatedTag(BaseModel):
    limit : int
    offset : int
    data : List['Tag']



class EnderecoBase(BaseModel):
    numero : int
    cep : str # sem mascara

class EnderecoCreate(EnderecoBase):
    pass

class Endereco(EnderecoBase):
    id : int

    class Config:
        orm_mode = True

class PaginatedEndereco(BaseModel):
    limit : int
    offset : int
    data : List['Endereco']
    
    

class ImovelBase(BaseModel):
    id_proprietario : int
    id_endereco : int
    nome : str
    tipo : int
    valor : float
    descricao : str
    tamanho : int
    quartos : int
    vagas : int
    banheiros : int
    disponivel : bool
    path_foto : str

class ImovelCreate(ImovelBase):
    id_tags : List[int] = list()

class Imovel(ImovelBase):
    id : int
    proprietario : 'Proprietario' = {}
    endereco : 'Endereco' = {}
    tags : List['Tag'] = list()

    class Config:
        orm_mode = True

class PaginatedImovel(BaseModel):
    limit : int
    offset : int
    data : List['Imovel']



class TelefoneBase(BaseModel):
    id_usuario : int
    numero : str # com mascara
    tipo : int

class TelefoneCreate(TelefoneBase):
    pass

class Telefone(TelefoneBase):
    id : int
    usuario : 'Usuario' = {}

    class Config:
        orm_mode = True

class PaginatedTelefone(BaseModel):
    limit : int
    offset : int
    data : List['Telefone']



class TransacaoBase(BaseModel):
    id_corretor : int
    id_imovel : int
    data : date
    valor_total : float

class TransacaoCreate(TransacaoBase):
    pass

class Transacao(TransacaoBase):
    id : int
    corretor : 'Corretor' = {}
    imovel : 'Imovel' = {}

    class Config:
        orm_mode = True

class PaginatedTransacao(BaseModel):
    limit : int
    offset : int
    data : List['Transacao']
