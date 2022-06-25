class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha: str, foto: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__foto = foto

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

if __name__ == '__main__':
    a = Usuario(1,'1','1','1','1')
    print(a.foto)
