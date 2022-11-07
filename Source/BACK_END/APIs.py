import requests
import json
import unidecode
from os import walk
from Source.BACK_END.FilmeWEB import FilmeWEB
from Source.BACK_END.Colecao import Colecao
from Source.BACK_END.Usuario import Usuario
from Source.BACK_END.Mensagem import Mensagem
from threading import Thread
import re

credentials = {
    "SM": "c2VsZWN0bW92aWVhcGk6czFlMmwzZTRjNXQ2bTdvOHY5aTBl",
    "TMDB": "9ccf9fd2aaa2811eabe3d8060d4b6e9f"
}

class TMDB_Consulta(Thread):
    def __init__(self, arquivo, pesquisa_completa=True):
        super().__init__()
        aux_filme = re.split(r"[/()]\s*", arquivo)
        self.titulo = aux_filme[-3]
        self.ano = aux_filme[-2]
        self.pesquisa_completa = pesquisa_completa

    def run(self):
        if self.pesquisa_completa:
            response = requests.get(
                f'https://api.themoviedb.org/3/search/movie?api_key={credentials["TMDB"]}&language=pt-BR&query={self.titulo}&page=1&year={self.ano}')
        else:
            response = requests.get(
                f'https://api.themoviedb.org/3/search/movie?api_key={credentials["TMDB"]}&language=pt-BR&query={self.titulo}&page=1')
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
                            f'https://api.themoviedb.org/3/search/movie?api_key={credentials["TMDB"]}&language=pt-BR&query={self.titulo}&page={pagina}&year={self.ano}')
                    else:
                        response = requests.get(
                            f'https://api.themoviedb.org/3/search/movie?api_key={credentials["TMDB"]}&language=pt-BR&query={self.titulo}&page={pagina}')
        else:
            self.filmes_api = False
            return None

    def generos(self, ids):
        with open("BACK_END/generos.json", encoding='utf-8') as meu_json:
            genero = json.load(meu_json)
        lista = [genero[str(i)] for i in ids]
        return '/'.join(lista)

class TMDB_Recomenda(Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        response = requests.get(f'https://api.themoviedb.org/3/movie/{self.id}/recommendations?api_key={credentials["TMDB"]}&language=pt-BR&page=1')
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
                self.filmes_api = Colecao(lista, 'Filmes Recomendados')
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
                            self.filmes_api = Colecao(lista, 'Filmes Recomendados')
                            return None

                    if pagina >= tamanho:
                        self.filmes_api = Colecao(lista, 'Filmes Recomendados')
                        return None
                    elif pagina < tamanho:
                        pagina += 1

                    response = requests.get(f'https://api.themoviedb.org/3/movie/{self.id}/recommendations?api_key={credentials["TMDB"]}&language=pt-BR&page={pagina}')
        else:
            self.filmes_api = False
            return None

    def generos(self, ids):
        with open("BACK_END/generos.json", encoding='utf-8') as meu_json:
            genero = json.load(meu_json)
        lista = [genero[str(i)] for i in ids]
        return '/'.join(lista)

class API_SM(Thread):
    def __init__(self, user: Usuario, funcao, segundo_plano=True, mensagem='', hora=''):
        funcoes = {
            'verificar_usuario': self.verificar_usuario,
            'enviar_mensagem': self.enviar_mensagem,
            'receber_mensagens': self.receber_mensagens
        }
        super().__init__(target=funcoes[funcao], daemon=segundo_plano)
        self.user = user
        self.url = 'https://selectmovietg.herokuapp.com'
        self.mensagem = mensagem
        self.hora = hora

    def verificar_usuario(self):
        try:
            url = f'{self.url}/user/read/name/email/'
            request_headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Basic {credentials["SM"]}'
            }
            request_body = {
              "nome": self.user.nome,
              "email": self.user.email
            }
            response = requests.post(url, headers=request_headers, data=json.dumps(request_body))
            if response.ok:
                id = response.json().get('id',None)
                self.id = id
            else:
                self.criar_usuario()
        except:
            self.id = False

    def criar_usuario(self):
        try:
            url = f'{self.url}/user/create/'
            request_headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Basic {credentials["SM"]}'
            }
            request_body = {
              "nome": self.user.nome,
              "email": self.user.email
            }
            response = requests.post(url, headers=request_headers, data=json.dumps(request_body))
            if response.ok:
                id = response.json().get('id',None)
                self.id = id
            else:
                self.id = None
        except:
            self.id = False

    def enviar_mensagem(self):
        try:
            url = f'{self.url}/user/create/message/'
            request_headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Basic {credentials["SM"]}'
            }
            request_body = {
              "user": {
              "nome": self.user.nome,
              "email": self.user.email
            },
              "message": {
                "message": self.mensagem,
                "hora": self.hora
              }
            }
            response = requests.post(url, headers=request_headers, data=json.dumps(request_body))
            if response.ok:
                id = response.json().get('id',None)
                self.id_mensagem = id
            else:
                self.id_mensagem = None
        except:
            self.id_mensagem = False

    def receber_mensagens(self):
        try:
            url = f'{self.url}/read/messages/?hora={self.hora}'
            request_headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Basic {credentials["SM"]}'
            }
            response = requests.get(url, headers=request_headers)
            if response.ok:
                lista = []
                mensagens = response.json()
                if len(mensagens) == 0:
                    self.mensagens = Colecao(lista, f'Mensagens do horário = {self.hora}')
                else:
                    lista = []
                    for dados in mensagens:
                        url = f'{self.url}/user/read/?user_id={dados["owner_id"]}'
                        response = requests.get(url, headers=request_headers)
                        if not response.ok:
                            continue
                        else:
                            nome = response.json()['nome']
                        m = Mensagem(id=dados['id'], nome=nome, mensagem=dados['message'], hora=dados['hora'])
                        lista.append(m)
                    self.mensagens = Colecao(lista,f'Mensagens do horário = {self.hora}')
            else:
                self.mensagens = None
        except:
            self.mensagens = False

if __name__ == '__main__':
    user = Usuario(1,'matheus','matheus@gmail.com','12345678','E:/perfil.png')

    api = SM(user=user, funcao='receber_mensagens', hora='16:50')
    api.start()
    api.join()
    for i in api.mensagens:
        print(i)
