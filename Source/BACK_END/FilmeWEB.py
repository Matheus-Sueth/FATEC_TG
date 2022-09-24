from os.path import isfile
import requests

class FilmeWEB:
    def __init__(self, id, titulo, ano, genero, sinopse, imgURL):
        self.__id = id
        self.__titulo = titulo
        if self.__titulo != None:
            self.tratar_titulo()
        self.__ano = int(ano[:4]) if ano != None else ano
        self.__genero = genero
        if self.__genero != None:
            self.tratar_genero()
        self.__imgURL = imgURL
        self.__sinopse = sinopse
        if self.__sinopse != None:
            self.tratar_sinopse()

    def __str__(self):
        return f'Titulo = {self.__titulo} - Ano = {self.__ano}'

    def __eq__(self, other):
        return (self.__titulo == other.titulo) and (self.__ano == other.ano)

    def verificar_null(self):
        return self.__genero == None or self.__imgURL == None or self.__sinopse == None

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        self.__titulo = novo_titulo.title()

    def tratar_titulo(self):
        self.__titulo.strip()
        self.__titulo.title()
        if ':' in self.__titulo:
            self.__titulo.replace(':',' -')

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, novo_ano):
        self.__ano = novo_ano

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, novo_genero):
        self.__genero = novo_genero

    def tratar_genero(self):
        genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in self.__genero)
        if 'Ficção/Científica' in genero:
            genero = genero.replace('Ficção/Científica', 'Ficção Científica')
        if 'Cinema/TV' in genero:
            genero = genero.replace('Cinema/TV', 'Cinema TV')
        self.__genero = genero

    @property
    def imgURL(self):
        return self.__sinopse

    @imgURL.setter
    def imgURL(self, nova_imgURL):
        self.__imgURL = nova_imgURL

    def download_imagem(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'wb') as imagem:
                respost = requests.get(self.__imgURL, stream=True)

                if not respost.ok:
                   return False
                else:
                    for dado in respost.iter_content(1024):
                        if not dado:
                            break

                        imagem.write(dado)
                    return True
        except:
            return False

    @property
    def sinopse(self):
        return self.__sinopse

    @sinopse.setter
    def sinopse(self, nova_sinopse):
        self.__sinopse = nova_sinopse

    def tratar_sinopse(self):
        self.__sinopse.capitalize()
        self.__sinopse.strip()
        self.__sinopse.replace("'", '"')