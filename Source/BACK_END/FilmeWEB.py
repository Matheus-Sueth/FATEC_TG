from os.path import isfile
import requests
import urllib.request
import io
from PIL import ImageTk
from PIL import Image
from pathlib import Path

class WebImage:
    def __init__(self, url, largura=600, altura=400):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        image.thumbnail((largura, altura))
        self.__image = ImageTk.PhotoImage(image)

    @property
    def image(self):
        return self.__image

class FilmeWEB:
    def __init__(self, id, titulo, ano, genero, sinopse, imgURL):
        self.__id = id
        self.__titulo = titulo
        self.tratar_titulo()
        self.__ano = int(ano[:4]) if ano != '' else ano
        self.__genero = genero if genero != None else genero
        if self.__genero != None:
            self.tratar_genero()
        self.__imgURL = imgURL
        self.__imgTk = self.__imgURL
        self.__sinopse = sinopse
        if self.__sinopse != None:
            self.tratar_sinopse()

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
        self.__titulo = self.__titulo.strip()
        if ':' in self.__titulo:
            self.__titulo = self.__titulo.replace(':',' -')
        return True

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
        self.__genero = self.__genero.strip()
        if self.__genero == '' or self.__genero == None:
            return False
        genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in self.__genero)
        if 'Ficção/Científica' in genero:
            genero = genero.replace('Ficção/Científica', 'Ficção Científica')
        if 'Cinema/TV' in genero:
            genero = genero.replace('Cinema/TV', 'Cinema TV')
        self.__genero = genero
        return True

    @property
    def imgURL(self):
        return self.__imgURL

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
    def imgTk(self):
        return self.__imgTk

    @imgTk.setter
    def imgTk(self, nova_imgTk):
        self.__imgTk = nova_imgTk

    def criar_imagem_tk(self, largura=550, altura=300):
        if self.__imgTk == None:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((largura, altura))
            self.__imgTk = ImageTk.PhotoImage(im)
            return False
        imagem = WebImage(self.__imgURL, largura, altura)
        self.__imgTk = imagem.image
        return True

    @property
    def sinopse(self):
        return self.__sinopse

    @sinopse.setter
    def sinopse(self, nova_sinopse):
        self.__sinopse = nova_sinopse

    def tratar_sinopse(self):
        self.__sinopse = self.__sinopse.capitalize()
        self.__sinopse = self.__sinopse.strip()
        self.__sinopse = self.__sinopse.replace("'", '"')
        if self.__sinopse == '' or self.__sinopse == None:
            return False
        return True