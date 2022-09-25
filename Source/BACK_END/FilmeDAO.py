import sqlite3 as sql
from Source.BACK_END.Filme import Filme
from Source.BACK_END.Colecao import Colecao
from Source.BACK_END.Banco import Banco

class FilmeDAO(Banco):
    def __init__(self, banco):
        super().__init__(banco)

    def inserir_dados(self, usuario_id, filme=Filme):
        try:
            self.cursor.execute(f"INSERT INTO filmes VALUES('{filme.id}',{usuario_id},'{filme.titulo}',{filme.ano},'{filme.nota}','{filme.genero}','{filme.extensao}','{filme.cam_filme}','{filme.cam_imagem}',{filme.assistido},'{filme.sinopse}')")
            self.banco_conectado.commit()
        except Exception as e:
            print(f"INSERT INTO filmes VALUES('{filme.id}',{usuario_id},'{filme.titulo}',{filme.ano},'{filme.nota}','{filme.genero}','{filme.extensao}','{filme.cam_filme}','{filme.cam_imagem}',{filme.assistido},'{filme.sinopse}')")
            print(e)
            exit()

    def ler_dados(self, usuario_id):
        lista = []
        self.cursor.execute(f'SELECT * FROM filmes WHERE usuario_id == {usuario_id}')
        result = self.cursor.fetchall()
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
        self.cursor.execute(f'SELECT * FROM filmes WHERE usuario_id == {usuario_id} ORDER BY titulo, ano')
        result = self.cursor.fetchall()
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

    def alterar_dados(self, indice, filme=Filme, usuario_id=0):
        self.cursor.execute(f"UPDATE filmes SET titulo = '{filme.titulo}', ano = {filme.ano}, nota = '{filme.nota}', genero = '{filme.genero}', extensao = '{filme.extensao}', cam_filme = '{filme.cam_filme}', cam_imagem = '{filme.cam_imagem}', sinopse = '{filme.sinopse}' WHERE id = {indice} and usuario_id = {usuario_id}")
        self.banco_conectado.commit()

    def deletar_dados(self, indice):
        self.cursor.execute(f'DELETE FROM filmes WHERE id="{indice}"')
        self.banco_conectado.commit()

    def procurar_filmes(self, coluna, texto):
        lista = []
        texto_procurado = ''
        if coluna == 'titulo' or coluna == 'sinopse':
            aux = [auxiliar for auxiliar in texto]
            texto = '%'.join(aux)
        if coluna != 'ano':
            texto_procurado = f' LIKE "%{texto}%"'
        else:
            texto_procurado = f' == {texto}'
        self.cursor.execute(f'SELECT * FROM filmes WHERE "{coluna}"{texto_procurado}')
        result = self.cursor.fetchall()
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

    def alterar_like_dados(self, valor, id):
        self.cursor.execute(f'UPDATE filmes SET qtd_assistido = {valor} WHERE id = {id}')
        self.banco_conectado.commit()
