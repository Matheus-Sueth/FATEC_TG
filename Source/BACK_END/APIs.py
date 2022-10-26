import requests
import json
import unidecode
from os import walk
from Source.BACK_END.FilmeWEB import FilmeWEB
from Source.BACK_END.Colecao import Colecao
from threading import Thread
import re


class TMDB_Consulta(Thread):
    API_KEY = '9ccf9fd2aaa2811eabe3d8060d4b6e9f'
    def __init__(self, arquivo, pesquisa_completa=True):
        super().__init__()
        aux_filme = re.split(r"[/()]\s*", arquivo)
        self.titulo = aux_filme[-3]
        self.ano = aux_filme[-2]
        self.pesquisa_completa = pesquisa_completa

    def run(self):
        if self.pesquisa_completa:
            response = requests.get(
                f'https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}&language=pt-BR&query={self.titulo}&page=1&year={self.ano}')
        else:
            response = requests.get(
                f'https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}&language=pt-BR&query={self.titulo}&page=1')
        if response.ok:
            resposta = response.json()
            tamanho = resposta['total_pages']
            if tamanho <= 0:
                self.filmes_api = False
                return None
            elif tamanho == 1:
                lista = []
                fim = resposta['total_results']
                for indice in range(fim):
                    id = resposta.get('results')[indice].get('id')
                    data = resposta.get('results')[indice].get('release_date')
                    titulo = resposta.get('results')[indice].get('title')
                    genero = resposta.get('results')[indice].get('genre_ids')
                    sinopse = resposta.get('results')[indice].get('overview')
                    imgURL = 'http://image.tmdb.org/t/p/w500' + resposta.get('results')[indice].get('poster_path') if \
                        resposta.get('results')[indice].get('poster_path') != None else None
                    if titulo != None and data != None:
                        lista.append(FilmeWEB(id, titulo, data, self.generos(genero), sinopse, imgURL))
                self.filmes_api = Colecao(lista, 'Filmes WEB')
                return None
            else:
                lista = []
                pagina = 1
                while True:
                    if response.ok:
                        resposta = response.json()
                        tam = len(resposta['results']) % 20 if pagina == tamanho else 20
                        for indice in range(tam):
                            id = resposta.get('results')[indice].get('id')
                            data = resposta.get('results')[indice].get('release_date')
                            titulo = resposta.get('results')[indice].get('title')
                            genero = resposta.get('results')[indice].get('genre_ids')
                            sinopse = resposta.get('results')[indice].get('overview')
                            imgURL = 'http://image.tmdb.org/t/p/w500' + resposta.get('results')[indice].get(
                                'poster_path') if \
                                resposta.get('results')[indice].get('poster_path') != None else None
                            if titulo != None and data != None:
                                lista.append(FilmeWEB(id, titulo, data, self.generos(genero), sinopse, imgURL))
                    else:
                        if len(lista) == 0:
                            self.filmes_api = False
                            return None
                        else:
                            self.filmes_api = Colecao(lista, 'Filmes WEB')
                            return None

                    if pagina >= tamanho:
                        self.filmes_api = Colecao(lista, 'Filmes WEB')
                        return None
                    elif pagina < tamanho:
                        pagina += 1

                    if self.pesquisa_completa:
                        response = requests.get(
                            f'https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}&language=pt-BR&query={self.titulo}&page={pagina}&year={self.ano}')
                    else:
                        response = requests.get(
                            f'https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}&language=pt-BR&query={self.titulo}&page={pagina}')
        else:
            self.filmes_api = False
            return None

    def generos(self, ids):
        with open("BACK_END/generos.json", encoding='utf-8') as meu_json:
            genero = json.load(meu_json)
        lista = [genero[str(i)] for i in ids]
        return '/'.join(lista)
