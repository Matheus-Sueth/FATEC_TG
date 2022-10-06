from Source.BACK_END.Usuario import Usuario
from Source.BACK_END.Banco import Banco
import base64

class UsuarioDAO(Banco):
    def __init__(self, banco):
        super().__init__(banco)
        selfbanco_conectado = self.banco

    def validar_dados_usuario(self,novo_usuario):
        if not novo_usuario.eh_nome_valido():
            raise Exception('O nome não condiz com a diretrizes do sistema')

        if not novo_usuario.eh_email_valido():
            raise Exception('O email não condiz com a diretrizes do sistema')

        if not novo_usuario.eh_senha_valida():
            raise Exception('A senha não condiz com a diretrizes do sistema')

        if not novo_usuario.eh_foto_valida():
            raise Exception('A foto não condiz com a diretrizes do sistema')
        return True

    def inserir_dados(self, novo_usuario: Usuario):
        try:
            auxiliar = self.validar_dados_usuario(novo_usuario)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM usuario WHERE email == "{novo_usuario.email}"')
        usuario_login = self.cursor.fetchall()
        if len(usuario_login) > 0:
            raise Exception(f'Usuário com o email: {novo_usuario.email} foi encontrado no sistema, a criação de usuário foi cancelada')
        encoded = (base64.b64encode(novo_usuario.senha.encode('ascii')))
        novo_usuario.senha = encoded.decode('ascii')
        self.cursor.execute(f'INSERT INTO usuario (nome,email,senha,foto) VALUES("{novo_usuario.nome}","{novo_usuario.email}","{novo_usuario.senha}","{novo_usuario.foto}")')
        return self.salvar_dados()

    def ler_dados_usuario(self, usuario: Usuario):
        try:
            auxiliar = self.validar_dados_usuario(usuario)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario.email}"')
        usuario_login = self.cursor.fetchall()
        if len(usuario_login) == 0:
            raise Exception('Nenhum usuário foi encontrado no sistema')
        usuario_login = [dado for dado in usuario_login[0]]
        decoded = base64.b64decode(usuario_login[3].encode('ascii'))
        usuario_login[3] = decoded.decode('ascii')
        usuario_encontrado = Usuario(usuario_login[0],usuario_login[1],usuario_login[2],usuario_login[3],usuario_login[4])
        if not (usuario_encontrado == usuario):
            raise Exception(f'Usuário ({usuario_encontrado.nome}) foi encontrado no sistema, porém a senha está incorreta')
        else:
            return Usuario(usuario_login[0],usuario_login[1],usuario_login[2],usuario_login[3],usuario_login[4])

    def alterar_dados(self, usuario_antigo: Usuario, usuario_alterado: Usuario):
        try:
            auxiliar = self.validar_dados_usuario(usuario_alterado)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario_antigo.email}"')
        usuario_login = self.cursor.fetchall()
        if len(usuario_login) == 0:
            raise Exception('Nenhum usuário foi encontrado no sistema')
        self.cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario_alterado.email}"')
        usuario_login = self.cursor.fetchall()
        if len(usuario_login) > 0:
            raise Exception('E-mail já está cadastrado no sistema')
        encoded = (base64.b64encode(usuario_alterado.senha.encode('ascii')))
        usuario_alterado.senha = encoded.decode('ascii')
        self.cursor.execute(
            f"UPDATE usuario SET nome = '{usuario_alterado.nome}', email = '{usuario_alterado.email}', senha = '{usuario_alterado.senha}', foto = '{usuario_alterado.foto}' WHERE id = {usuario_antigo.id}")
        return self.salvar_dados()

    def deletar_dados(self, usuario: Usuario):
        try:
            auxiliar = self.validar_dados_usuario(usuario)
        except Exception as erro:
            raise Exception(erro)
        self.cursor.execute(f'SELECT * FROM usuario WHERE email == "{usuario.email}"')
        usuario_login = self.cursor.fetchall()
        if len(usuario_login) == 0:
            raise Exception('Nenhum usuário foi encontrado no sistema')
        self.cursor.execute(
            f'DELETE FROM usuario WHERE email == "{usuario.email}"')
        return self.salvar_dados()
