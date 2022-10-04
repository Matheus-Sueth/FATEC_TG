from os.path import isfile
from pathlib import Path

class Pasta:
    def __init__(self, id, usuario_id, filme, imagem, banco):
        self.__id = id
        self.__usuario_id = usuario_id
        self.__caminho_filme = rf'{filme}'
        self.__caminho_imagem = rf'{imagem}'
        self.__caminho_banco =  rf'{banco}'

    def __str__(self):
        return f'Diretório dos filmes = {self.__caminho_filme}\nDiretório das imagens = {self.__caminho_imagem}\nDiretório do banco = {self.__caminho_banco}'

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, outro_id):
        self.__id = outro_id

    @property
    def usuario_id(self):
        return self.__usuario_id

    @usuario_id.setter
    def usuario_id(self, outro_usuario_id):
        self.__usuario_id = outro_usuario_id

    @property
    def caminho_filme(self):
        return self.__caminho_filme

    @caminho_filme.setter
    def caminho_filme(self, outro_filme):
        self.__caminho_filme = outro_filme

    def validar_caminho_filme(self):
        return Path(self.__caminho_filme).is_dir() and len(self.__caminho_filme) != 0

    @property
    def caminho_imagem(self):
        return self.__caminho_imagem

    @caminho_imagem.setter
    def caminho_imagem(self, outro_imagem):
        self.__caminho_imagem = outro_imagem

    def validar_caminho_imagem(self):
        return Path(self.__caminho_imagem).is_dir() and len(self.__caminho_imagem) != 0

    @property
    def caminho_banco(self):
        return self.__caminho_banco

    @caminho_banco.setter
    def caminho_banco(self, outro_banco):
        self.__caminho_banco = outro_banco
