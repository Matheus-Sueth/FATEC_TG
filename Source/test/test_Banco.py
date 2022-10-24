from pytest import raises, mark, fixture
from Source.test.db_demo import UsuarioDAO

@mark.database
class TestClassBanco:
    @mark.database_success
    def test_quando_programa_valida_estrutura_banco_retorna_true(self):
        banco = UsuarioDAO('banco_testes.db')
        return banco.validar_estrutura_banco()

    @mark.database_failure
    def test_quando_programa_valida_estrutura_banco_retorna_exception_banco(self):
        with raises(Exception) as erro:
            banco = UsuarioDAO('banco_testes2.db')
            chave = 'usuario'
            return banco.validar_estrutura_banco()
        assert f'A estrura da tabela({chave}) não está com de acordo com as diretrizes do sistema' in str(erro.value)