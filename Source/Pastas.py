class Pasta:
    def __init__(self, filme, imagem, banco):
        self.__caminho_filme = filme
        self.__caminho_imagem = imagem
        self.__caminho_banco = banco

    @property
    def caminho_filme(self):
        return self.__caminho_filme

    @caminho_filme.setter
    def caminho_filme(self, outro_filme):
        self.__caminho_filme = outro_filme

    @property
    def caminho_imagem(self):
        return self.__caminho_imagem

    @caminho_imagem.setter
    def caminho_imagem(self, outro_imagem):
        self.__caminho_imagem = outro_imagem

    @property
    def caminho_banco(self):
        return self.__caminho_banco

    @caminho_banco.setter
    def caminho_banco(self, outro_banco):
        self.__caminho_banco = outro_banco
