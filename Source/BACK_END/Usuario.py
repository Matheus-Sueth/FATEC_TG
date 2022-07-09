class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha: str, foto: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__foto = foto

    def __str__(self):
        return f'Olá, {self.__nome}'

    def __eq__(self, other):
        if (self.__email == other.email) and (self.__senha == other.senha):
            return True
        elif (self.__email == other.email) and (self.__senha != other.senha):
            return False
        else:
            return None

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, outro_nome):
        self.__nome = outro_nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, outro_email):
        self.__email = outro_email

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, outra_senha):
        self.__senha = outra_senha

    @property
    def foto(self):
        return self.__foto

    @foto.setter
    def foto(self, outra_foto):
        self.__foto = outra_foto
