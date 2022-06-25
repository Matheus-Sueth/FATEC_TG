import sqlite3 as sql
from BACK_END.Filme import Filme

class FilmeDAO:
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

    def inserir_dados(self, usuario_id, filme=Filme):
        self.__cursor.execute(f"INSERT INTO filmes VALUES('{filme.id}',{usuario_id},'{filme.titulo}',{filme.ano},'{filme.nota}','{filme.genero}','{filme.extensao}','{filme.cam_filme}','{filme.cam_imagem}',{filme.assistido},'{filme.sinopse}')")
        self.__banco_conectado.commit()

    def ler_dados(self, usuario_id):
        lista = []
        self.__cursor.execute(f'SELECT * FROM filmes WHERE usuario_id == {usuario_id}')
        result = self.__cursor.fetchall()
        for dados in result:
            filme = Filme(
                id=dados[0],
                titulo=dados[2],
                ano=dados[3],
                nota=dados[4],
                genero=dados[5],
                extensao=dados[6],
                cam_filme=dados[7],
                cam_imagem=dados[8],
                valor=dados[9],
                sinopse=dados[10])
            lista.append(filme)
        return lista

    def ler_dados_ordenados(self):
        self.__cursor.execute('SELECT * FROM filmes ORDER BY titulo, ano')
        result = self.__cursor.fetchall()
        for dados in result:
            filme = Filme(
                id=dados[0],
                titulo=dados[2],
                ano=dados[3],
                nota=dados[4],
                genero=dados[5],
                extensao=dados[6],
                cam_filme=dados[7],
                cam_imagem=dados[8],
                valor=dados[9],
                sinopse=dados[10])
            lista.append(filme)
        return lista

    def alterar_like_dados(self, valor, id):
        self.__cursor.execute(f'UPDATE filmes SET qtd_assistido = {valor} WHERE id = {id}')
        self.__banco_conectado.commit()

    def procurar_filmes(self):
        self.__cursor.execute('SELECT titulo,ano,extensao FROM filmes')
        return self.__cursor.fetchall()
