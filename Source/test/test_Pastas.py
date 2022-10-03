from Source.BACK_END.Pastas import Pasta
from Source.BACK_END.Usuario import Usuario
from pytest import raises, mark, fixture
from Source.test.db_demo import banco_pastas

@fixture
def usuario_dentro_bd():
    return Usuario(9, 'Abigail', 'abigail@hotmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def usuario_fora_bd():
    return Usuario(7, 'Spike', 'spike@gmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def pasta_valida_dentro_bd():
    return Pasta(1, 1, r'D:/Filmes', r'D:/Imagens_Filmes', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@fixture
def pasta_valida_fora_bd():
    return Pasta(0, 0, r'D:/Filmes', r'E:/imagens', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@fixture
def pasta_failure_imagem():
    return Pasta(1, 1, r'D:/Filmes', r'', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@fixture
def pasta_failure_filme():
    return Pasta(1, 1, r'', r'D:/Imagens_Filmes', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@mark.folders
class TestClassPastas:
    @mark.validation_folders
    class TestClassPastasValidation:
        @mark.validation_folders_success
        def test_quando_programa_validar_pastas_recebe_pasta_deve_retornar_true(self, pasta_valida_dentro_bd):
            assert banco_pastas.validar_pastas(pasta_valida_dentro_bd)

        @mark.validation_folders_failure_imagem
        def test_quando_programa_validar_pastas_recebe_pasta_deve_retornar_exception_imagem(self, pasta_failure_imagem):
            with raises(Exception) as erro:
                banco_pastas.validar_pastas(pasta_failure_imagem)
                assert f'Diretório de imagens({pasta_failure_imagem.caminho_imagem}) não foi encontrado' == str(erro.value)

        @mark.validation_folders_failure_filme
        def test_quando_programa_validar_pastas_recebe_pasta_deve_retornar_exception_filme(self, pasta_failure_filme):
            with raises(Exception) as erro:
                banco_pastas.validar_pastas(pasta_failure_filme)
                assert f'Diretório de filmes({pasta.caminho_filme}) não foi encontrado' == str(erro.value)

    @mark.validation_folder_photo
    class TestClassPastasValidationFolderPhoto:
        @mark.validation_folder_photo_success
        def test_quando_programa_verificar_pasta_imagem_recebe_pasta_deve_retornar_true(self, pasta_valida_fora_bd):
            assert banco_pastas.verificar_pasta_imagem(pasta_valida_fora_bd)

        @mark.validation_folder_photo_failure_imagem
        def test_quando_programa_verificar_pasta_imagem_recebe_pasta_deve_retornar_exception_imagem(self, pasta_valida_dentro_bd):
            with raises(Exception) as erro:
                banco_pastas.verificar_pasta_imagem(pasta_valida_dentro_bd)
                assert 'Essa pasta de imagem já existe no banco de dados' == str(erro.value)

    @mark.create_folders
    class TestClassPastasCreate:
        @mark.create_folders_success
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_true(self, pasta_valida_fora_bd, usuario_dentro_bd):
            assert banco_pastas.inserir_pastas(pasta_valida_fora_bd, usuario_dentro_bd)

        @mark.create_folders_failure_photo
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_imagem(self, pasta_failure_imagem, usuario_fora_bd):
            with raises(Exception) as erro:
                banco_pastas.inserir_pastas(pasta_failure_imagem, usuario_dentro_bd)
                assert f'Diretório de filmes({pasta_failure_imagem.caminho_imagem}) não foi encontrado' == str(erro.value)

        @mark.create_folders_failure_movie
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_filme(self, pasta_failure_filme,usuario_fora_bd):
            with raises(Exception) as erro:
                banco_pastas.inserir_pastas(pasta_failure_filme, usuario_dentro_bd)
                assert f'Diretório de filmes({pasta_failure_filme.caminho_filme}) não foi encontrado' == str(erro.value)

        @mark.create_folders_failure_user_existing
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_user_existing(self, pasta_valida_fora_bd, usuario_dentro_bd):
            with raises(Exception) as erro:
                banco_pastas.inserir_pastas(pasta_valida_bd_create_folders, usuario_dentro_bd)
                assert f'O usuário {usuario_dentro_bd.nome} já possui pastas cadastradas' == str(erro.value)

        @mark.create_folders_failure_photo_existing
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_photo_existing(self,pasta_valida_fora_bd,usuario_fora_bd):
            with raises(Exception) as erro:
                banco_pastas.inserir_pastas(pasta_valida_fora_bd, usuario_fora_bd)
                assert 'Essa pasta de imagem já existe no banco de dados' == str(erro.value)

    @mark.read_folders
    class TestClassPastasRead:
        @mark.read_folders_success
        def test_quando_programa_consulta_pastas_usuario_recebe_usuario_deve_retornar_true(self, usuario_dentro_bd):
            assert type(banco_pastas.ler_pastas_usuario(usuario_dentro_bd)) == Pasta

        @mark.read_folders_failure
        def test_quando_programa_consulta_pastas_usuario_recebe_usuario_deve_retornar_exception(self, usuario_fora_bd):
            with raises(Exception) as erro:
                banco_pastas.ler_pastas_usuario(usuario_fora_bd)
                assert f'Nenhuma pasta foi encontrada para o usuário {usuario_fora_bd.nome}' == str(evento.value)

    @mark.update_folders
    class TestClassPastasUpdate:
        @mark.update_folders_success
        def test_quando_programa_altera_pastas_usuario_recebe_pastas_deve_retornar_true(self):
            pass

        @mark.update_folders_failure_photo
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_imagem(self,pasta_valida_dentro_bd, pasta_failure_imagem, usuario_dentro_bd):
            with raises(Exception) as erro:
                banco_pastas.alterar_pastas(pasta_valida_dentro_bd, pasta_failure_imagem, usuario_dentro_bd)
                assert f'Diretório de filmes({pasta_failure_imagem.caminho_imagem}) não foi encontrado' == str(erro.value)

        @mark.update_folders_failure_movie
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_filme(self, pasta_valida_dentro_bd, pasta_failure_filme, usuario_dentro_bd):
            with raises(Exception) as erro:
                banco_pastas.alterar_pastas(pasta_valida_dentro_bd, pasta_failure_filme, usuario_dentro_bd)
                assert f'Diretório de filmes({pasta_failure_filme.caminho_filme}) não foi encontrado' == str(erro.value)

        @mark.update_folders_failure_user_not_existing
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_usuario_nao_existe(self, pasta_valida_dentro_bd, pasta_valida_fora_bd, usuario_fora_bd):
            with raises(Exception) as erro:
                banco_pastas.alterar_pastas(pasta_valida_dentro_bd, pasta_valida_fora_bd, usuario_fora_bd)
                assert False
                #assert not (f'uma pasta foi encontrada para o usuário {usuario_fora_bd.nome}' == str(erro.value))

        @mark.update_folders_failure_photo_existing
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_imagem_existe(self, pasta_valida_dentro_bd, pasta_valida_fora_bd, usuario_fora_bd):
            with raises(Exception) as erro:
                banco_pastas.alterar_pastas(pasta_valida_dentro_bd, pasta_failure_filme, usuario_dentro_bd)
                assert 'Essa pasta de imagem já existe no banco de dados' == str(erro.value)
