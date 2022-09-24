from BACK_END.ControleDeTela import *
from BACK_END.Usuario import Usuario
from BACK_END.PastasDAO import Colecao
from pytest import raises, mark, fixture

ambiente = 'HMG'

@fixture
def usuario_valido_fora_bd_create_user_success():
   '''Retorna um usuário válido que não está no banco de dados para ser usado no create_user_success'''
   return Usuario(3, 'Fanta Uva', 'fanta.uva@yahoo.com', 'uvamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd_create_user_failure_user_existing():
   '''Retorna um usuário válido que está no banco de dados para sr usado no create_user_failure_user_existing'''
   return Usuario(1, 'Matheus', 'matheus@gmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd_login_user_success():
   '''Retorna um usuário válido que está no banco de dados para ser usado no login_user_success'''
   return Usuario(2, 'Teste', 'teste@gmail.com', 'teste', 'E:/0b8c081b7b05dcc0aad6238856ea87d2.gif')

@fixture
def usuario_valido_fora_bd_login_user_failure():
   '''Retorna um usuário válido que não está no banco de dados para ser usado no login_user_failure'''
   return Usuario(4, 'Fanta Laranja', 'fanta.laranja@yahoo.com', 'laranjamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd_update_user_success():
   '''Retorna um usuário válido que está no banco de dados para ser usado no update_user_success'''
   return Usuario(1, 'Matheus', 'matheus@gmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def usuario_valido_fora_bd_update_user_failure_user_old():
   '''Retorna um usuário válido que não está no banco de dados para ser usado no update_user_failure_user_old'''
   return Usuario(4, 'Fanta Laranja', 'fanta.laranja@yahoo.com', 'laranjamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd_update_user_failure_user_changed_1():
   '''Retorna um usuário válido que está no banco de dados para ser usado no update_user_failure_user_changed'''
   return Usuario(2, 'Teste', 'teste@gmail.com', 'teste', 'E:/0b8c081b7b05dcc0aad6238856ea87d2.gif')

@fixture
def usuario_valido_dentro_bd_update_user_failure_user_changed_2():
   '''Retorna um usuário válido que está no banco de dados para ser usado no update_user_failure_user_changed'''
   return Usuario(3, 'Fanta Uva', 'fanta.uva@yahoo.com', 'uvamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_dentro_bd_delete_user_success():
   '''Retorna um usuário válido que está no banco de dados para ser usado no delete_user_success'''
   return Usuario(3, 'Fanta Uva', 'fanta.uva@yahoo.com', 'uvamais2l', r'E:/2020-02-20.jpg')

@fixture
def usuario_valido_fora_bd_delete_user_failure():
   '''Retorna um usuário válido que não está no banco de dados para ser usado no delete_user_failure'''
   return Usuario(4, 'Fanta Laranja', 'fanta.laranja@yahoo.com', 'laranjamais2l', r'E:/2020-02-20.jpg')


@mark.user
class TestClassUsuario:
   @mark.data_validation
   class TestClassUsuarioValidation:
      @mark.data_validation_success
      @mark.parametrize("usuario", [
         (Usuario(3, 'Fanta Uva', 'fanta.uva@yahoo.com', 'uvamais2l', r'E:/2020-02-20.jpg')),
         (Usuario(4, 'Fanta Laranja', 'fanta.laranja@yahoo.com', 'laranjamais2l', r'E:/2020-02-20.jpg')),
         (Usuario(1, 'Matheus', 'matheus@gmail.com', '1234', 'E:/2020-02-20.jpg')),
         (Usuario(2, 'Teste', 'teste@gmail.com', 'teste', 'E:/0b8c081b7b05dcc0aad6238856ea87d2.gif')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_true(self, usuario):
         assert banco_usuarios.validar_dados_usuario(usuario, ambiente)

      @mark.data_validation_failure_nome
      @mark.parametrize("usuario", [
         (Usuario(0, '', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20.jpg')),
         (Usuario(0, 'mi', 'miguelcunha@gmail.com', 'cunha@1234', r'E:/imagens/perfil.jpg')),
         (Usuario(0, 'emilly92', 'emilly92@yahoo.com.br', 'emilly92@1234', r'E:/2020-02-20.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_nome(self, usuario):
         with raises(Exception):
            assert banco_usuarios.validar_dados_usuario(usuario, ambiente)

      @mark.data_validation_failure_foto
      @mark.parametrize("usuario", [
         (Usuario(0, 'UsuarioTeste', 'usuario.teste@gmail.com', 'usuario@1234', r'E:/2020-02-20')),
         (Usuario(0, 'miguel cunha', 'miguelcunha@gmail.com', 'cunha@1234', r'')),
         (Usuario(0, 'emilly', 'emilly92@yahoo.com.br', 'emilly92@1234', r'E:/imagens/')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_foto(self, usuario):
         with raises(Exception):
            assert banco_usuarios.validar_dados_usuario(usuario, ambiente)

      @mark.data_validation_failure_email
      @mark.parametrize("usuario", [
         (Usuario(0, 'UsuarioTeste', 'usuario.testegmail.com', 'usuario@1234', r'E:/2020-02-20.jpg')),
         (Usuario(0, 'miguel cunha', 'miguelcunha@com', 'cunha@1234', r'E:/imagens/perfil.jpg')),
         (Usuario(0, 'emilly', '', 'emilly92@1234', r'E:/imagens/perfil.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_email(self, usuario):
         with raises(Exception):
            assert banco_usuarios.validar_dados_usuario(usuario, ambiente)

      @mark.data_validation_failure_senha
      @mark.parametrize("usuario", [
         (Usuario(0, 'UsuarioTeste', 'usuario.teste@gmail.com', '', r'E:/2020-02-20.jpg')),
         (Usuario(0, 'miguel cunha', 'miguelcunha@hotmail.com', 'c', r'E:/imagens/perfil.jpg')),
         (Usuario(0, 'emilly', 'emilly92@yahoo.com', '123', r'E:/imagens/perfil.jpg')),
      ])
      def test_quando_programa_valida_dados_recebe_dados_usuario_deve_retornar_exception_senha(self, usuario):
         with raises(Exception):
            assert banco_usuarios.validar_dados_usuario(usuario, ambiente)

   @mark.create_user
   class TestClassUsuarioCreate:
      @mark.create_user_success
      def test_quando_programa_cria_usuario_recebe_dados_usuario_deve_retornar_true(self, usuario_valido_fora_bd_create_user_success):
         assert banco_usuarios.inserir_dados(usuario_valido_fora_bd_create_user_success, ambiente)

      @mark.create_user_failure_user_existing
      def test_quando_programa_cria_usuario_recebe_dados_usuario_deve_retornar_exception_user_existing(self, usuario_valido_dentro_bd_create_user_failure_user_existing):
         with raises(Exception):
            assert banco_usuarios.inserir_dados(usuario_valido_dentro_bd_create_user_failure_user_existing, ambiente)

   @mark.login_user
   class TestClassUsuarioLogin:
      @mark.login_user_success
      def test_quando_programa_tenta_logar_recebe_dados_usuario_deve_retornar_usuario(self, usuario_valido_dentro_bd_login_user_success):
         assert type(banco_usuarios.ler_dados_usuario(usuario_valido_dentro_bd_login_user_success, ambiente)) == Usuario

      @mark.login_user_failure
      def test_quando_programa_tenta_logar_recebe_dados_usuario_deve_retornar_exception_usuario(self, usuario_valido_fora_bd_login_user_failure):
         with raises(Exception):
            assert banco_usuarios.ler_dados_usuario(usuario_valido_fora_bd_login_user_failure, ambiente)

   @mark.read_user
   class TestClassUsuarioRead:
      @mark.read_user_success
      def test_quando_programa_consulta_usuarios_recebe_caminho_banco_deve_retornar_colecao_usuarios(self):
         assert type(banco_usuarios.ler_dados(ambiente)) == Colecao

   @mark.update_user
   class TestClassUsuarioUpdate:
      @mark.update_user_success
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_true(self, usuario_valido_dentro_bd_update_user_success):
         novo_usuario = Usuario(usuario_valido_dentro_bd_update_user_success.id, usuario_valido_dentro_bd_update_user_success.nome, 'email.novo@hotmail.com', usuario_valido_dentro_bd_update_user_success.senha, usuario_valido_dentro_bd_update_user_success.foto)
         assert banco_usuarios.alterar_dados(usuario_valido_dentro_bd_update_user_success, novo_usuario, ambiente)

      @mark.update_user_failure_user_old
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_exception_usuario_antigo(self, usuario_valido_fora_bd_update_user_failure_user_old):
         with raises(Exception):
            novo_usuario = Usuario(usuario_valido_fora_bd_update_user_failure_user_old.id, usuario_valido_fora_bd_update_user_failure_user_old.nome, 'email.novo@hotmail.com', usuario_valido_fora_bd_update_user_failure_user_old.senha, usuario_valido_fora_bd_update_user_failure_user_old.foto)
            assert banco_usuarios.alterar_dados(usuario_valido_fora_bd_update_user_failure_user_old, novo_usuario, ambiente)

      @mark.update_user_failure_user_changed
      def test_quando_programa_altera_usuario_recebe_dados_usuario_retornar_exception_usuario_alterado(self, usuario_valido_dentro_bd_update_user_failure_user_changed_1, usuario_valido_dentro_bd_update_user_failure_user_changed_2):
         with raises(Exception):
            assert banco_usuarios.alterar_dados(usuario_valido_dentro_bd_update_user_failure_user_changed_1, usuario_valido_dentro_bd_update_user_failure_user_changed_2, ambiente)

   @mark.delete_user
   class TestClassUsuarioDelete:
      @mark.delete_user_success
      def test_quando_programa_deleta_usuario_recebe_dados_usuario_deve_retornar_true(self, usuario_valido_dentro_bd_delete_user_success):
         assert banco_usuarios.deletar_dados(usuario_valido_dentro_bd_delete_user_success, ambiente)

      @mark.delete_user_failure
      def test_quando_programa_deleta_usuario_recebe_dados_usuario_deve_retornar_exception(self, usuario_valido_fora_bd_delete_user_failure):
         with raises(Exception):
            assert banco_usuarios.deletar_dados(usuario_valido_fora_bd_delete_user_failure, ambiente)
