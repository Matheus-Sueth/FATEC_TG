from Source.BACK_END.Filme import Filme
from Source.BACK_END.Colecao import Colecao
from Source.BACK_END.Banco import Banco
from Source.BACK_END.Usuario import Usuario

class FilmeDAO(Banco):
    def __init__(self, banco):
        super().__init__(banco)

    def validar_filme(self, filme: Filme):
        if not filme.tratar_titulo():
            raise Exception('O titulo do filme deve ser preenchido')
        if not filme.tratar_ano():
            raise Exception('O ano do filme deve ser maior que 1900 e menor ou igual que o ano atual')
        if not filme.tratar_genero():
            raise Exception('O genêro do filme deve estar dentro da lista dos genêros do sistema')
        if not filme.tratar_nota():
            raise Exception('A nota do filme deve estar dentro da lista de notas do sistema')
        if not filme.tratar_extensao():
            raise Exception('O formato da extensao do filme deve ser(.extensao)')
        if not filme.tratar_sinopse():
            raise Exception('A sinopse do filme deve ser preenchida')
        if not filme.tratar_cam_imagem():
            raise Exception('O caminho da imagem deve existir')
        if not filme.tratar_cam_filme():
            raise Exception('O caminho do filme deve existir')
        return True

    def inserir_filme(self, filme:Filme, usuario: Usuario):
        try:
            auxiliar = self.validar_filme(filme)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM filmes WHERE id == "{filme.id}" and usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) > 0:
            raise Exception(f'O filme {filme.titulo} - ano {filme.ano} está cadastrado')
        self.cursor.execute(f"INSERT INTO filmes VALUES('{filme.id}',{usuario.id},'{filme.titulo}',{filme.ano},'{filme.nota}','{filme.genero}','{filme.extensao}','{filme.cam_filme}','{filme.cam_imagem}',{filme.assistido},'{filme.sinopse}')")
        return self.salvar_dados()

    def ver_filmes(self, usuario: Usuario):
        lista = []
        self.cursor.execute(f'SELECT * FROM filmes WHERE usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) >= 1:
            for dados in result:
                filme = Filme(
                    id=dados[0],
                    titulo=dados[2],
                    ano=dados[3],
                    nota=dados[4],
                    genero=dados[5],
                    extensao=dados[6],
                    cam_filme=dados[7],
                    cam_imagem=dados[8],
                    valor=dados[9],
                    sinopse=dados[10])
                lista.append(filme)
        return Colecao(lista, 'Filmes')

    def ver_filmes_ordenados(self, usuario: Usuario):
        lista = []
        self.cursor.execute(f'SELECT * FROM filmes WHERE usuario_id == {usuario.id} ORDER BY titulo, ano')
        result = self.cursor.fetchall()
        if len(result) >= 1:
            for dados in result:
                filme = Filme(
                    id=dados[0],
                    titulo=dados[2],
                    ano=dados[3],
                    nota=dados[4],
                    genero=dados[5],
                    extensao=dados[6],
                    cam_filme=dados[7],
                    cam_imagem=dados[8],
                    valor=dados[9],
                    sinopse=dados[10])
                lista.append(filme)
        return Colecao(lista,'Filmes ordenados por titulo e ano')

    def alterar_filme(self, filme: Filme, usuario: Usuario):
        try:
            auxiliar = self.validar_filme(filme)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM filmes WHERE id == "{filme.id}" and usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) == 0:
            raise Exception(f'O filme {filme.titulo} - ano {filme.ano} não está cadastrado')
        self.cursor.execute(f"UPDATE filmes SET titulo = '{filme.titulo}', ano = {filme.ano}, nota = '{filme.nota}', genero = '{filme.genero}', extensao = '{filme.extensao}', cam_filme = '{filme.cam_filme}', cam_imagem = '{filme.cam_imagem}', sinopse = '{filme.sinopse}' WHERE id = '{filme.id}' and usuario_id = {usuario.id}")
        return self.salvar_dados()

    def deletar_filme(self, filme: Filme, usuario: Usuario):
        self.cursor.execute(f'SELECT * FROM filmes WHERE id == "{filme.id}" and usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) == 0:
            raise Exception(f'O filme {filme.titulo} - ano {filme.ano} não está cadastrado')
        self.cursor.execute(f'DELETE FROM filmes WHERE id = "{filme.id}" and usuario_id = {usuario.id}')
        return self.salvar_dados()

    def procurar_filmes(self, coluna: str, texto: str, usuario: Usuario):
        lista = []
        texto_procurado = ''
        if coluna == 'titulo' or coluna == 'sinopse':
            aux = [auxiliar for auxiliar in texto]
            texto = '%'.join(aux)

        if coluna != 'ano':
            texto_procurado = f' LIKE "%{texto}%"'
        else:
            texto_procurado = f' == {texto}'
        self.cursor.execute(f'SELECT * FROM filmes WHERE {coluna}{texto_procurado} and usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        for dados in result:
            filme = Filme(
                id=dados[0],
                titulo=dados[2],
                ano=dados[3],
                nota=dados[4],
                genero=dados[5],
                extensao=dados[6],
                cam_filme=dados[7],
                cam_imagem=dados[8],
                valor=dados[9],
                sinopse=dados[10])
            lista.append(filme)
        return Colecao(lista, f'Filmes ordenados pela coluna: {coluna}')

    def somar_atributo_filme(self, filme: Filme, usuario: Usuario):
        self.cursor.execute(f'SELECT * FROM filmes WHERE id == "{filme.id}" and usuario_id == {usuario.id}')
        result = self.cursor.fetchall()
        if len(result) == 0:
            raise Exception(f'O filme {filme.titulo} - ano {filme.ano} não está cadastrado')
        filme.aumentar_assistido()
        self.cursor.execute(f'UPDATE filmes SET qtd_assistido = {filme.assistido} WHERE id = "{filme.id}" and usuario_id = {usuario.id}')
        return self.salvar_dados()

    def achar_filme_recomendado(self, usuario:Usuario):
        lista = []
        self.cursor.execute(f'SELECT id FROM filmes WHERE usuario_id == {usuario.id} AND qtd_assistido <> 0 AND nota IN ("EXCELENTE","MUITO BOM") GROUP BY id ORDER BY qtd_assistido DESC, nota')
        result = self.cursor.fetchall()
        if len(result) >= 1:
            for dados in result:
                lista.append(dados[0])
        return Colecao(lista, 'Ids de filmes para recomendação')