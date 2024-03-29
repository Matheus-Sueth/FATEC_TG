from email_validator import validate_email
from os.path import isfile
import re

class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha: str, foto: str):
        self.__id = id
        self.__nome = nome.strip().title()
        self.__email = email
        self.__senha = senha
        self.__foto = rf'{foto}'

    def __str__(self):
        return f'Olá, {self.__nome}'

    def __eq__(self, other):
        if (self.__email == other.email) and (self.__senha == other.senha):
            return True
        else:
            return False

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, outro_nome):
        self.__nome = outro_nome

    def eh_nome_valido(self):
        return re.match(r'^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$',self.__nome) and len(self.__nome) > 2

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, outro_email):
        self.__email = outro_email

    def eh_email_valido(self):
        try:
            validation = validate_email(self.__email, check_deliverability=False)
            self.__email = validation.email
            return True
        except:
            return False

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, outra_senha):
        self.__senha = outra_senha

    def eh_senha_valida(self):
        return not self.__senha.isspace() and len(self.__senha) > 3

    @property
    def foto(self):
        return self.__foto

    @foto.setter
    def foto(self, outra_foto):
        self.__foto = outra_foto

    def eh_foto_valida(self):
        return not self.__foto.isspace() and isfile(self.__foto)
