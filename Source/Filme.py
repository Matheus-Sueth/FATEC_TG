class Filme:
    def __init__(self, id, titulo: str, ano: int, nota: str, genero: str,
                 extensao: str, cam_filme: str, cam_imagem: str, sinopse: str, valor:int=0):
        self.__id = id #vai ser o id na API TMDB, se não encontrar vai ser -1.len(banco_filmes)
        self.__titulo = titulo.title()
        self.__ano = ano
        self.__nota = nota
        self.__genero = genero.title()
        self.__extensao = extensao
        self.__cam_filme = cam_filme
        self.__cam_imagem = cam_imagem
        self.__qtd_assistido = valor
        self.__sinopse = sinopse

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        self.__titulo = novo_titulo.title()

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, novo_ano):
        self.__ano = novo_ano

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, nova_nota):
        self.__nota = nova_nota

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, novo_genero):
        self.__genero = novo_genero.title()

    @property
    def extensao(self):
        return self.__extensao

    @extensao.setter
    def extensao(self, nova_extensao):
        self.__extensao = nova_extensao

    @property
    def cam_filme(self):
        return self.__cam_filme

    @cam_filme.setter
    def cam_filme(self, novo_cam_filme):
        self.__cam_filme = novo_cam_filme

    @property
    def cam_imagem(self):
        return self.__cam_imagem

    @cam_imagem.setter
    def cam_imagem(self, novo_cam_imagem):
        self.__cam_imagem = novo_cam_imagem

    @property
    def assistido(self):
        return self.__qtd_assistido

    def aumentar_assistido(self):
        self.__qtd_assistido = self.__qtd_assistido + 1

    @property
    def sinopse(self):
        return self.__sinopse

    @sinopse.setter
    def sinopse(self, nova_sinopse):
        self.__sinopse = nova_sinopse