from Source.BACK_END.Usuario import Usuario
from Source.BACK_END.Filme import Filme
from Source.BACK_END.Colecao import Colecao
from pytest import raises, mark, fixture
from Source.test.db_demo import banco_filmes

@fixture
def usuario_dentro_bd():
    return Usuario(9, 'Abigail', 'abigail@hotmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def usuario_fora_bd():
    return Usuario(7, 'Spike', 'spike@gmail.com', '1234', 'E:/2020-02-20.jpg')

@fixture
def filme_valido_dentro_bd():
    return Filme(
            id='1.250546',
            titulo='Annabelle',
            ano=2014,
            nota='NÃO ASSISTIDO',
            genero='Terror',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\Annabelle/Annabelle (2014).mp4',
            cam_imagem=r'D:/Imagens_Filmes/Annabelle (2014).png',
            sinopse='Um casal se prepara para a chegada de sua primeira filha e compra para ela uma boneca. quando sua casa é invadida por membros de uma seita, o casal é violentamente atacado e a boneca, annabelle, se torna recipiente de uma entidade do mal.'
    )

@fixture
def filme_valido_fora_bd():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.'
    )

@fixture
def filme_valido_fora_bd2():
    return Filme(
            id='1.64688',
            titulo='Anjos da Lei',
            ano=2012,
            nota='NÃO ASSISTIDO',
            genero='Ação/Comédia/Crime',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\Anjos da Lei/Anjos da Lei (2012).mp4',
            cam_imagem=r'D:/Imagens_Filmes/Anjos da Lei (2012).png',
            sinopse='Jenko e schmidt estudaram juntos, mas nunca foram amigos. anos depois, os dois se reencontram na academia de polícia e passam a se ajudar. já formados, a dupla se envolve em uma confusão ao tentar prender um traficante. por causa de seu desempenho catastrófico, eles são remanejados para trabalhar infiltrados como alunos de ensino médio. eles devem desvendar quem é o fornecedor de uma nova droga em uma escola, enquanto tentam manter seu disfarce de estudantes.'
    )

@fixture
def filme_falha_titulo():
    return Filme(
            id='1.411',
            titulo='',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@fixture
def filme_falha_ano():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2023,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@fixture
def filme_falha_nota():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@fixture
def filme_falha_genero():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@fixture
def filme_falha_extensao():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@fixture
def filme_falha_sinopse():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='',
            valor=0
    )

@fixture
def filme_falha_cam_imagem():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\As Crônicas de Nárnia/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).mp4',
            cam_imagem=r'',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@fixture
def filme_falha_cam_filme():
    return Filme(
            id='1.411',
            titulo='As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa',
            ano=2000,
            nota='NÃO ASSISTIDO',
            genero='Aventura/Família/Fantasia',
            extensao='.mp4',
            cam_filme=r'',
            cam_imagem=r'D:/Imagens_Filmes/As Crônicas de Nárnia - O Leão, A Feiticeira e o Guarda-Roupa (2005).png',
            sinopse='Durante os bombardeios da segunda guerra mundial de londres, quatro irmãos ingleses são enviados para uma casa de campo onde eles estarão seguros. um dia, lucy encontra um guarda-roupa que a transporta para um mundo mágico chamado nárnia. depois de voltar, ela logo volta a nárnia com seus irmãos, peter e edmund, e sua irmã, susan. lá eles se juntam ao leão mágico, aslan, na luta contra a feiticeira branca.',
            valor=0
    )

@mark.movie
class TestClassFilme():
    @mark.validation_movie
    class TestClassFilmeValidation():
        @mark.validation_movie_success
        def test_quando_programa_validar_filme_recebe_filme_deve_retornar_true(self, filme_valido_fora_bd):
            return banco_filmes.validar_filme(filme_valido_fora_bd)

        @mark.validation_movie_failure_title
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_titulo(self, filme_falha_titulo):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_titulo)
            assert 'O titulo do filme deve ser preenchido' in str(erro.value)

        @mark.validation_movie_failure_year
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_ano(self, filme_falha_ano):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_ano)
            assert 'O ano do filme deve ser maior que 1900 e menor ou igual que o ano atual' in str(erro.value)

        @mark.validation_movie_failure_note
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_nota(self, filme_falha_nota):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_nota)
            assert 'A nota do filme deve estar dentro da lista de notas do sistema' in str(erro.value)

        @mark.validation_movie_failure_genre
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_genero(self, filme_falha_genero):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_genero)
            assert 'O genêro do filme deve estar dentro da lista dos genêros do sistema' in str(erro.value)

        @mark.validation_movie_failure_extension
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_extensao(self, filme_falha_extensao):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_extensao)
            assert 'O formato da extensao do filme deve ser(.extensao)' in str(erro.value)

        @mark.validation_movie_failure_overview
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_sinopse(self, filme_falha_sinopse):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_sinopse)
            assert 'A sinopse do filme deve ser preenchida' in str(erro.value)

        @mark.validation_movie_failure_cam_imagem
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_cam_imagem(self, filme_falha_cam_imagem):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_cam_imagem)
            assert 'O caminho da imagem deve existir' in str(erro.value)

        @mark.validation_movie_failure_cam_movie
        def test_quando_programa_validar_filme_recebe_filme_deve_exception_cam_filme(self, filme_falha_cam_filme):
            with raises(Exception) as erro:
                return banco_filmes.validar_filme(filme_falha_cam_filme)
            assert 'O caminho do filme deve existir' in str(erro.value)

    @mark.create_movie
    class TestClassFilmeCreate():
        @mark.create_movie_success
        def test_quando_programa_cria_filme_recebe_filme_usuario_deve_retornar_true(self, filme_valido_fora_bd, usuario_dentro_bd):
            return banco_filmes.inserir_filme(filme_valido_fora_bd, usuario_dentro_bd)

        @mark.create_movie_failure_title
        def test_quando_programa_cria_filme_recebe_filme_deve_exception_titulo(self, filme_falha_titulo, usuario_dentro_bd):
            with raises(Exception) as erro:
                return banco_filmes.inserir_filme(filme_falha_titulo, usuario_dentro_bd)
            assert 'O titulo do filme deve ser preenchido' in str(erro.value)

        @mark.create_movie_failure_movie_existing
        def test_quando_programa_cria_filme_recebe_filme_usuario_deve_retornar_exception_filme_existe(self, filme_valido_dentro_bd, usuario_dentro_bd):
            with raises(Exception) as erro:
                return banco_filmes.inserir_filme(filme_valido_dentro_bd, usuario_dentro_bd)
            assert f'O filme {filme_valido_dentro_bd.titulo} - ano {filme_valido_dentro_bd.ano} está cadastrado' in str(erro.value)

    @mark.read_movie
    class TestClassFilmeRead():
        @mark.read_movie_success
        def test_quando_programa_ve_filme_recebe_usuario_deve_retornar_colecao(self, usuario_dentro_bd):
            resultado = banco_filmes.ver_filmes(usuario_dentro_bd)
            return type(resultado) == Colecao and len(resultado) > 0 and resultado.tipo == 'Filmes'

        @mark.read_movie_usuario_not_existing
        def test_quando_programa_ve_filme_recebe_usuario_deve_retornar_colecao_vazia(self, usuario_fora_bd):
            resultado = banco_filmes.ver_filmes(usuario_fora_bd)
            return type(resultado) == Colecao and len(resultado) == 0 and resultado.tipo == 'Filmes'

    @mark.read_movie_ordered
    class TestClassFilmeReadOrdered():
        @mark.read_movie_ordered_success
        def test_quando_programa_ve_filme_ordenado_recebe_usuario_deve_retornar_colecao(self, usuario_dentro_bd):
            resultado = banco_filmes.ver_filmes_ordenados(usuario_dentro_bd)
            return type(resultado) == Colecao and len(resultado) > 0 and resultado.tipo == 'Filmes ordenados por titulo e ano'

        @mark.read_movie_ordered_usuario_not_existing
        def test_quando_programa_ve_filme_ordenado_recebe_usuario_deve_retornar_colecao_vazia(self, usuario_fora_bd):
            resultado = banco_filmes.ver_filmes_ordenados(usuario_fora_bd)
            return type(resultado) == Colecao and len(resultado) == 0 and resultado.tipo == 'Filmes ordenados por titulo e ano'

    @mark.update_movie
    class TestClassFilmeUpdate():
        @mark.update_movie_success
        @mark.parametrize("filme_alterado", [
            (Filme(
            id='1.250546',
            titulo='Annabelle',
            ano=2014,
            nota='EXCELENTE',
            genero='Terror/Mistério',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\Annabelle/Annabelle (2014).mp4',
            cam_imagem=r'D:/Imagens_Filmes/Annabelle (2014).png',
            sinopse='Um casal se prepara para a chegada de sua primeira filha e compra para ela uma boneca. quando sua casa é invadida por membros de uma seita, o casal é violentamente atacado e a boneca, annabelle, se torna recipiente de uma entidade do mal.'
    )),
            (Filme(
            id='1.250546',
            titulo='Annabelle',
            ano=2014,
            nota='NÃO ASSISTIDO',
            genero='Terror',
            extensao='.mp4',
            cam_filme=r'D:/Filmes\A\Annabelle/Annabelle (2014).mp4',
            cam_imagem=r'D:/Imagens_Filmes/Annabelle (2014).png',
            sinopse='Um casal se prepara para a chegada de sua primeira filha e compra para ela uma boneca. quando sua casa é invadida por membros de uma seita, o casal é violentamente atacado e a boneca, annabelle, se torna recipiente de uma entidade do mal.'
    ))
        ])
        def test_quando_programa_altera_filme_recebe_filme_usuario_deve_retornar_true(self, usuario_dentro_bd, filme_alterado):
            return banco_filmes.alterar_filme(filme_alterado, usuario_dentro_bd)

        @mark.update_movie_failure_title
        def test_quando_programa_altera_filme_recebe_filme_deve_exception_titulo(self, usuario_dentro_bd, filme_falha_titulo):
            with raises(Exception) as erro:
                return banco_filmes.alterar_filme(filme_falha_titulo, usuario_dentro_bd)
            assert 'O titulo do filme deve ser preenchido' in str(erro.value)

        @mark.update_movie_failure_movie_not_existing
        def test_quando_programa_altera_filme_recebe_filme_usuario_deve_retornar_exception_filme_nao_existe(self, usuario_dentro_bd, filme_valido_fora_bd2):
            with raises(Exception) as erro:
                return banco_filmes.alterar_filme(filme_valido_fora_bd2, usuario_dentro_bd)
            assert f'O filme {filme_valido_fora_bd2.titulo} - ano {filme_valido_fora_bd2.ano} não está cadastrado' in str(erro.value)

    @mark.delete_movie
    class TestClassFilmeDelete():
        @mark.delete_movie_success
        def test_quando_programa_deleta_filme_recebe_filme_usuario_deve_retornar_true(self, filme_valido_fora_bd, usuario_dentro_bd):
            return banco_filmes.deletar_filme(filme_valido_fora_bd, usuario_dentro_bd)

        @mark.delete_movie_failure_movie_not_existing
        def test_quando_programa_altera_filme_recebe_filme_usuario_deve_retornar_exception_filme_nao_existe(self, usuario_dentro_bd, filme_valido_fora_bd2):
            with raises(Exception) as erro:
                return banco_filmes.deletar_filme(filme_valido_fora_bd2, usuario_dentro_bd)
            assert f'O filme {filme_valido_fora_bd2.titulo} - ano {filme_valido_fora_bd2.ano} não está cadastrado' in str(erro.value)

    @mark.search_movie
    class TestClassFilmeSearch():
        @mark.parametrize("coluna,texto", [('titulo','anna'),('sinopse','chegada'),('ano',2014),('titulo','cs'),('sinopse','animal'),('ano',2022)])
        def test_quando_programa_procura_filme_recebe_coluna_texto_usuario_deve_retornar_colecao(self, coluna, texto, usuario_dentro_bd):
            resultado = banco_filmes.procurar_filmes(coluna, texto,usuario_dentro_bd)
            return type(resultado) == Colecao and f'Filmes ordenados pela coluna: {coluna}' in resultado.tipo

    @mark.add_attribute_movie
    class TestClassFilmeAddAttribute():
        @mark.add_attribute_movie_success
        def test_quando_programa_deleta_filme_recebe_filme_usuario_deve_retornar_true(self, filme_valido_dentro_bd, usuario_dentro_bd):
            return banco_filmes.somar_atributo_filme(filme_valido_dentro_bd, usuario_dentro_bd)

        @mark.add_attribute_movie_failure_movie_not_existing
        def test_quando_programa_altera_filme_recebe_filme_usuario_deve_retornar_exception_filme_nao_existe(self, filme_valido_fora_bd, usuario_dentro_bd):
            with raises(Exception) as erro:
                return banco_filmes.somar_atributo_filme(filme_valido_fora_bd, usuario_dentro_bd)
            assert f'O filme {filme_valido_fora_bd.titulo} - ano {filme_valido_fora_bd.ano} não está cadastrado' in str(erro.value)

