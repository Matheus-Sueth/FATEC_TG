import sqlite3 as sql
from BACK_END.Filme import Filme
from BACK_END.Colecao import Colecao

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
        return Colecao(lista, 'Filmes')

    def ler_dados_ordenados(self, usuario_id):
        lista = []
        self.__cursor.execute(f'SELECT * FROM filmes WHERE usuario_id == {usuario_id} ORDER BY titulo, ano')
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
        return Colecao(lista,'Filmes')

    def alterar_like_dados(self, valor, id):
        self.__cursor.execute(f'UPDATE filmes SET qtd_assistido = {valor} WHERE id = {id}')
        self.__banco_conectado.commit()

    def alterar_dados(self, indice, filme=Filme, usuario_id=0):
        self.__cursor.execute(f'UPDATE filmes SET titulo = "{filme.titulo}", ano = {filme.ano}, nota = "{filme.nota}", genero = "{filme.genero}", extensao = "{filme.extensao}", cam_filme = "{filme.cam_filme}", cam_imagem = "{filme.cam_imagem}", sinopse = "{filme.sinopse}" WHERE id = {indice} and usuario_id = {usuario_id}')
        self.__banco_conectado.commit()

    def deletar_dados(self, indice):
        self.__cursor.execute(
            f'DELETE FROM filmes WHERE id="{indice}"')
        self.__banco_conectado.commit()

    def procurar_filmes(self, coluna, texto):
        lista = []
        aux = [auxiliar for auxiliar in texto]
        texto2 = '%'.join(aux)
        self.__cursor.execute(f'SELECT * FROM filmes WHERE "{coluna}" LIKE "%{texto2}%"')
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
        return Colecao(lista, f'Filmes ordenados pela coluna: {coluna}')
