import sqlite3 as sql
from BACK_END.Usuario import Usuario
from BACK_END.Colecao import Colecao
import base64
from pathlib import Path

class UsuarioDAO:
    def __init__(self,banco:str):
        self.__banco = Path(banco).absolute()
        self.__banco_conectado = sql.connect(self.__banco)
        self.__cursor = self.__banco_conectado.cursor()
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS "usuario" ("id" INTEGER, "nome" TEXT, "email" TEXT, "senha" TEXT, "foto" TEXT,'
                              ' PRIMARY KEY("id" AUTOINCREMENT))')
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS "pastas" ("id" INTEGER, "usuario_id" INTEGER, "filme" TEXT, "imagem" TEXT, "banco" TEXT,' \
            ' PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("usuario_id") REFERENCES "usuario"("id"))')
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS "filmes"'
                              ' ("id" TEXT, "usuario_id" INTEGER, "titulo" TEXT, "ano" INTEGER, "nota" TEXT, "genero" TEXT, "extensao" TEXT,'
                              ' "cam_filme" TEXT, "cam_imagem" TEXT, "qtd_assistido" INTEGER, "sinopse" TEXT,'
                              ' FOREIGN KEY("usuario_id") REFERENCES "usuario"("id"), PRIMARY KEY("id") )')

    @property
    def banco(self):
        return self.__banco

    @banco.setter
    def banco(self,novo_banco):
        self.__banco = novo_banco

    @property
    def cursor(self):
        return self.__cursor

    def validar_estrutura_banco(self, ambiente='PRD'):
        colunas = {'usuario':('id','nome','email','senha','foto'),
                   'pastas':('id', 'usuario_id', 'filme', 'imagem', 'banco'),
                   'filmes':('id', 'usuario_id', 'titulo', 'ano', 'nota', 'genero', 'extensao', 'cam_filme', 'cam_imagem', 'qtd_assistido', 'sinopse')
        }
        for chave, valor in colunas.items():
            auxiliar = self.__cursor.execute(f'SELECT * FROM {chave}')
            bd_colunas = [coluna[0] for coluna in auxiliar.description]
            if ambiente == 'PRD' and tuple(bd_colunas) != valor:
                return False
        return True

    def validar_dados_usuario(self,novo_usuario,ambiente):
        if not novo_usuario.eh_nome_valido():
            if ambiente == 'PRD':
                return False
            raise Exception('O nome não condiz com a diretrizes do sistema')

        if not novo_usuario.eh_email_valido():
            if ambiente == 'PRD':
                return False
            raise Exception('O email não condiz com a diretrizes do sistema')

        if not novo_usuario.eh_senha_valida():
            if ambiente == 'PRD':
                return False
            raise Exception('A senha não condiz com a diretrizes do sistema')

        if not novo_usuario.eh_foto_valida():
            if ambiente == 'PRD':
                return False
            raise Exception('A foto não condiz com a diretrizes do sistema')

        return True

    def inserir_dados(self, novo_usuario: Usuario, ambiente='PRD'):
        auxiliar = self.validar_dados_usuario(novo_usuario,ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        self.__cursor.execute(f'SELECT * FROM usuario WHERE email == "{novo_usuario.email}"')
        usuario_login = self.__cursor.fetchall()
        if len(usuario_login) > 0:
            if ambiente == 'PRD':
                return None
            raise Exception('Usuário foi encontrado no sistema, a criação de usuário foi cancelada')
        encoded = (base64.b64encode(novo_usuario.senha.encode('ascii')))
        novo_usuario.senha = encoded.decode('ascii')
        self.__cursor.execute(f'INSERT INTO usuario (nome,email,senha,foto) VALUES("{novo_usuario.nome}","{novo_usuario.email}","{novo_usuario.senha}","{novo_usuario.foto}")')
        if ambiente == 'PRD':
            self.__banco_conectado.commit()
        return True

    def ler_dados(self, ambiente='PRD'):
        lista_usuarios = []
        self.__cursor.execute('SELECT * FROM usuario')
        banco_usuarios = self.__cursor.fetchall()
        if ambiente == 'PRD' and len(banco_usuarios) == 0:
            return False
        for usuario in banco_usuarios:
            usuario = [dado for dado in usuario]
            decoded = base64.b64decode(usuario[3].encode('ascii'))
            usuario[3] = decoded.decode('ascii')
            lista_usuarios.append(Usuario(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4]))
        return Colecao(lista_usuarios,'Usuários')

    def ler_dados_usuario(self, usuario: Usuario, ambiente='PRD'):
        auxiliar = self.validar_dados_usuario(usuario, ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        self.__cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario.email}"')
        usuario_login = self.__cursor.fetchall()
        if len(usuario_login) == 0:
            if ambiente == 'PRD':
                return None
            raise Exception('Nenhum usuário foi encontrado no sistema')
        usuario_login = [dado for dado in usuario_login[0]]
        decoded = base64.b64decode(usuario_login[3].encode('ascii'))
        usuario_login[3] = decoded.decode('ascii')
        return Usuario(usuario_login[0],usuario_login[1],usuario_login[2],usuario_login[3],usuario_login[4])

    def alterar_dados(self, usuario_antigo: Usuario, usuario_alterado: Usuario, ambiente='PRD'):
        auxiliar = self.validar_dados_usuario(usuario_alterado, ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        self.__cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario_antigo.email}"')
        usuario_login = self.__cursor.fetchall()
        if len(usuario_login) == 0:
            if ambiente == 'PRD':
                return False
            raise Exception('Nenhum usuário foi encontrado no sistema')
        self.__cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario_alterado.email}"')
        usuario_login = self.__cursor.fetchall()
        if len(usuario_login) > 0:
            if ambiente == 'PRD':
                return False
            raise Exception('E-mail já está cadastrado no sistema')
        encoded = (base64.b64encode(usuario_alterado.senha.encode('ascii')))
        usuario_alterado.senha = encoded.decode('ascii')
        self.__cursor.execute(
            f"UPDATE usuario SET nome = '{usuario_alterado.nome}', email = '{usuario_alterado.email}', senha = '{usuario_alterado.senha}', foto = '{usuario_alterado.foto}' WHERE id = {usuario_antigo.id}")
        if ambiente == 'PRD':
            self.__banco_conectado.commit()
        return True

    def deletar_dados(self, usuario: Usuario, ambiente='PRD'):
        self.__cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario.email}"')
        usuario_login = self.__cursor.fetchall()
        if len(usuario_login) == 0:
            if ambiente == 'PRD':
                return False
            raise Exception('Nenhum usuário foi encontrado no sistema')
        self.__cursor.execute(
            f'DELETE FROM usuario WHERE id={usuario.id}')
        if ambiente == 'PRD':
            self.__banco_conectado.commit()
        return True
