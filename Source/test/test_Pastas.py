from Source.BACK_END.ControleDeTela import *
from Source.BACK_END.Pastas import Pasta
from Source.BACK_END.Colecao import Colecao
from Source.BACK_END.Usuario import Usuario
from pytest import raises, mark, fixture
from os.path import isfile
from Source.test.db_demo import banco_pastas

ambiente='HMG'

@fixture
def usuario_dentro_bd():
    return Usuario(1, 'Matheus', 'matheus@gmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def usuario_fora_bd():
    return Usuario(3, 'Mateuz', 'mateuz@gmail.com', '4567', 'E:/2020-02-20.jpg')

@fixture
def pasta_valida_bd_validation_folders_success():
    return Pasta(1, 1, r'D:/Filmes', r'D:/Imagens_Filmes', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@fixture
def pasta_valida_bd_validation_folders_failure_imagem():
    return Pasta(1, 1, r'D:/Filmes', r'', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@fixture
def pasta_valida_bd_validation_folders_failure_filme():
    return Pasta(1, 1, r'', r'D:/Imagens_Filmes', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@fixture
def pasta_valida_bd_create_folders():
    return Pasta(1, 1, r'D:/Filmes', r'D:/Imagens_Filmes', r'E:\Matheus\Arquivos\Linguagens\Python\tg\Source\banco.db')

@mark.folders
class TestClassPastas:
    @mark.validation_folders
    class TestClassPastasValidation:
        @mark.validation_folders_success
        def test_quando_programa_validar_pastas_usuario_recebe_pasta_deve_retornar_true(self, pasta_valida_bd_validation_folders_success):
            assert banco_pastas.validar_pastas(pasta_valida_bd_validation_folders_success, ambiente)

        @mark.validation_folders_failure_imagem
        def test_quando_programa_validar_pastas_usuario_recebe_pasta_deve_retornar_exception_imagem(self, pasta_valida_bd_validation_folders_failure_imagem):
            with raises(Exception):
                assert banco_pastas.validar_pastas(pasta_valida_bd_validation_folders_failure_imagem, ambiente)

        @mark.validation_folders_failure_filme
        def test_quando_programa_validar_pastas_usuario_recebe_pasta_deve_retornar_exception_filme(self, pasta_valida_bd_validation_folders_failure_filme):
            with raises(Exception):
                assert banco_pastas.validar_pastas(pasta_valida_bd_validation_folders_failure_filme, ambiente)

    @mark.create_folders
    class TestClassPastasCreate:
        @mark.create_folders_success
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_true(self, pasta_valida_bd_create_folders, usuario_fora_bd):
            assert banco_pastas.inserir_pastas(pasta_valida_bd_create_folders, usuario_fora_bd, ambiente)

        @mark.create_folders_failure_user_existing
        def test_quando_programa_cria_pastas_usuario_recebe_pasta_deve_retornar_exception_user_existing(self, pasta_valida_bd_create_folders, usuario_dentro_bd):
            with raises(Exception):
                assert banco_pastas.inserir_pastas(pasta_valida_bd_create_folders, usuario_dentro_bd, ambiente)

    @mark.read_folders
    class TestClassPastasRead:
        @mark.read_folders_success
        def test_quando_programa_consulta_pastas_usuario_recebe_usuario_deve_retornar_true(self, usuario_dentro_bd):
            assert type(banco_pastas.ler_pastas_usuario(usuario_dentro_bd, ambiente)) == Pasta

        @mark.read_folders_failure
        def test_quando_programa_consulta_pastas_usuario_recebe_usuario_deve_retornar_exception(self, usuario_fora_bd):
            with raises(Exception):
                assert banco_pastas.ler_pastas_usuario(usuario_fora_bd, ambiente)

    @mark.update_folders
    class TestClassPastasUpdate:
        @mark.update_folders_success
        def test_quando_programa_altera_pastas_usuario_recebe_pastas_deve_retornar_true(self):
            pass