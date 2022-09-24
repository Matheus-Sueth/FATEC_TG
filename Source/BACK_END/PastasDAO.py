import sqlite3 as sql
from BACK_END.Pastas import Pasta
from BACK_END.Colecao import Colecao
from BACK_END.UsuarioDAO import Usuario

class PastaDAO:
    def __init__(self,banco):
        self.__banco = banco
        self.__banco_conectado = sql.connect(self.__banco)
        self.__cursor = self.__banco_conectado.cursor()

    @property
    def banco(self):
        return self.__banco

    @banco.setter
    def banco(self, novo_banco):
        self.__banco = novo_banco

    @property
    def cursor(self):
        return self.__cursor

    def validar_pastas(self, pasta: Pasta, ambiente: str):
        if not pasta.validar_caminho_imagem():
            if ambiente == 'PRD':
                return False
            raise Exception('Diretório de imagens não foi encontrado')

        if not pasta.validar_caminho_filme():
            if ambiente == 'PRD':
                return False
            raise Exception('Diretório de filmes não foi encontrado')
        return True

    def inserir_pastas(self, pasta:Pasta, usuario:Usuario, ambiente='PRD'):
        auxiliar = self.validar_pastas(pasta, ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        self.__cursor.execute(f'SELECT * FROM pastas WHERE usuario_id == {usuario.id}')
        result = self.__cursor.fetchall()
        if len(result) > 0:
            if ambiente == 'PRD':
                return False
            raise Exception(f'O usuário {usuario.nome} já possui pastas cadastradas')
        self.__cursor.execute(
            f'INSERT INTO pastas (usuario_id,filme,imagem,banco) VALUES("{pasta.usuario_id}","{pasta.caminho_filme}","{pasta.caminho_imagem}","{pasta.caminho_banco}")')
        if ambiente == 'PRD':
            self.__banco_conectado.commit()
        return True

    def ler_pastas_usuario(self, usuario:Usuario, ambiente='PRD'):
        self.__cursor.execute(f'SELECT * FROM pastas WHERE usuario_id == {usuario.id}')
        result = self.__cursor.fetchall()[0]
        if len(result) == 0:
            if ambiente == 'PRD':
                return False
            raise Exception(f'Nenhuma pasta foi encontrada para o usuário {usuario.nome}')
        return Pasta(result[0],result[1],result[2],result[3],result[4])

    def alterar_pastas(self, pasta_antiga: Pasta, pasta_alterada: Pasta, usuario:Usuario, ambiente='PRD'):
        auxiliar = self.validar_pastas(pasta_antiga, ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        auxiliar = self.validar_pastas(pasta_alterada, ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        auxiliar = self.ler_pastas_usuario(usuario, ambiente)
        if type(auxiliar) != Pasta:
            if ambiente == 'PRD':
                return False
            raise Exception(f'Nem a pasta nem o usuário {usuario.nome} foram encontrados')
        self.__cursor.execute(
            f"UPDATE usuario SET usuario_id = '{pasta_alterada.usuario_id}', filme = '{pasta_alterada.filme}', imagem = '{pasta_alterada.imagem}', banco = '{pasta_alterada.banco}' WHERE id = {pasta_antiga.id}")
        if ambiente == 'PRD':
            self.__banco_conectado.commit()
        return True

    def deletar_pastas(self, pasta:Pasta, usuario:Usuario, ambiente='PRD'):
        auxiliar = self.validar_pastas(pasta, ambiente)
        if ambiente == 'PRD' and not auxiliar:
            return False
        auxiliar = self.ler_pastas_usuario(usuario, ambiente)
        if type(auxiliar) != Pasta:
            if ambiente == 'PRD':
                return False
            raise Exception(f'Nem a pasta nem o usuário {usuario.nome} foram encontrados')
        self.__cursor.execute(
            f'DELETE FROM pastas WHERE id = {pasta.id}')
        if ambiente == 'PRD':
            self.__banco_conectado.commit()
        return True