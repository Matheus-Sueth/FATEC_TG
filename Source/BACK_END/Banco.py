import sqlite3 as sql
from pathlib import Path

class Banco:
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

    def salvar_dados(self):
        self.__banco_conectado.commit()
        return True

    def validar_estrutura_banco(self):
        colunas = {'usuario':('id','nome','email','senha','foto'),
                   'pastas':('id', 'usuario_id', 'filme', 'imagem', 'banco'),
                   'filmes':('id', 'usuario_id', 'titulo', 'ano', 'nota', 'genero', 'extensao', 'cam_filme', 'cam_imagem', 'qtd_assistido', 'sinopse')
        }
        for chave, valor in colunas.items():
            auxiliar = self.__cursor.execute(f'SELECT * FROM {chave}')
            bd_colunas = [coluna[0] for coluna in auxiliar.description]
            if tuple(bd_colunas) != valor:
                raise Exception(f'A estrura da tabela({chave}) não está com de acordo com as diretrizes do sistema')
        return True