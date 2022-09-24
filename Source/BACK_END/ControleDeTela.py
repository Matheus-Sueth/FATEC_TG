from BACK_END.UsuarioDAO import UsuarioDAO
from BACK_END.PastasDAO import PastaDAO
from BACK_END.FilmeDAO import FilmeDAO
from BACK_END.Pastas import Pasta
from os import listdir, walk
from os.path import join, realpath
import re
from tkinter.messagebox import showinfo, showwarning, askquestion, showerror, askyesno
from tkinter import filedialog, Tk

def mostrar_mensagem(mensagem,tipo='info'):
    if tipo == 'info':
        showinfo(
            title='INFORMAÇÃO',
            message=mensagem
        )
    elif tipo == 'aviso':
        showwarning(
            title='ATENÇÃO',
            message=mensagem
        )
    elif tipo == 'erro':
        showerror(
            title='ALERTA',
            message=mensagem
        )
    else:
        showinfo(
            title=tipo,
            message=mensagem
        )

def perguntar(titulo,mensagem):
    return askyesno(titulo, mensagem)

def verificar_arquivos(caminho):
    aux_lista = []
    for diretorio, subpastas, arquivos in walk(caminho):
        for arquivo in arquivos:
            aux_lista.append(fr'{diretorio}/{arquivo}')
    return aux_lista

def formata_string(texto):
    aux = set()
    for i in range(len(texto)):
        try:
            aux.add(texto.index('.', i, len(texto)))
        except:
            break
    return max(aux)

def escolher_diretorio(title):
    diretorio = filedialog.askdirectory(
        title=title,
        initialdir='/'
    )

    if diretorio == '':
        return False
    else:
        mostrar_mensagem(f'Pasta = {diretorio}', 'Diretório Escolhido')

    return diretorio

def verifica_caminho_imagens(caminho: Pasta):
    lista_imagem = [imagem[:formata_string(imagem) - len(imagem)] for imagem in verificar_arquivos(caminho.caminho_imagem)]
    for imagem in lista_imagem:
        busca = re.search(r'[a-zA-Zà-úÁ-Úà-ùÀ-Ù\d\Wº]+[\s]{1}[(][\d]{4}[)]', imagem)
        if not busca:
            mensagem = f'O arquivo {imagem} não está com nome adequado, arrume se quiser continuar\nExemplo: titulo (ano).extensao'
            mostrar_mensagem(mensagem)
            exit()
        contador = lista_imagem.count(imagem)
        if contador > 1:
            mensagem = f'Na pasta {caminho.caminho_imagem}, existe {contador} arquivos com o mesmo nome {imagem}, remova os arquivos em excesso'
            mostrar_mensagem(mensagem)
            exit()

def verifica_caminho_filmes(caminho: Pasta):
    lista_filme = [filme[:formata_string(filme) - len(filme)] for filme in verificar_arquivos(caminho.caminho_filme)]
    for filme in lista_filme:
        busca = re.search(r'[a-zA-Zà-úÁ-Úà-ùÀ-Ù\d\Wº]+[\s]{1}[(][\d]{4}[)]', filme)
        if not busca:
            mensagem = f'O arquivo {filme} não está com nome adequado, arrume se quiser continuar\nExemplo: titulo (ano).extensao'
            mostrar_mensagem(mensagem)
            exit()
        contador = lista_filme.count(filme)
        if contador > 1:
            mensagem = f'Na pasta {caminho.caminho_filme} existe {contador} arquivos com o mesmo nome {filme}, remova os arquivos em excesso'
            mostrar_mensagem(mensagem)
            exit()

def criar_pastas():
    while True:
        cam_filme = escolher_diretorio('Escolha o diretório dos filmes')
        if cam_filme != False:
            break
        else:
            resposta = perguntar("AVISO", "Você quer continuar?")
            if not resposta:
                mostrar_mensagem('Até a próxima')
                exit()

    while True:
        cam_imagem = escolher_diretorio('Escolha o diretório das imagens')
        if cam_imagem != False:
            break
        else:
            resposta = perguntar("AVISO", "Você quer continuar?")
            if not resposta:
                mostrar_mensagem('Até a próxima')
                exit()
    return cam_filme, cam_imagem

def verificar_pastas(caminho: Pasta):
    try:
        listdir(caminho.caminho_filme)
    except:
        while True:
            cam_filme = escolher_diretorio('Escolha o diretório dos filmes')
            if cam_filme != False:
                caminho.caminho_filme = cam_filme
                break
            else:
                resposta = perguntar("AVISO", "Você quer continuar?")
                if not resposta:
                    mostrar_mensagem('Até a próxima')
                    exit()

    try:
        listdir(caminho.caminho_imagem)
    except:
        while True:
            cam_imagem = escolher_diretorio('Escolha o diretório das imagens')
            if cam_imagem != False:
                caminho.caminho_imagem = cam_imagem
                break
            else:
                resposta = perguntar("AVISO", "Você quer continuar?")
                if not resposta:
                    mostrar_mensagem('Até a próxima')
                    exit()

    return caminho

root = Tk()
banco_usuarios = UsuarioDAO('banco.db')
if not banco_usuarios.validar_estrutura_banco():
    mensagem = f'Contate o desenvolvedor no número (11) 96985-8000'
    showwarning(
        title='ATENÇÃO',
        message=mensagem
    )
    exit()
banco_pastas = PastaDAO(banco_usuarios.banco)
banco_filmes = FilmeDAO(banco_usuarios.banco)

