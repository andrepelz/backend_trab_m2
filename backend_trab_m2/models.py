from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import date
from typing import List

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id        : Mapped[int] = mapped_column(primary_key=True, index=True)
    nome      : Mapped[str] = mapped_column(nullable=False)
    email     : Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    senha     : Mapped[str] = mapped_column(nullable=False)
    cpf       : Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    path_foto : Mapped[str] = mapped_column()
    tipo      : Mapped[str] = mapped_column()

    telefone : Mapped['Telefone'] = relationship(back_populates='usuario')

    __mapper_args__ = {
        "polymorphic_identity" : "usuario",
        "polymorphic_on" : "tipo"
    }

class Proprietario(Usuario):
    __tablename__ = 'proprietario'

    id : Mapped[int] = mapped_column(ForeignKey('usuario.id'), primary_key=True)

    imoveis : Mapped[List['Imovel']] = relationship(back_populates='proprietario')
    
    __mapper_args__ = {
        "polymorphic_identity" : "proprietario"
    }

class Corretor(Usuario):
    __tablename__ = 'corretor'
    
    id                  : Mapped[int]   = mapped_column(ForeignKey('usuario.id'), primary_key=True)
    percentual_comissao : Mapped[float] = mapped_column()

    transacoes : Mapped[List['Transacao']] = relationship(back_populates='corretor')
    
    __mapper_args__ = {
        "polymorphic_identity" : "corretor"
    }



class Imovel(Base):
    __tablename__ = 'imovel'

    id              : Mapped[int]   = mapped_column(primary_key=True, index=True)
    id_proprietario : Mapped[int]   = mapped_column(ForeignKey('proprietario.id'), nullable=False)
    id_endereco     : Mapped[int]   = mapped_column(ForeignKey('endereco.id'), nullable=False)
    nome            : Mapped[str]   = mapped_column(nullable=False)
    tipo            : Mapped[int]   = mapped_column(nullable=False)
    valor           : Mapped[float] = mapped_column(nullable=False)
    descricao       : Mapped[str]   = mapped_column()
    tamanho         : Mapped[int]   = mapped_column(nullable=False)
    quartos         : Mapped[int]   = mapped_column(nullable=False)
    vagas           : Mapped[int]   = mapped_column(nullable=False)
    banheiros       : Mapped[int]   = mapped_column(nullable=False)
    disponivel      : Mapped[bool]  = mapped_column(nullable=False)
    path_foto       : Mapped[str]   = mapped_column()

    proprietario : Mapped['Proprietario'] = relationship(back_populates='imoveis')
    endereco     : Mapped['Endereco']     = relationship(back_populates='imovel')
    tags         : Mapped[List['Tag']]    = relationship(secondary='imovel_tag', back_populates='imoveis')
    transacao    : Mapped['Transacao']    = relationship(back_populates='imovel')

class Tag(Base):
    __tablename__ = 'tag'

    id   : Mapped[int]  = mapped_column(primary_key=True, index=True)
    nome : Mapped[str]  = mapped_column(nullable=False)
    tipo : Mapped[bool] = mapped_column(nullable=False)

    imoveis : Mapped[List['Imovel']] = relationship(secondary='imovel_tag', back_populates='tags')

ImovelTag = Table('imovel_tag', Base.metadata, 
    Column('id_imovel', ForeignKey('imovel.id'), primary_key=True),
    Column('id_tag', ForeignKey('tag.id'), primary_key=True)
)



class Telefone(Base):
    __tablename__ = 'telefone'

    id         : Mapped[int] = mapped_column(primary_key=True, index=True)
    id_usuario : Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=False)
    numero     : Mapped[str] = mapped_column(nullable=False)
    tipo       : Mapped[int] = mapped_column(nullable=False)

    usuario : Mapped['Usuario'] = relationship(back_populates='telefone')

class Endereco(Base):
    __tablename__ = 'endereco'

    id     : Mapped[int] = mapped_column(primary_key=True, index=True)
    numero : Mapped[int] = mapped_column(nullable=False)
    cep    : Mapped[str] = mapped_column(nullable=False)

    imovel : Mapped['Imovel'] = relationship(back_populates='endereco')



class Transacao(Base):
    __tablename__ = 'transacao'

    id          : Mapped[int]   = mapped_column(primary_key=True, index=True)
    id_corretor : Mapped[int]   = mapped_column(ForeignKey('corretor.id'), nullable=False)
    id_imovel   : Mapped[int]   = mapped_column(ForeignKey('imovel.id'), nullable=False)
    data        : Mapped[date]  = mapped_column(nullable=False)
    valor_total : Mapped[float] = mapped_column(nullable=False)

    corretor : Mapped['Corretor'] = relationship(back_populates='transacoes')
    imovel   : Mapped['Imovel']   = relationship(back_populates='transacao')
