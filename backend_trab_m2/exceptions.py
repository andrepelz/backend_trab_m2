class NotFoundException(Exception):
    ...

class AlreadyExistException(Exception):
    ...


class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "USUARIO_NAO_ENCONTRADO"

class UsuarioAlreadyExistError(UsuarioException, AlreadyExistException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_OU_CPF_DUPLICADO"



class ProprietarioException(UsuarioException):
    ...

class ProprietarioNotFoundError(ProprietarioException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "PROPRIETARIO_NAO_ENCONTRADO"

class ProprietarioAlreadyExistError(ProprietarioException, AlreadyExistException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_OU_CPF_DUPLICADO"



class CorretorException(UsuarioException):
    ...

class CorretorNotFoundError(CorretorException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "CORRETOR_NAO_ENCONTRADO"

class CorretorAlreadyExistError(CorretorException, AlreadyExistException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_OU_CPF_DUPLICADO"



class ImovelException(Exception):
    ...

class ImovelNotFoundError(ImovelException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "IMOVEL_NAO_ENCONTRADO"



class TagException(Exception):
    ...

class TagNotFoundError(TagException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "TAG_NAO_ENCONTRADA"



class EnderecoException(Exception):
    ...

class EnderecoNotFoundError(EnderecoException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "ENDERECO_NAO_ENCONTRADO"



class TelefoneException(Exception):
    ...

class TelefoneNotFoundError(TelefoneException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "TELEFONE_NAO_ENCONTRADO"
  


class TransacaoException(Exception):
    ...

class TransacaoNotFoundError(TransacaoException, NotFoundException):
    def __init__(self):
        self.status_code = 404
        self.detail = "TRANSACAO_NAO_ENCONTRADA"
