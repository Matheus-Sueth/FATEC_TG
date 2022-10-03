from Source.test.db_demo import banco_usuarios
from Source.BACK_END.Usuario import Usuario
from pytest import raises, mark, fixture

@fixture
def usuario_valido_fora_bd():
   '''Retorna um usuário válido que não está no banco de dados para ser usado no create_user_success'''
   return Usuario(0, 'Marcelo', 'marcelo@yahoo.com', '1234', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_fora_bd2():
   '''Retorna um usuário válido que não está no banco de dados para ser usado no login_user_failure'''
   return Usuario(0, 'Fanta Laranja', 'fanta.laranja@yahoo.com', 'laranjamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_fora_bd3():
   '''Retorna um usuário válido que está no banco de dados para ser usado no update_user_failure_user_changed'''
   return Usuario(0, 'Fanta Uva', 'fanta.uva@yahoo.com', 'uvamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd():
   '''Retorna um usuário válido que está no banco de dados para sr usado no create_user_failure_user_existing'''
   return Usuario(1, 'José', 'Jose@gmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd2():
   '''Retorna um usuário válido que está no banco de dados para ser usado no update_user_failure_user_changed'''
   return Usuario(6, 'Catarina', 'catarina@gmail.com', '1234', 'E:/0b8c081b7b05dcc0aad6238856ea87d2.gif')


@mark.user
class TestClassUsuario:
   @mark.data_validation
   class TestClassUsuarioValidation:
      @mark.data_validation_success
      @mark.parametrize("usuario", [
         (Usuario(1, 'José', 'Jose@gmail.com', '1234', r'E:/2020-02-20.jpg')),
         (Usuario(2, 'Maria', 'maria@hotmail.com', '1234', r'E:/2020-02-20.jpg')),
         (Usuario(3, 'Carlos', 'carlos@yahoo.com', '1234', 'E:/2020-02-20.jpg')),
         (Usuario(4, 'Alex', 'alex@yahoo.com', '1234', 'E:/2020-02-20.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_true(self, usuario):
         assert banco_usuarios.validar_dados_usuario(usuario)

      @mark.data_validation_failure_nome
      @mark.parametrize("usuario", [
         (Usuario(0, '', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20.jpg')),
         (Usuario(0, 'mi', 'miguelcunha@gmail.com', 'cunha@1234', r'E:/imagens/perfil.jpg')),
         (Usuario(0, 'emilly92', 'emilly92@yahoo.com.br', 'emilly92@1234', r'E:/2020-02-20.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_nome(self, usuario):
         with raises(Exception) as erro:
            banco_usuarios.validar_dados_usuario(usuario)
         assert 'O nome não condiz com a diretrizes do sistema' in str(erro.value)

      @mark.data_validation_failure_foto
      @mark.parametrize("usuario", [
         (Usuario(0, 'UsuarioTeste', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20')),
         (Usuario(0, 'miguel cunha', 'miguelcunha@gmail.com', 'cunha@1234', r'')),
         (Usuario(0, 'emilly', 'emilly92@yahoo.com.br', 'emilly92@1234', r'E:/imagens/')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_foto(self, usuario):
         with raises(Exception) as erro:
            banco_usuarios.validar_dados_usuario(usuario)
         assert 'A foto não condiz com a diretrizes do sistema' in str(erro.value)

      @mark.data_validation_failure_email
      @mark.parametrize("usuario", [
         (Usuario(0, 'UsuarioTeste', 'usuario.testegmail.com', 'usuario@1234', r'E:/2020-02-20.jpg')),
         (Usuario(0, 'miguel cunha', 'miguelcunha@com', 'cunha@1234', r'E:/imagens/perfil.jpg')),
         (Usuario(0, 'emilly', '', 'emilly92@1234', r'E:/imagens/perfil.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_email(self, usuario):
         with raises(Exception) as erro:
            banco_usuarios.validar_dados_usuario(usuario)
         assert 'O email não condiz com a diretrizes do sistema' in str(erro.value)

      @mark.data_validation_failure_senha
      @mark.parametrize("usuario", [
         (Usuario(0, 'UsuarioTeste', 'usuario.teste@gmail.com', '', r'E:/2020-02-20.jpg')),
         (Usuario(0, 'miguel cunha', 'miguelcunha@hotmail.com', 'c', r'E:/imagens/perfil.jpg')),
         (Usuario(0, 'emilly', 'emilly92@yahoo.com', '123', r'E:/imagens/perfil.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_senha(self, usuario):
         with raises(Exception) as erro:
            banco_usuarios.validar_dados_usuario(usuario)
         assert 'A senha não condiz com a diretrizes do sistema' in str(erro.value)

   @mark.create_user
   class TestClassUsuarioCreate:
      @mark.create_user_success
      def test_quando_programa_cria_usuario_recebe_dados_usuario_deve_retornar_true(self, usuario_valido_fora_bd):
         assert banco_usuarios.inserir_dados(usuario_valido_fora_bd)

      @mark.create_user_failure_user_existing
      def test_quando_programa_cria_usuario_recebe_dados_usuario_deve_retornar_exception_usuario_existe(self, usuario_valido_dentro_bd):
         with raises(Exception) as erro:
            banco_usuarios.inserir_dados(usuario_valido_dentro_bd)
         assert f'Usuário com o email: {usuario_valido_dentro_bd.email} foi encontrado no sistema, a criação de usuário foi cancelada' in str(erro.value)

      @mark.create_user_failure_data_validation
      def test_quando_programa_cria_usuario_recebe_dados_usuario_deve_retornar_exception_usuario_nome(self):
         with raises(Exception) as erro:
            banco_usuarios.inserir_dados(Usuario(0, '', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20.jpg'))
         assert 'O nome não condiz com a diretrizes do sistema' in str(erro.value)

   @mark.login_user
   class TestClassUsuarioLogin:
      @mark.login_user_success
      def test_quando_programa_tenta_logar_recebe_dados_usuario_deve_retornar_usuario(self, usuario_valido_dentro_bd):
         assert type(banco_usuarios.ler_dados_usuario(usuario_valido_dentro_bd)) == Usuario

      @mark.login_user_failure
      def test_quando_programa_tenta_logar_recebe_dados_usuario_deve_retornar_exception_usuario(self, usuario_valido_fora_bd2):
         with raises(Exception) as erro:
            banco_usuarios.ler_dados_usuario(usuario_valido_fora_bd2)
         assert 'Nenhum usuário foi encontrado no sistema' in str(erro.value)

      @mark.login_user_failure_data_validation
      def test_quando_programa_tenta_logar_recebe_dados_usuario_deve_retornar_exception_usuario_nome(self):
         with raises(Exception) as erro:
            banco_usuarios.ler_dados_usuario(Usuario(0, '', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20.jpg'))
         assert 'O nome não condiz com a diretrizes do sistema' in str(erro.value)

   @mark.update_user
   class TestClassUsuarioUpdate:
      @mark.update_user_success
      @mark.parametrize("usuario, novo_usuario", [
         (Usuario(1, 'José', 'Jose@gmail.com', '1234', r'E:/2020-02-20.jpg'),Usuario(1, 'Joseane', 'joseane@gmail.com', '1234', r'E:/2020-02-20.jpg')),
         (Usuario(1, 'Joseane', 'joseane@gmail.com', '1234', r'E:/2020-02-20.jpg'),Usuario(1, 'José', 'Jose@gmail.com', '1234', r'E:/2020-02-20.jpg'))
      ])
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_true(self, usuario, novo_usuario):
         assert banco_usuarios.alterar_dados(usuario, novo_usuario)

      @mark.update_user_failure_user_not_existing
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_exception_usuario_nao_existe(self, usuario_valido_fora_bd2, usuario_valido_fora_bd3):
         with raises(Exception) as erro:
            banco_usuarios.alterar_dados(usuario_valido_fora_bd2, usuario_valido_fora_bd3)
         assert 'Nenhum usuário foi encontrado no sistema' in str(erro.value)

      @mark.update_user_failure_user_existing
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_exception_outro_usuario_exite(self, usuario_valido_dentro_bd, usuario_valido_dentro_bd2):
         with raises(Exception) as erro:
            banco_usuarios.alterar_dados(usuario_valido_dentro_bd, usuario_valido_dentro_bd2)
         assert 'E-mail já está cadastrado no sistema' in str(erro.value)

      @mark.update_user_failure_data_validation
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_exception_outro_usuario_nome(self, usuario_valido_dentro_bd):
         with raises(Exception) as erro:
            banco_usuarios.alterar_dados(usuario_valido_dentro_bd, Usuario(0, '', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20.jpg'))
         assert 'O nome não condiz com a diretrizes do sistema' in str(erro.value)

   @mark.delete_user
   class TestClassUsuarioDelete:
      @mark.delete_user_success
      def test_quando_programa_deleta_usuario_recebe_dados_usuario_deve_retornar_true(self, usuario_valido_fora_bd):
         assert banco_usuarios.deletar_dados(usuario_valido_fora_bd)

      @mark.delete_user_failure
      def test_quando_programa_deleta_usuario_recebe_dados_usuario_deve_retornar_exception(self, usuario_valido_fora_bd2):
         with raises(Exception) as erro:
            banco_usuarios.deletar_dados(usuario_valido_fora_bd2)
         assert 'Nenhum usuário foi encontrado no sistema' in str(erro.value)

      @mark.delete_user_failure_data_validation
      def test_quando_programa_deleta_usuario_recebe_dados_usuario_deve_retornar_exception_usuario_nome(self):
         with raises(Exception) as erro:
            banco_usuarios.deletar_dados(Usuario(0, '', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20.jpg'))
         assert 'O nome não condiz com a diretrizes do sistema' in str(erro.value)
