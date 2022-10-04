from Source.BACK_END.Pastas import Pasta
from Source.BACK_END.UsuarioDAO import Usuario
from Source.BACK_END.Banco import Banco

class PastaDAO(Banco):
    def __init__(self, banco):
        super().__init__(banco)

    def validar_pastas(self, pasta:Pasta):
        if not pasta.validar_caminho_imagem():
            raise Exception(f'Diretório de imagens({pasta.caminho_imagem}) não foi encontrado')

        if not pasta.validar_caminho_filme():
            raise Exception(f'Diretório de filmes({pasta.caminho_filme}) não foi encontrado')
        return True

    def verificar_pasta_imagem(self, pasta:Pasta):
        self.cursor.execute(f'SELECT * FROM pastas WHERE imagem == "{pasta.caminho_imagem}"')
        result = self.cursor.fetchall()
        if len(result) != 0:
            raise Exception('Essa pasta de imagem já existe no banco de dados')
        return True

    def inserir_pastas(self, pasta:Pasta, usuario:Usuario):
        try:
            auxiliar = self.validar_pastas(pasta)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM pastas WHERE usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) > 0:
            raise Exception(f'O usuário {usuario.nome} já possui pastas cadastradas')
        try:
            auxiliar = self.verificar_pasta_imagem(pasta)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(
            f'INSERT INTO pastas (usuario_id,filme,imagem,banco) VALUES({usuario.id},"{pasta.caminho_filme}","{pasta.caminho_imagem}","{pasta.caminho_banco}")')
        return self.salvar_dados()

    def ler_pastas_usuario(self, usuario:Usuario):
        self.cursor.execute(f'SELECT * FROM pastas WHERE usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) == 0:
            raise Exception(f'Nenhuma pasta foi encontrada para o usuário {usuario.nome}')
        dados = result[0]
        return Pasta(dados[0],dados[1],dados[2],dados[3],dados[4])

    def alterar_pastas(self, pasta_antiga:Pasta, pasta_alterada:Pasta, usuario:Usuario):
        try:
            auxiliar = self.validar_pastas(pasta_alterada)
        except Exception as erro:
            raise Exception(erro)
        try:
            auxiliar = self.verificar_pasta_imagem(pasta_alterada)
        except Exception as erro:
            raise Exception(erro)
        try:
            auxiliar = self.ler_pastas_usuario(usuario)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(
            f"UPDATE pastas SET filme = '{pasta_alterada.caminho_filme}', imagem = '{pasta_alterada.caminho_imagem}', banco = '{pasta_alterada.caminho_banco}' WHERE usuario_id == {usuario.id}")
        return self.salvar_dados()

    def deletar_pastas(self, pasta:Pasta, usuario:Usuario):
        try:
            auxiliar = self.ler_pastas_usuario(usuario)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'DELETE FROM pastas WHERE usuario_id == {usuario.id}')
        return self.salvar_dados()