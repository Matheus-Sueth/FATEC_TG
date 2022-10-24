import json
import datetime
from os.path import isfile

class Filme:
    def __init__(self, id: str, titulo: str, ano: int, nota: str, genero: str, extensao: str, cam_filme: str, cam_imagem: str, sinopse: str, valor:int=0):
        self.__id = id #vai ser o id na API TMDB, se não encontrar vai ser -1.len(banco_filmes)
        self.__titulo = titulo
        self.__ano = ano
        self.__nota = nota
        self.__genero = genero
        self.__extensao = extensao
        self.__cam_filme = rf'{cam_filme}'
        self.__cam_imagem = rf'{cam_imagem}'
        self.__qtd_assistido = valor
        self.__sinopse = sinopse.capitalize()

    def __str__(self):
        return f'Titulo = {self.__titulo} - Ano = {self.__ano}'

    def __eq__(self, other):
        return (self.__titulo == other.titulo) and (self.__ano == other.ano)

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        self.__titulo = novo_titulo

    def tratar_titulo(self):
        if self.__titulo.strip() == '':
            return False
        return True

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, novo_ano):
        self.__ano = novo_ano

    def tratar_ano(self):
        return self.__ano >= 1900 and self.__ano <= int(datetime.datetime.now().year)

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, nova_nota):
        self.__nota = nova_nota

    def tratar_nota(self):
        notas_list = ['NÃO ASSISTIDO', 'PÉSSIMO', 'MUITO RUIM', 'MAIS OU MENOS', 'MUITO BOM','EXCELENTE']
        return  self.__nota.strip() in notas_list

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, novo_genero):
        self.__genero = novo_genero

    def tratar_genero(self):
        genero_list = ['Animação', 'Aventura', 'Ação', 'Cinema TV', 'Comédia', 'Crime', 'Documentário', 'Drama',
                       'Família', 'Fantasia', 'Faroeste', 'Ficção Científica', 'Guerra', 'História', 'Mistério',
                       'Música', 'Romance', 'Terror', 'Thriller']
        auxiliar = self.__genero.split('/')
        for nota in auxiliar:
            if nota not in genero_list:
                return False
        else:
            return True

    @property
    def extensao(self):
        return self.__extensao

    @extensao.setter
    def extensao(self, nova_extensao):
        self.__extensao = nova_extensao

    def tratar_extensao(self):
        return self.__extensao.strip() != '' and '.' in self.__extensao and len(self.__extensao.strip()) > 2

    @property
    def cam_filme(self):
        return self.__cam_filme

    @cam_filme.setter
    def cam_filme(self, novo_cam_filme):
        self.__cam_filme = novo_cam_filme

    def tratar_cam_filme(self):
        return isfile(self.__cam_filme)

    @property
    def cam_imagem(self):
        return self.__cam_imagem

    @cam_imagem.setter
    def cam_imagem(self, novo_cam_imagem):
        self.__cam_imagem = novo_cam_imagem

    def tratar_cam_imagem(self):
        return isfile(self.__cam_imagem)

    @property
    def assistido(self):
        return self.__qtd_assistido

    def aumentar_assistido(self):
        self.__qtd_assistido = self.__qtd_assistido + 1
        return True

    @property
    def sinopse(self):
        return self.__sinopse

    @sinopse.setter
    def sinopse(self, nova_sinopse):
        self.__sinopse = nova_sinopse

    def tratar_sinopse(self):
        if self.__sinopse.strip() == '':
            return False
        self.__sinopse = self.__sinopse.replace("'", '"')
        return True