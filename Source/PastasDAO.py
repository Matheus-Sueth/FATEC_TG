import sqlite3 as sql
from Pastas import Pasta

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

    def inserir_dados(self, indice:int, id_usuario:int, pastas:Pasta):
        self.__cursor.execute(
            f'INSERT INTO pastas VALUES({indice},"{id_usuario}","{pastas.caminho_filme}","{pastas.caminho_imagem}","{pastas.caminho_banco}")')
        self.__banco_conectado.commit()

    def ler_dados(self):
        pastas = []
        self.__cursor.execute('SELECT * FROM pastas')
        result = self.__cursor.fetchall()
        for dado in result:
            pasta = Pasta(dado[2],dado[3],dado[4])
            pastas.append((dado[0],dado[1],pasta))
        return pastas

    def conferir_banco(self):
        colunas = ['id','nome','email','senha','foto']
        contador = 0
        try:
            auxiliar = self.__cursor.execute('SELECT * FROM usuario')
            for coluna in auxiliar.description:
                if not coluna[0] in colunas:
                    return False
                else:
                    contador+=1
            if contador != len(colunas):
                return False
        except:
            return False
        colunas = ['id', 'usuario_id', 'filme', 'imagem', 'banco']
        contador = 0
        try:
            auxiliar = self.__cursor.execute('SELECT * FROM pastas')
            for coluna in auxiliar.description:
                if not coluna[0] in colunas:
                    return False
                else:
                    contador+=1
            if contador != len(colunas):
                return False
        except:
            return False
        colunas = ['id', 'usuario_id', 'titulo', 'ano', 'nota', 'genero', 'extensao', 'cam_filme', 'cam_imagem', 'qtd_assistido', 'sinopse']
        contador = 0
        try:
            auxiliar = self.__cursor.execute('SELECT * FROM filmes')
            for coluna in auxiliar.description:
                if not coluna[0] in colunas:
                    return False
                else:
                    contador+=1
                    continue
            if contador != len(colunas):
                return False
        except:
            return False
        return True