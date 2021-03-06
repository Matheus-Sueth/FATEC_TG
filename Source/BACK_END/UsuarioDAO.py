import sqlite3 as sql
from BACK_END.Usuario import Usuario
from BACK_END.Colecao import Colecao
import base64

class UsuarioDAO:
    def __init__(self,banco):
        self.__banco = banco
        self.__banco_conectado = sql.connect(self.__banco)
        self.__cursor = self.__banco_conectado.cursor()

    @property
    def banco(self):
        return self.__banco

    @banco.setter
    def banco(self,novo_banco):
        self.__banco = novo_banco

    @property
    def cursor(self):
        return self.__cursor

    def inserir_dados(self, novo_usuario: Usuario):
        encoded = (base64.b64encode(novo_usuario.senha.encode('ascii')))
        novo_usuario.senha = encoded.decode('ascii')
        self.__cursor.execute(f'INSERT INTO usuario VALUES({novo_usuario.id},"{novo_usuario.nome}","{novo_usuario.email}","{novo_usuario.senha}","{novo_usuario.foto}")')
        self.__banco_conectado.commit()

    def ler_dados(self):
        lista_usuarios = []
        banco_usuarios = self.__cursor.execute('SELECT * FROM usuario')
        banco_usuarios = banco_usuarios.fetchall()
        if len(banco_usuarios) > 0:
            if len(banco_usuarios[0]) != 5:
                return False
        for id, usuario in enumerate(banco_usuarios):
            if None in usuario:
                return True
        for usuario in banco_usuarios:
            usuario = [dado for dado in usuario]
            decoded = base64.b64decode(usuario[3].encode('ascii'))
            usuario[3] = decoded.decode('ascii')
            lista_usuarios.append(Usuario(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4]))
        return Colecao(lista_usuarios,'Usuários')

    def deletar_dados(self, indice):
        self.__cursor.execute(
            f'DELETE FROM usuario WHERE id={indice}')
        self.__banco_conectado.commit()