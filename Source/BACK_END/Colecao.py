class Colecao:
    def __init__(self, arquivos, tipo):
        self.__arquivos = arquivos
        self.tipo = tipo

    def __str__(self):
        return f'Coleção de {self.tipo}'

    def __len__(self):
        return len(self.__arquivos)

    def __getitem__(self, item):
        return self.__arquivos[item]

    @property
    def arquivos(self):
        return self.__arquivos

    @arquivos.setter
    def arquivos(self, outros_colecao_arquivos):
        self.__arquivos = outros_colecao_arquivos
