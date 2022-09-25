from Source.BACK_END.UsuarioDAO import UsuarioDAO
from Source.BACK_END.PastasDAO import PastaDAO
from Source.BACK_END.FilmeDAO import FilmeDAO

banco_usuarios = UsuarioDAO('banco_testes.db')
banco_pastas = PastaDAO(banco_usuarios.banco)
banco_filmes = FilmeDAO(banco_usuarios.banco)