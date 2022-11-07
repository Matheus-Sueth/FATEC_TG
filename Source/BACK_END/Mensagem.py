class Mensagem:
    def __init__(self, id, nome, mensagem, hora):
        self.id:int = id
        self.nome:str = nome
        self.mensagem:str = mensagem
        self.hora:str = hora

    def __str__(self):
        return f'{self.nome} - {self.hora}\n{self.mensagem}\n\n'

