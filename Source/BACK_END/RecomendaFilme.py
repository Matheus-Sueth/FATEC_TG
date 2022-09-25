import requests
import json
import unidecode
from os import walk
from Source.BACK_END.FilmeWEB import FilmeWEB
from Source.BACK_END.Colecao import Colecao

def procurar_filme_api(arquivo,ano=True):
    API_KEY = '9ccf9fd2aaa2811eabe3d8060d4b6e9f'
    filme = arquivo.split(' (')
    filme[1] = filme[1][:4]
    if ano:
        response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page=1&year={filme[1]}')
    else:
        response = requests.get(
            f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page=1')
    if response.ok:
        resposta = response.json()
        tamanho = resposta['total_pages']
        if tamanho <= 0:
            return False
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
                lista.append(FilmeWEB(id, titulo, data, generos(genero), sinopse, imgURL))
            return Colecao(lista,'Filmes WEB')
        else:
            lista = []
            pagina = 1
            while True:
                if response.ok:
                    resposta = response.json()
                    tam = len(resposta['results'])%20 if pagina == tamanho else 20
                    for indice in range(tam):
                        id = resposta.get('results')[indice].get('id')
                        data = resposta.get('results')[indice].get('release_date')
                        titulo = resposta.get('results')[indice].get('title')
                        genero = resposta.get('results')[indice].get('genre_ids')
                        sinopse = resposta.get('results')[indice].get('overview')
                        imgURL = 'http://image.tmdb.org/t/p/w500' + resposta.get('results')[indice].get('poster_path') if \
                            resposta.get('results')[indice].get('poster_path') != None else None
                        lista.append(FilmeWEB(id, titulo, data, generos(genero), sinopse, imgURL))
                else:
                    return False

                if pagina >= tamanho:
                    return Colecao(lista, 'Filmes WEB')
                elif pagina < tamanho:
                    pagina+=1

                if ano:
                    response = requests.get(
                        f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page={pagina}&year={filme[1]}')
                else:
                    response = requests.get(
                        f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=pt-BR&query={filme[0]}&page={pagina}')
    else:
        return False

def generos(ids):
    with open("BACK_END/generos.json", encoding='utf-8') as meu_json:
        genero = json.load(meu_json)
    juncao = ''
    for i in ids:
        juncao+=genero[str(i)]+'/'
    #print('GENERO = ',juncao[:-1])
    return juncao[:-1]