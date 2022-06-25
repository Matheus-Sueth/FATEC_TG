from tkinter import *
from os.path import exists
import BACK_END.Pastas as pt
import BACK_END.UsuarioDAO as usdao
from tkinter.messagebox import showwarning
from pathlib import Path

pastas = pt.Pasta('','','banco.db')
lista_usuarios = []
root = Tk()
win_width = 140
win_height = 20
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height))
root.geometry(f"{win_width+100}x{win_height}+{start_x}+{start_y-200}")
root.resizable(False, False)
w = Label(root, text='VERIFICANDO PASTAS', font="50")
w.pack()

def atualiza_banco(banco_usuarios):
    auxiliar = banco_usuarios.ler_dados()
    if auxiliar == False:
        mensagem = f'Exclua o banco de dados e faça outro'
        showwarning(
            title='ATENÇÃO',
            message=mensagem
        )
        exit()
    elif auxiliar == True:
        mensagem = f'Tabela usuarios possui campos vazios\nPor favor arrume'
        showwarning(
            title='ATENÇÃO',
            message=mensagem
        )
        exit()
    else:
        return auxiliar


if exists(pastas.caminho_banco):
    pastas.caminho_banco = Path('banco.db').absolute()
    banco_usuarios = usdao.UsuarioDAO(pastas.caminho_banco)
    lista_usuarios = atualiza_banco(banco_usuarios)
else:
    nome_banco = 'banco.db'
    banco_usuarios = usdao.UsuarioDAO(nome_banco)
    pastas.caminho_banco = Path(nome_banco).absolute()
    try:
        banco_usuarios.cursor.execute(
            'CREATE TABLE "usuario" ('
            ' "id" INTEGER,'
            ' "nome" TEXT,'
            ' "email" TEXT,'
            ' "senha" TEXT,'
            ' "foto" TEXT,'
            ' PRIMARY KEY("id") )')
    except:
        mensagem = f'Contate o desenvolvedor no número (11) 96985-8000'
        showwarning(
            title='ATENÇÃO',
            message=mensagem
        )
        exit()
    try:
        banco_usuarios.cursor.execute(
            'CREATE TABLE "filmes" ('
            ' "id"	TEXT,'
            ' "usuario_id"	INTEGER,'
            ' "titulo"	TEXT,'
            ' "ano"	INTEGER,'
            ' "nota"	TEXT,'
            ' "genero"	TEXT,'
            ' "extensao"	TEXT,'
            ' "cam_filme"	TEXT,'
            ' "cam_imagem"	TEXT,'
            ' "qtd_assistido"	INTEGER,'
            ' "sinopse"	TEXT,'
            ' FOREIGN KEY("usuario_id") REFERENCES "usuario"("id"),'
            ' PRIMARY KEY("id") )' )
    except:
        mensagem = f'Contate o desenvolvedor no número (11) 96985-8000'
        showwarning(
            title='ATENÇÃO',
            message=mensagem
        )
        exit()
    try:
        banco_usuarios.cursor.execute(
            'CREATE TABLE "pastas" ('
            ' "id"	INTEGER,'
            ' "usuario_id"	INTEGER,'
            ' "filme"	TEXT,'
            ' "imagem"	TEXT,'
            ' "banco"	TEXT,'
            ' FOREIGN KEY("usuario_id") REFERENCES "usuario"("id"),'
            ' PRIMARY KEY("id") )')
    except:
        mensagem = f'Contate o desenvolvedor no número (11) 96985-8000'
        showwarning(
            title='ATENÇÃO',
            message=mensagem
        )
        exit()
w.destroy()