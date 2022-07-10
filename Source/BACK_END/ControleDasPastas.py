from os import listdir, walk
from os.path import join, realpath
import BACK_END.PastasDAO as ptdao
import BACK_END.FilmeDAO as fldao
import BACK_END.Filme as fl
from tkinter.messagebox import showinfo, showwarning, askquestion, showerror, askyesno
from tkinter import filedialog
import BACK_END.ControleDeUsuario as cdu
import re

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

def selecionar_arquivo(filetypes=''):
    filetypes = (("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("jfif files", "*.jfif"), ("png files", "*.png"))
    filename = filedialog.askopenfilename(
        title='Escolha o Arquivo',
        filetypes=filetypes,
        initialdir='/')
    if filename == '':
        return False
    else:
        return filename

def listar_caminho_arquivo(caminho_filme, filme):
    for diretorio, subpastas, arquivos in walk(caminho_filme):
        for arquivo in arquivos:
            if filme == arquivo:
                return join(realpath(diretorio), arquivo)
    return 'erro'

def verificar_arquivos(caminho):
    aux_lista = []
    for diretorio, subpastas, arquivos in walk(caminho):
        for arquivo in arquivos:
            aux_lista.append(f'{diretorio}/{arquivo}')
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
        mostrar_mensagem(diretorio, 'Diretório Escolhido')

    return diretorio

def verifica_caminho_imagens(caminho):
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

def verifica_caminho_filmes(caminho):
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

root = cdu.root
caminho = cdu.pastas
banco_pastas = ptdao.PastaDAO(caminho.caminho_banco)
if not banco_pastas.conferir_banco():
    mensagem = f'Contate o desenvolvedor no número (11) 96985-8000'
    showwarning(
        title='ATENÇÃO',
        message=mensagem
    )
    exit()
lista_pastas = banco_pastas.ler_dados()
banco_filmes = fldao.FilmeDAO(caminho.caminho_banco)
banco_usuarios = cdu.banco_usuarios

def criar_pastas():
    caminhos = []
    while True:
        cam_filme = escolher_diretorio('Escolha o diretório dos filmes')
        if cam_filme != False:
            caminhos.append(cam_filme)
            break
        else:
            resposta = perguntar("AVISO", "Você quer continuar?")
            if not resposta:
                mostrar_mensagem('Até a próxima')
                exit()

    while True:
        cam_imagem = escolher_diretorio('Escolha o diretório das imagens')
        if cam_imagem != False:
            caminhos.append(cam_imagem)
            break
        else:
            resposta = perguntar("AVISO", "Você quer continuar?")
            if not resposta:
                mostrar_mensagem('Até a próxima')
                exit()
    return caminhos[0],caminhos[1]

def verificar_pastas(caminho):
    alteracao = False
    try:
        listdir(caminho.caminho_filme)
        alteracao = perguntar('AVISO','Deseja alterar seu diretório dos filmes?')
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

    if alteracao:
        while True:
            cam_filme = escolher_diretorio('Escolha o diretório dos filmes')
            if cam_filme != False:
                caminho.caminho_filme = cam_filme
                break
            else:
                resposta = perguntar("AVISO", "Deseja sair do aplicativo?")
                if resposta:
                    mostrar_mensagem('Até a próxima')
                    exit()
                else:
                    resposta = perguntar("AVISO", "Deseja manter o diretório antigo?")
                    if resposta:
                        break

    alteracao = False
    try:
        listdir(caminho.caminho_imagem)
        alteracao = perguntar('AVISO', 'Deseja alterar seu diretório dos filmes?')
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


    if alteracao:
        while True:
            alteracao = True
            cam_imagem = escolher_diretorio('Escolha o diretório das imagens')
            if cam_imagem != False:
                caminho.caminho_imagem = cam_imagem
                break
            else:
                resposta = perguntar("AVISO", "Deseja sair do aplicativo?")
                if resposta:
                    mostrar_mensagem('Até a próxima')
                    exit()
                else:
                    resposta = perguntar("AVISO", "Deseja manter o diretório antigo?")
                    if resposta:
                        break
    return caminho