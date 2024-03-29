from tkinter import *
from tkinter.ttk import Combobox, Progressbar
from PIL import ImageTk
from PIL import Image
from Source.BACK_END.ControleDeTela import *
from Source.BACK_END.Usuario import Usuario
from Source.BACK_END.PastasDAO import PastaDAO
from Source.BACK_END.Pastas import Pasta
from Source.BACK_END.Filme import Filme
from Source.BACK_END.Colecao import Colecao
from Source.BACK_END.APIs import *
import urllib.request
import io
import re
from pathlib import Path
from os.path import isfile
from os import startfile
from random import randint
import datetime
from threading import Thread
import base64
from time import sleep


def tamanho_janela(menu, win_width, win_height):
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    start_x = int((screen_width / 2) - (win_width / 2))
    start_y = int((screen_height / 2) - (win_height / 2))
    menu.iconbitmap('Images/1.ico')
    menu['bg'] = '#154f91'
    menu.geometry(f"{win_width}x{win_height}+{start_x}+{start_y}")
    menu.resizable(False, False)
    menu.update()


class SM:
    def __init__(self, root=None):
        self.teste = 0
        self.root = root
        self.root.title('SM')
        tamanho_janela(self.root, 800, 700)
        #self.root.resizable(False, False)
        self.frame = Frame(self.root, bg='#154f91')
        self.frame.pack()

        self.label_aplicativo = Label(
            self.frame,
            text='SELECT MOVIE SM',
            background='#154f91',
            fg='white',
            width=30,
            font=('Arial Black', 24)
        ).pack(pady=70)

        self.frame_botoes = Frame(self.frame, bg='#154f91')
        self.frame_botoes.pack()

        self.botao_login = Button(
            self.frame_botoes,
            text='LOGIN',
            bg='#154f91',
            fg='white',
            height=2,
            width=15,
            font=('Arial', 18),
            border=15,
            command=self.ir_tela_login
        ).pack(pady=10, side=TOP)
        self.botao_cadastro = Button(
            self.frame_botoes,
            text='CADASTRO',
            bg='#154f91',
            fg='white',
            height=2,
            width=15,
            font=('Arial', 18),
            border=15,
            command=self.ir_tela_cadastro
        ).pack(pady=10)
        self.botao_ajuda = Button(
            self.frame_botoes,
            text='AJUDA',
            bg='#154f91',
            fg='white',
            height=2,
            width=15,
            font=('Arial', 18),
            border=15,
            command=self.ajuda
        ).pack(pady=10)
        self.botao_sobre = Button(
            self.frame_botoes,
            text='SOBRE',
            bg='#154f91',
            fg='white',
            height=2,
            width=15,
            font=('Arial', 18),
            border=15,
            command=self.sobre
        ).pack(pady=10)

    def sobre(self):
        mostrar_mensagem('Esse sistema foi desenvolvido para ajudar no gerenciamento de filmes pagos e de domínio público.'
                         '\nContendo integração ao The Movie Database API para auxiliar o usuário em pesquisas e recomendações de filmes'
                         '\nO uso inadequado do software será de total responsabilidade do usuário','SOBRE O SISTEMA')
        return None

    def ajuda(self):
        print('TELA DE AJUDA')

    def ir_tela_login(self):
        self.frame.pack_forget()
        self.page_Login = Login(master=self.root, app=self)
        self.page_Login.tela_login()

    def ir_tela_cadastro(self):
        self.frame.pack_forget()
        self.page_Cadastro = Cadastro(master=self.root, app=self)
        self.page_Cadastro.tela_cadastro()

    def tela_SM(self):
        self.frame.pack()


class Login:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.master.title('LOGIN')
        tamanho_janela(self.master, 700, 330)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        frame_email = Frame(self.frame, bg='#154f91')
        frame_email.pack(pady=20)
        label_email = Label(
            frame_email,
            text='EMAIL',
            bg='#154f91',
            fg='white',
            anchor=W,
            justify=LEFT,
            width=44,
            font=('Arial', 12)
        )
        label_email.pack(side=TOP)
        self.entrada_email = Entry(
            frame_email,
            text='SENHA',
            #bg='#1e99be',
            #fg='white',
            width=30,
            font=('Arial', 18),
            border=2,
            relief=GROOVE
        )
        self.entrada_email.pack()
        self.entrada_email.insert(0, 'matheus@gmail.com')
        frame_senha = Frame(self.frame, bg='#154f91')
        frame_senha.pack(pady=20)
        label_senha = Label(
            frame_senha,
            text='SENHA',
            bg='#154f91',
            fg='white',
            anchor=W,
            justify=LEFT,
            font=('Arial', 12),
            width=44
        )
        label_senha.pack(side=TOP)
        self.entrada_senha = Entry(
            frame_senha,
            #bg='#1e99be',
            #fg='white',
            width=30,
            font=('Arial', 18),
            border=2,
            relief=GROOVE,
            show='*'
        )
        self.entrada_senha.pack()
        self.entrada_senha.insert(0, '1234')
        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)
        botao = Button(
            frame_botao,
            text='VOLTAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_sm
        )
        botao.pack(padx=10, side=LEFT)
        botao = Button(
            frame_botao,
            text='LOGAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.login
        )
        botao.pack(padx=10, side=LEFT)

    def login(self):
        email = self.entrada_email.get()
        senha = self.entrada_senha.get()
        if email == '':
            mostrar_mensagem('campo EMAIL não foi preenchido','aviso')
            self.entrada_email.focus_set()
        elif senha == '':
            mostrar_mensagem('campo SENHA não foi preenchido', 'aviso')
            self.entrada_senha.focus_set()
        else:
            self.usuario_login = Usuario(0,'Usuario',email,senha,'Images/foto.png')
            try:
                self.usuario = banco_usuarios.ler_dados_usuario(self.usuario_login)
            except Exception as msg:
                mostrar_mensagem(msg,'aviso')
                return None
            try:
                self.pasta_usuario = banco_pastas.ler_pastas_usuario(self.usuario)
            except Exception as msg:
                mostrar_mensagem(msg, 'aviso')
                self.pasta_usuario = Pasta(0,self.usuario.id,'','',banco_usuarios.banco)
                while True:
                    self.pasta_usuario.caminho_filme, self.pasta_usuario.caminho_imagem = criar_pastas()
                    try:
                        banco_pastas.inserir_pastas(self.pasta_usuario, self.usuario)
                        break
                    except Exception as msg:
                        mostrar_mensagem(msg,'aviso')
            self.ir_tela_inicio()

    def tela_login(self):
        self.frame.pack()

    def ir_tela_cadastro(self):
        self.frame.pack_forget()
        self.page_Cadastro = Cadastro(master=self.master, app=self)
        self.page_Cadastro.tela_cadastro()

    def ir_tela_sm(self):
        self.frame.pack_forget()
        self.master.title('SM')
        tamanho_janela(self.master, 800, 700)
        self.app.tela_SM()

    def ir_tela_inicio(self):
        verifica_caminho_filmes(self.pasta_usuario)
        verifica_caminho_imagens(self.pasta_usuario)
        self.frame.pack_forget()
        self.page_Inicio = Inicio(master=self.master, app=self)
        self.page_Inicio.tela_inicio()


class Cadastro:
    def __init__(self, master=None, app=None):
        self.master = master
        self.master.title('CADASTRO')
        tamanho_janela(self.master, 800, 630)
        self.app = app
        self.frame = Frame(self.master, bg='#154f91')
        frame_foto = Frame(self.frame, bg='#154f91')
        frame_foto.pack(pady=20)
        self.caminho_foto = ''

        self.botao_2 = Button(
            frame_foto,
            text='SELECIONAR\nFOTO',
            bg='#334B49',
            fg='white',
            font=('Arial', 22),
            border=5,
            height=4,
            width=15,
            relief=RIDGE,
            command=lambda: self.selecionar_arquivo('Escolha sua foto de perfil'))
        self.botao_2.pack(padx=10)

        frame_nome = Frame(self.frame, bg='#154f91')
        frame_nome.pack(pady=20)

        label_nome = Label(
            frame_nome,
            text='NOME',
            bg='#154f91',
            anchor=W,
            justify=LEFT,
            fg='white',
            font=('Arial', 12),
            width=44)
        label_nome.pack(side=TOP)
        self.entrada_nome = Entry(
            frame_nome,
            #bg='#1e99be',
            #fg='white',
            width=30,
            font=('Arial', 18),
            border=2,
            relief=GROOVE)
        self.entrada_nome.pack()

        frame_email = Frame(self.frame, bg='#154f91')
        frame_email.pack(pady=20)

        label_email = Label(
            frame_email,
            text='EMAIL',
            bg='#154f91',
            anchor=W,
            justify=LEFT,
            fg='white',
            font=('Arial', 12),
            width=44)
        label_email.pack(side=TOP)
        self.entrada_email = Entry(
            frame_email,
            #bg='#1e99be',
            #fg='white',
            width=30,
            font=('Arial', 18),
            border=2,
            relief=GROOVE)
        self.entrada_email.pack()

        frame_senha = Frame(self.frame, bg='#154f91')
        frame_senha.pack(pady=20)

        label_senha = Label(
            frame_senha,
            text='SENHA',
            bg='#154f91',
            anchor=W,
            justify=LEFT,
            fg='white',
            font=('Arial', 12),
            width=44)
        label_senha.pack(side=TOP)
        self.entrada_senha = Entry(
            frame_senha,
            #bg='#1e99be',
            #fg='white',
            width=30,
            font=('Arial', 18),
            border=2,
            relief=GROOVE,
            show='*')
        self.entrada_senha.pack()

        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)

        botao = Button(frame_botao, text='VOLTAR', bg='#154f91', fg='white', height=3, width=30, font=('Arial', 10),
                       border=15, command=self.ir_tela_sm)
        botao.pack(padx=10, side=LEFT)
        botao = Button(frame_botao, text='CRIAR', bg='#154f91', fg='white', height=3, width=30, font=('Arial', 10),
                       border=15, command=self.cadastro)
        botao.pack(padx=10, side=LEFT)

    def selecionar_arquivo(self, title):
        while True:
            caminho = filedialog.askopenfilename(
                filetypes=(("Arquivos jpg", "*.jpg"), ("Arquivos jpeg", "*.jpeg"), ("Arquivos jfif", "*.jfif"), ("Arquivos png", "*.png")),
                title=title,
                initialdir='/')
            if caminho == '':
                resposta = perguntar("AVISO", "Deseja continuar")
                if not resposta:
                    mostrar_mensagem('Tudo bem')
                    return self.caminho_foto
            else:
                break
        try:
            self.caminho_foto = caminho
            im = Image.open(self.caminho_foto)
            im.thumbnail((150, 150))
            self.photoImg = ImageTk.PhotoImage(im)
            self.botao_2.configure(image=self.photoImg, height=150, width=150)
            self.botao_2.update()
        except:
            mostrar_mensagem('Arquivo de imagem corrompido ou inválido', 'erro')

    def cadastro(self):
        if self.caminho_foto == '':
            resposta = perguntar('Aviso','Campo FOTO não foi preenchido\nDeseja utilizar uma imagem padrão?')
            if not resposta:
                self.botao_2.focus_set()
                return None
            else:
                try:
                    self.caminho_foto = 'Images/foto.png'
                    im = Image.open(self.caminho_foto)
                    im.thumbnail((150, 150))
                    self.photoImg = ImageTk.PhotoImage(im)
                    self.botao_2.configure(text='', image=self.photoImg, height=150, width=150)
                except:
                    mostrar_mensagem('Não estou conseguindo acessar a imagem padrão.'
                                     ' Por favor escolha uma foto se deseja continuar.\nSe o erro persistir contate o desenvolvedor')
                    return None
        if self.entrada_nome.get() == '':
            mostrar_mensagem('Campo NOME não foi preenchido', 'aviso')
            self.entrada_nome.focus_set()
        elif self.entrada_email.get() == '':
            mostrar_mensagem('Campo EMAIL não foi preenchido', 'aviso')
            self.entrada_email.focus_set()
        elif self.entrada_senha.get() == '':
            mostrar_mensagem('Campo SENHA não foi preenchido', 'aviso')
            self.entrada_senha.focus_set()
        else:
            foto = self.caminho_foto
            nome = self.entrada_nome.get()
            email = self.entrada_email.get()
            senha = self.entrada_senha.get()
            indice = 0
            self.novo_usuario = Usuario(indice,nome, email, senha, foto)
            try:
                result = banco_usuarios.inserir_dados(self.novo_usuario)
            except Exception as mensagem:
                mostrar_mensagem(mensagem,'aviso')
                return None
            mostrar_mensagem('Usuário Criado\nAgora vamos para a tela de login', 'info')
            self.app.sobre()
            self.ir_tela_login()

    def ir_tela_login(self):
        self.frame.pack_forget()
        self.page_Login = Login(master=self.master, app=self.app)
        self.page_Login.entrada_email.insert(0,self.novo_usuario.email)
        self.page_Login.tela_login()

    def tela_cadastro(self):
        self.frame.pack()

    def ir_tela_sm(self):
        self.frame.pack_forget()
        self.master.title('SM')
        tamanho_janela(self.master, 800, 700)
        self.app.tela_SM()


class Inicio:
    def __init__(self, master=None, app=None):
        self.master = master
        self.master.bind("<MouseWheel>", self.mouse_wheel)
        self.master.bind("<Button-4>", self.mouse_wheel)
        self.master.bind("<Button-5>", self.mouse_wheel)
        self.app = app
        self.usuario = banco_usuarios.ler_dados_usuario(self.app.usuario_login)
        self.pastas = banco_pastas.ler_pastas_usuario(self.usuario)
        self.filmes = banco_filmes.ver_filmes(self.usuario)
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        self.objeto = [[0,840],[24,420],[48,210],[96,105],[192,57],[384,28]]

        self.id = 0
        self.mouse = 0
        self.end_barra = len(self.filmes) // 6 if len(self.filmes) % 6 != 0 or len(self.filmes) == 0 else len(self.filmes) // 6 - 1
        self.sliderlength = [dado[1] for dado in self.objeto if self.end_barra <= dado[0]][0]
        self.barra = Scale(self.frame, from_=self.id, to=self.end_barra, width=25, sliderlength=self.sliderlength, length=850, command=self.vervalor)
        self.barra.pack(side=RIGHT)

        frame_foto = Frame(self.frame, bg='#154f91')
        frame_foto.pack(side=LEFT, fill="both", expand="yes",padx=10)

        try:
            im = Image.open(self.usuario.foto)
            im.thumbnail((130, 130))
            self.photoImg = ImageTk.PhotoImage(im)
        except:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((130, 130))
            self.photoImg = ImageTk.PhotoImage(im)

        self.foto_usuario = Button(
            frame_foto,
            image=self.photoImg,
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=130,
            width=130,
            command=self.logoff
        )
        self.foto_usuario.pack(anchor=NW,fill="both", expand="yes")

        self.label_nome_usuario = Label(
            frame_foto,
            text=self.usuario.nome,
            fg='white',
            font=('Arial', 16),
            bg = '#1A857F',
            width=10,
            bd=2,
            relief=SOLID,
            wraplength=110
        )
        self.label_nome_usuario.pack(fill="both", expand="yes")

        self.botoes = []
        dicionario_botao = {
            0: ['ADICIONAR\nFILME',self.ir_tela_add_filmes],
            1: ['FILME\nALEATÓRIO', self.aleatorio],
            2: ['RECOMENDAÇÃO\nDE FILMES', self.recomendacao],
            3: ['PESQUISAR\nFILME', self.pesquisar_filmes],
            4: ['ORDENAR FILMES\nA-Z', self.ordenar]
        }

        for id in range(5):
            botao = Button(frame_foto, text=dicionario_botao[id][0], bg='#154f91', fg='white',
                       font=('Arial', 10), border=15, command=dicionario_botao[id][1], relief=RAISED)
            self.botoes.append(botao)
            botao.pack(pady=30, side=BOTTOM, anchor=S, fill="both", expand="yes")

        frame_usuario2 = Frame(self.frame, bg='#154f91')
        frame_usuario2.pack(side=RIGHT, anchor=NE,padx=15)

        frame_pesquisa = Frame(frame_usuario2, bg='#154f91')
        frame_pesquisa.pack()
        label_nome_texto = f'{len(self.filmes):>04} Filmes' if len(self.filmes) != 1 else f'{len(self.filmes):>04} Filme'
        self.label_nome = Label(
            frame_pesquisa,
            text=label_nome_texto,
            fg='white',
            font=('Arial', 14),
            bg='#154f91',
            width=10,
            bd=2,
            relief=SOLID,
            wraplength=120
        )
        self.label_nome.pack(fill="both", expand="yes", side=LEFT)
        self.combobox_filtro = Combobox(frame_pesquisa,
                                      state='readonly',
                                      values=['TITULO', 'ANO', 'GENERO', 'NOTA','SINOPSE'],
                                      font=('Arial', 20),
                                      justify=CENTER,
                                      width=10)
        self.combobox_filtro.current(0)
        self.combobox_filtro.pack(fill="both", expand="yes", side=LEFT)
        self.entry_pesquisa = Entry(
            frame_pesquisa,
            width=30,
            font=('Arial', 20),
            border=2,
            relief=GROOVE
        )
        self.entry_pesquisa.pack(side=LEFT,fill="both", expand="yes")
        im = Image.open(r'Images/lupa.png')
        im.thumbnail((30, 30))
        self.pesquisar = ImageTk.PhotoImage(im)
        bt = Button(frame_pesquisa, image=self.pesquisar, bg='#154f91', command=self.procurar_filme)
        bt.pack(side=LEFT,fill="both", expand="yes")

        indice = -1
        self.photoFilme = []
        self.nomes_filmes = []
        self.frames_filmes = []
        self.foto_filmes = []
        self.titulo_filmes = []
        self.dicionario = {}

        for numero in range(6):
            try:
                im = Image.open(rf'{self.filmes[numero].cam_imagem}')
                im.thumbnail((150, 150))
                self.photoFilme.append(ImageTk.PhotoImage(im))
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((150, 150))
                self.photoFilme.append(ImageTk.PhotoImage(im))
            try:
                self.nomes_filmes.append([self.filmes[numero].titulo, self.filmes[numero]])
            except:
                self.nomes_filmes.append(['Filme Não Encontrado', ''])

        for numero in range(6):
            if numero % 3 == 0:
                indice+=1
                frame = Frame(frame_usuario2, bg='#154f91')
                self.frames_filmes.append(frame)
                self.frames_filmes[indice].pack(pady=50, padx=50, fill="both")

            self.frame_foto = Frame(self.frames_filmes[indice], bg='#154f91')
            self.frame_foto.pack(pady=45, padx=45, side=LEFT)

            foto_filme = Button(
                self.frame_foto,
                image=self.photoFilme[numero],
                bg='#334B49',
                border=5,
                relief=RIDGE,
                height=150,
                width=100,
                command=lambda m=self.nomes_filmes[numero]: self.ir_tela_ver_filme(m)
            )
            self.foto_filmes.append([foto_filme, numero])
            foto_filme.pack(side=TOP,fill="both", expand="yes")
            self.label_titulo = Label(
                self.frame_foto,
                text=self.nomes_filmes[numero][0],
                fg='white',
                font=('Arial', 10),
                bg='#1A857F',
                height=3,
                width=21,
                bd=2,
                relief=SOLID,
                wraplength=150
            )
            self.titulo_filmes.append([self.label_titulo, numero])
            self.label_titulo.pack(fill="both", expand="yes")

    def mouse_wheel(self,event):
        if event.num == 5 or event.delta == -120:
            self.mouse += 1
        if event.num == 4 or event.delta == 120:
            self.mouse -= 1
        if self.mouse < 0:
            self.mouse = 0
        elif self.mouse > self.end_barra:
            self.mouse = self.end_barra
        self.barra.set(self.mouse)
        self.vervalor(self.mouse)

    def procurar_filme(self):
        opcao = self.combobox_filtro.get()
        texto = self.entry_pesquisa.get().strip()
        if texto == '':
            self.filmes = banco_filmes.ver_filmes(self.usuario)
        else:
            if opcao == 'TITULO':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto, self.usuario)
            if opcao == 'ANO':
                if not texto.isdigit():
                    mostrar_mensagem('Somente números podem digitados quando a coluna é ANO','erro')
                    return None
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto, self.usuario)
            if opcao == 'GENERO':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto, self.usuario)
            if opcao == 'NOTA':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto, self.usuario)
            if opcao == 'SINOPSE':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto, self.usuario)
        self.barra.set(0)
        self.atualiza_filmes(pesquise=False)

    def ordenar(self):
        self.atualiza_filmes(indice=self.id,tipo='abc')

    def pesquisar_filmes(self):
        self.frame.pack_forget()
        self.page_Pesquisar_Filme = Pesquisar_Filme(master=self.master, app=self)
        self.page_Pesquisar_Filme.tela_pesquisar_filme()

    def ir_tela_ver_filme(self,filme):
        if filme[0] == 'Filme Não Encontrado':
            mostrar_mensagem('Não foi encontrado um filme\nSe deseja visulizar um filme, você deve adicionar um filme','aviso')
        else:
            self.frame.pack_forget()
            self.page_READ_Filme = READ_Filme(master=self.master, app=self, filme=filme[1])
            self.page_READ_Filme.tela_read_filme()

    def recomendacao(self):
        self.frame.pack_forget()
        self.page_Recomendacao_Filme = Recomendacao_Filme(master=self.master, app=self)
        self.page_Recomendacao_Filme.tela_recomendacao_filme()

    def aleatorio(self):
        if len(self.filmes) == 0:
            mostrar_mensagem('Nenhum filme foi encontrado','aviso')
            return None
        self.frame.pack_forget()
        self.page_Aleatorio_Filme = Aleatorio_Filme(master=self.master, app=self)
        self.page_Aleatorio_Filme.tela_filme_aleatorio()

    def atualiza_filmes(self, indice=0, pesquise=True, tipo=''):
        self.photoFilme.clear()
        self.nomes_filmes.clear()
        if pesquise:
            if tipo == '':
                self.filmes = banco_filmes.ver_filmes(self.usuario)
            else:
                self.filmes = banco_filmes.ver_filmes_ordenados(self.usuario)
        label_nome_texto = f'{len(self.filmes):>04} Filmes' if len(self.filmes) != 1 else f'{len(self.filmes):>04} Filme'
        self.label_nome.config(text=label_nome_texto)
        self.end_barra = len(self.filmes) // 6 if len(self.filmes) % 6 != 0 or len(self.filmes) == 0 else len(self.filmes) // 6 - 1
        self.sliderlength = [dado[1] for dado in self.objeto if self.end_barra <= dado[0]][0]
        self.barra.config(to=self.end_barra, sliderlength=self.sliderlength)
        for numero in range(indice, indice+6):
            try:
                im = Image.open(rf'{self.filmes[numero].cam_imagem}')
                im.thumbnail((150, 150))
                self.photoFilme.append(ImageTk.PhotoImage(im))
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((150, 150))
                self.photoFilme.append(ImageTk.PhotoImage(im))
            try:
                self.nomes_filmes.append([self.filmes[numero].titulo,self.filmes[numero]])
            except:
                self.nomes_filmes.append(['Filme Não Encontrado',''])
        for numero in range(6):
            self.foto_filmes[numero][0].config(image=self.photoFilme[numero], command=lambda m=self.nomes_filmes[numero]: self.ir_tela_ver_filme(m))
            self.titulo_filmes[numero][0].config(text=self.nomes_filmes[numero][0])

    def vervalor(self,v):
        self.mouse = int(v)
        self.id = int(v)*6
        self.atualiza_filmes(self.id,False)

    def logoff(self):
        self.frame.pack_forget()
        self.page_Menu_Usuario = Menu_Usuario(master=self.master, app=self)
        self.page_Menu_Usuario.tela_menu_usuario()

    def tela_inicio(self):
        self.frame.pack()
        try:
            im = Image.open(self.usuario.foto)
            im.thumbnail((130, 130))
            self.photoImg5 = ImageTk.PhotoImage(im)
        except:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((130, 130))
            self.photoImg5 = ImageTk.PhotoImage(im)
        self.foto_usuario.config(image=self.photoImg5, height=130, width=130)
        self.label_nome_usuario.config(text=self.usuario.nome)

    def ir_tela_add_filmes(self):
        self.filmes = banco_filmes.ver_filmes(self.usuario)
        self.frame.pack_forget()
        self.page_ADD_Filme = ADD_Filme(master=self.master, app=self)
        self.page_ADD_Filme.tela_add_filmes()


class ADD_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.master.title('ADICIONAR FILME')
        tamanho_janela(self.master, 1000, 900)
        self.app = app
        self.pastas = self.app.pastas
        self.usuario = self.app.usuario
        self.lista = self.app.filmes
        self.frame = Frame(self.master, bg='#154f91')
        frame_imagem = Frame(self.frame, bg='#154f91')
        frame_imagem.pack(pady=30)
        self.caminho_filme = ''
        self.caminho_foto = ''
        self.photoImg = ''
        self.id_filme = f'{self.usuario.id}.-1.{len(self.lista)}'
        self.filmes = []
        self.lista_generos = []
        #slc = SELECIONAR
        self.botao_slc_imagem = Button(
            frame_imagem,
            text='SELECIONAR\nIMAGEM\nDO FILME',
            #bg='#334B49',
            #fg='white',
            height=5,
            width=15,
            font=('Arial', 18),
            border=5,
            relief=RIDGE,
            command=lambda: self.selecionar_arquivo((("Arquivos jfif", "*.jfif"), ("Arquivos jpg", "*.jpg"), ("Arquivos jpeg", "*.jpeg"), ("Arquivos png", "*.png")),'Escolha uma imagem'))
        self.botao_slc_imagem.pack()

        frame_sinopse = Frame(self.frame, bg='#154f91')
        frame_sinopse.pack(pady=15)

        label_sinopse = Label(
            frame_sinopse,
            text='SINOPSE',
            background='#154f91',
            anchor=W,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_sinopse.pack(side=TOP)

        self.entrada_sinopse = Text(
            frame_sinopse,
            #bg='#1e99be',
            #fg='white',
            wrap=WORD,
            width=60,
            height=3,
            font=('Arial', 12),
            bd=2,
            relief=GROOVE
        )
        self.entrada_sinopse.pack(fill=Y, expand="yes")

        frame_titulo = Frame(self.frame, bg='#154f91')
        frame_titulo.pack(pady=15)

        self.botao_slc_arquivo = Button(frame_titulo,
                                        text='SELECIONAR\nARQUIVO\nDO FILME',
                                        #bg='#334B49',
                                        #fg='white',
                                        height=4,
                                        width=38,
                                        border=5,
                                        relief=RIDGE,
                                        wraplength=470,
                                        font=('Arial', 18),
                                        command=lambda: self.selecionar_arquivo((("Arquivos avi", "*.avi"), ("Arquivos mp4", "*.mp4"), ("Arquivos mkv", "*.mkv"), ("Arquivos m4v", "*.m4v")),'Escolha um filme'))
        self.botao_slc_arquivo.pack()

        frame_genero = Frame(self.frame, bg='#154f91')
        frame_genero.pack(pady=15)

        label_genero = Label(
            frame_genero,
            text='GENÊRO',
            background='#154f91',
            anchor=W,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_genero.pack(side=TOP)

        frame_genero_check = Frame(frame_genero, bg='#154f91')
        frame_genero_check.pack()

        self.var_list = []
        check_list = []
        self.genero_list = ['Animação', 'Aventura', 'Ação', 'Cinema TV', 'Comédia', 'Crime', 'Documentário', 'Drama',
                       'Família', 'Fantasia', 'Faroeste', 'Ficção Científica', 'Guerra', 'História', 'Mistério',
                       'Música', 'Romance', 'Terror', 'Thriller']
        linha = -1
        for index, task in enumerate(self.genero_list):
            coluna = index % 5
            if coluna == 0:
                linha += 1
            self.var_list.append(IntVar(value=0))
            check = Checkbutton(frame_genero_check,
                variable=self.var_list[index],
                font=('Arial', 12),
                text=task,
                fg='white',
                bg='#154f91',
                selectcolor='#154f91',
                command=lambda a=index, b=task: self.pegar_genero(a, b),
                padx=10
            )
            check_list.append(check)
            check_list[index].grid(column=coluna, row=linha)

        frame_nota = Frame(self.frame, bg='#154f91')
        frame_nota.pack(pady=15)

        label_nota = Label(
            frame_nota,
            text='NOTA',
            background='#154f91',
            anchor=W,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_nota.pack(side=TOP)

        self.combobox_slc_nota = Combobox(frame_nota,
                                          state='readonly',
                                          values=['NÃO ASSISTIDO', 'PÉSSIMO', 'MUITO RUIM', 'MAIS OU MENOS', 'MUITO BOM','EXCELENTE'],
                                          font=('Arial', 18),
                                          justify=CENTER,
                                          width=40)
        self.combobox_slc_nota.current(0)
        self.combobox_slc_nota.pack(fill="both", expand="yes")

        frame_botoes = Frame(self.frame, bg='#154f91')
        frame_botoes.pack(pady=15)

        botao_tela_gerenciar = Button(frame_botoes,
                                      text='VOLTAR',
                                      bg='#154f91',
                                      fg='white',
                                      height=3,
                                      width=20,
                                      font=('Arial', 10),
                                      border=15,
                                      command=self.ir_tela_inicio)
        botao_tela_gerenciar.pack(padx=10, side=LEFT)
        botao_popular_informacao = Button(frame_botoes,
                                 text='PROCURAR\nINFORMAÇÕES',
                                 bg='#154f91',
                                 fg='white',
                                 height=3,
                                 width=20,
                                 font=('Arial', 10),
                                 border=15,
                                 command=self.procurar_informacao)
        botao_popular_informacao.pack(padx=10, side=LEFT)
        #add = ADICIONAR
        botao_add_filme = Button(frame_botoes,
                                 text='ADICIONAR',
                                 bg='#154f91',
                                 fg='white',
                                 height=3,
                                 width=20,
                                 font=('Arial', 10),
                                 border=15,
                                 command=self.adicionar_filmes)
        botao_add_filme.pack(padx=10, side=LEFT)
        botao_procurar_filmes = Button(frame_botoes,
                                       text='PROCURAR\nFILMES NA PASTA',
                                       bg='#154f91',
                                       fg='white',
                                       height=3,
                                       width=20,
                                       font=('Arial', 10),
                                       border=15,
                                       command=self.procurar_filmes)
        botao_procurar_filmes.pack(padx=10, side=LEFT)

    def monitor(self):
        if self.auxiliar.is_alive():
            # check the thread every 100ms
            self.master.after(500, lambda: self.monitor())
        else:
            self.lista_filmes_web = self.auxiliar.filmes_api

            if type(self.lista_filmes_web) == bool:
                mostrar_mensagem(
                    f'O filme: {arquivo[-1]}\nNão foi encontrado na base. Procure seu filme na tela de pesquisa')
            else:
                self.frame.pack_forget()
                self.page_Filmes_API = Filmes_API(master=self.master, app=self)
                self.page_Filmes_API.tela_auxiliar()
            return None

    def pegar_genero(self, indice, tarefa):
        valor = self.var_list[indice].get()
        if valor == 0:
            self.lista_generos.remove(tarefa)
        else:
            self.lista_generos.append(tarefa)
            self.lista_generos.sort()

    def limpar_informacoes(self):
        self.caminho_foto = ''
        self.botao_slc_imagem.config(
            image='',
            height=5,
            width=15,
            text='SELECIONAR\nIMAGEM\nDO FILME',
            font=('Arial', 18))
        self.combobox_slc_nota.current(0)
        for componente in self.var_list:
            if componente.get() == 1:
                componente.set(0)
        self.lista_generos.clear()
        self.entrada_sinopse.delete(1.0,END)
        self.botao_slc_arquivo.config(text='SELECIONAR\nARQUIVO\nDO FILME')

    def adicionar_filmes(self):
        self.imagens = verificar_arquivos(self.pastas.caminho_imagem)
        nota = self.combobox_slc_nota.get()
        if self.caminho_filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar um arquivo')
            return None
        genero = '/'.join(self.lista_generos)
        sinopse = self.entrada_sinopse.get('1.0',END)

        aux_filme = re.split(r"[/()]\s*", self.caminho_filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()

        if type(self.caminho_foto) == FilmeWEB:
            arquivos = ('png', 'jpg', 'jfif', 'jpeg')
            for ext in arquivos:
                caminho = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).{ext}'
                if caminho in self.imagens:
                    break
            else:
                caminho = fr'{self.pastas.caminho_imagem}/{self.caminho_foto.titulo} ({self.caminho_foto.ano}).png'
                self.caminho_foto.download_imagem(caminho)
            self.caminho_foto = caminho
        elif self.caminho_foto == '':
            self.botao_slc_imagem.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar uma imagem')
            return None

        auxiliar_filme = f'{titulo} ({ano})'
        auxiliar_imagem = self.caminho_foto.split('/')
        auxiliar_imagem = auxiliar_imagem[-1].split('.')
        auxiliar_imagem = '.'.join(auxiliar_imagem[:-1])
        if auxiliar_filme != auxiliar_imagem.strip():
            mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem estão com titulo ou ano diferentes\n'
                            f'Para prosseguir você tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem}',
                             'erro')
            return None

        filme = Filme(self.id_filme, titulo, ano, nota, genero, extensao, self.caminho_filme, self.caminho_foto,sinopse)

        try:
            banco_filmes.inserir_filme(filme, self.usuario)
        except Exception as mensagem:
            mostrar_mensagem(mensagem,'aviso')
            return None

        mostrar_mensagem('Filme adicionado com sucesso')
        self.limpar_informacoes()
        self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ver_filmes(self.usuario))}'

    def procurar_informacao(self):
        if self.caminho_filme == '':
            mostrar_mensagem('Para procurar e adicionar as informações de um filme, você deve selecionar um filme')
            return None
        aux_filme = re.split(r"[/()]\s*", self.caminho_filme)
        titulo = aux_filme[-3].strip()
        ano = aux_filme[-2]
        self.auxiliar = TMDB_Consulta(arquivo=f'{titulo} ({ano})', pesquisa_completa=True)
        self.auxiliar.daemon = True
        self.auxiliar.start()
        self.monitor()
        print(2)

    def selecionar_arquivo(self, tipo_arquivo, title):
        if title == 'Escolha uma imagem':
            inicio = self.pastas.caminho_imagem
        else:
            inicio = self.pastas.caminho_filme
        while True:
            caminho = filedialog.askopenfilename(filetypes=tipo_arquivo,
                title=title,
                initialdir=inicio)
            if caminho == '':
                resposta = perguntar("AVISO", "Deseja continuar?")
                if not resposta:
                    mostrar_mensagem('Tudo bem')
                    return self.caminho_filme
            else:
                break
        if title == 'Escolha uma imagem':
            try:
                tam_caminho_imagem = self.pastas.caminho_imagem
                if caminho[:len(tam_caminho_imagem)] != self.pastas.caminho_imagem:
                    mostrar_mensagem(f'Arquivo da imagem não está dentro da pasta = {self.pastas.caminho_imagem}',
                                     'erro')
                    return None
                self.caminho_foto = caminho
                im = Image.open(self.caminho_foto)
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
                self.botao_slc_imagem.configure(image=self.photoImg, height=150, width=150)
                self.botao_slc_imagem.update()
            except:
                self.caminho_foto = ''
                mostrar_mensagem('Arquivo de imagem corrompido ou inválido', 'erro')
        else:
            try:
                tam_caminho_filme = self.pastas.caminho_filme
                if caminho[:len(tam_caminho_filme)] != self.pastas.caminho_filme:
                    mostrar_mensagem(f'Arquivo do filme não está dentro da pasta = {self.pastas.caminho_filme}', 'erro')
                    return None
                self.caminho_filme = caminho
                arquivo = self.caminho_filme.split('/')
                self.botao_slc_arquivo.config(text=arquivo[-1])
            except:
                self.caminho_filme = ''
                mostrar_mensagem('Arquivo do filme corrompido ou inválido', 'erro')

    def tela_add_filmes(self, filme_web=False):
        self.frame.pack()
        if type(filme_web) != bool:
            if filme_web.imgURL != None:
                resposta = perguntar('ARQUIVO DE MENSAGEM','Deseja utilizar a imagem do filme mostrada na tela anterior?')
                if resposta:
                    self.caminho_foto = filme_web
                    filme_web.criar_imagem_tk(150,150)
                    self.botao_slc_imagem.config(image=filme_web.imgTk, height=150, width=150)

            if filme_web.genero != None:
                for componente in self.var_list:
                    if componente.get() == 1:
                        componente.set(0)

                genero = filme_web.genero.split('/')
                self.lista_generos = genero
                for i, g in enumerate(self.genero_list):
                    if g in genero:
                        self.var_list[i].set(1)

            if filme_web.sinopse != None:
                self.entrada_sinopse.delete(1.0, END)
                self.entrada_sinopse.insert('1.0', filme_web.sinopse)
            self.id_filme = f'{self.usuario.id}.{filme_web.id}'

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id)
        self.app.tela_inicio()

    def procurar_filmes(self):
        self.frame.pack_forget()
        tamanho_janela(self.master, 800, 150)
        frame = Frame(self.master, bg='#154f91')
        pb = Progressbar(
            frame,
            orient='horizontal',
            mode='determinate',
            length=650
        )
        pb.grid(column=0, row=0, columnspan=2, pady=20)
        value_label = Label(frame, text=f"Progresso: {pb['value']}%", bg='#154f91', fg='white', font=('Arial',20))
        value_label.grid(column=0, row=2, columnspan=2)
        frame.pack()
        self.filmes = verificar_arquivos(self.pastas.caminho_filme)
        self.imagens = verificar_arquivos(self.pastas.caminho_imagem)
        filmes_armazenados = banco_filmes.ver_filmes(self.usuario)
        for indice in range(len(self.filmes)):
            pb['value'] = int(((indice+1)*100)/len(self.filmes))
            value_label['text'] = f"Progresso: {pb['value']}%"
            self.master.update_idletasks()
            self.caminho_filme = self.filmes[indice]
            self.caminho_foto = ''
            aux_filme = re.split(r"[/()]\s*", self.caminho_filme)
            titulo = aux_filme[-3].strip()
            ano = int(aux_filme[-2])
            extensao = aux_filme[-1].strip()
            auxiliar_filme = f'{titulo} ({ano})'

            filme = Filme(
                id='',
                titulo=titulo,
                ano=ano,
                nota='',
                genero='',
                extensao='',
                cam_filme='',
                cam_imagem='',
                sinopse='')

            if filme in filmes_armazenados:
                continue

            lista_filmes_web = procurar_filme_api(f'{titulo} ({ano}).{extensao}',True)
            if type(lista_filmes_web) == bool:
                lista_filmes_web = procurar_filme_api(f'{titulo} ({ano}).{extensao}',False)
                if type(lista_filmes_web) == bool:
                    mostrar_mensagem(
                        f'O filme: {auxiliar_filme} - Não foi encontrado na base.\nProcure seu filme na tela de pesquisa')
                    tamanho_janela(self.master, 1000, 900)
                    frame.pack_forget()
                    self.frame.pack()
                    return None

            if len(lista_filmes_web) > 1:
                self.botao_slc_arquivo.config(text=self.filmes[indice])
                frame.pack_forget()
                mostrar_mensagem(f'Vamos adicionar agora o filme:\n{auxiliar_filme}')
                self.procurar_informacao()
                return None
            else:
                filme_web: FilmeWEB = lista_filmes_web[0]
                self.id_filme = f'{self.usuario.id}.{filme_web.id}'

            arquivos = ('png', 'jpg', 'jfif', 'jpeg')
            for ext in arquivos:
                existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).{ext}'
                if existe_arquivo in self.imagens:
                    self.caminho_foto = existe_arquivo
                    break
            else:
                existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).png'
                if not filme_web.download_imagem(existe_arquivo):
                    mostrar_mensagem(f'Não foi possível realizar o download da imagem do filme: {auxiliar_filme}\n'
                                    'Você vai ter que fazer o download manualmente','Problema com a imagem do filme')
                    self.botao_slc_arquivo.config(text=self.filmes[indice])

                    if filme_web.genero != None:
                        for componente in self.var_list:
                            if componente.get() == 1:
                                componente.set(0)

                        genero = filme_web.genero.split('/')
                        self.lista_generos = genero
                        for i, g in enumerate(self.genero_list):
                            if g in genero:
                                self.var_list[i].set(1)

                    if filme_web.sinopse != None:
                        self.entrada_sinopse.delete(1.0, END)
                        self.entrada_sinopse.insert('1.0', filme_web.sinopse)

                    tamanho_janela(self.master, 1000, 900)
                    frame.pack_forget()
                    self.frame.pack()
                    return None
                self.caminho_foto = existe_arquivo

            auxiliar_imagem = self.caminho_foto.split('/')
            auxiliar_imagem = auxiliar_imagem[-1].split('.')
            auxiliar_imagem = '.'.join(auxiliar_imagem[:-1])
            if auxiliar_filme != auxiliar_imagem.strip():
                mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem estão com titulo ou ano diferentes\n'
                                 f'Para prosseguir você tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem}',
                                 'erro')
                tamanho_janela(self.master, 1000, 900)
                frame.pack_forget()
                self.frame.pack()
                return None
            sinopse = not filme_web.tratar_sinopse()
            genero = not filme_web.tratar_genero()
            if sinopse or genero:
                vazio = 'não foi achado o gênero' if genero else 'não foi achado a sinopse' if sinopse else 'não foi achado o gênero e a sinopse'
                mostrar_mensagem(f'Você vai ter que adicionar manualmente, {vazio} do filme: {auxiliar_filme}', 'Problema com a imagem do filme')
                self.botao_slc_arquivo.config(text=self.filmes[indice])
                im = Image.open(self.caminho_foto)
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
                self.botao_slc_imagem.configure(image=self.photoImg, height=150, width=150)
                self.botao_slc_imagem.update()
                if not genero:
                    for componente in self.var_list:
                        if componente.get() == 1:
                            componente.set(0)

                    genero = filme_web.genero.split('/')
                    self.lista_generos = genero
                    for i, g in enumerate(self.genero_list):
                        if g in genero:
                            self.var_list[i].set(1)

                if not sinopse:
                    self.entrada_sinopse.delete(1.0, END)
                    self.entrada_sinopse.insert('1.0', filme_web.sinopse)

                tamanho_janela(self.master, 1000, 900)
                frame.pack_forget()
                self.frame.pack()
                return None

            filme = Filme(
                id=self.id_filme,
                titulo=titulo,
                ano=ano,
                nota='NÃO ASSISTIDO',
                genero=filme_web.genero,
                extensao=extensao,
                cam_filme=self.caminho_filme,
                cam_imagem=self.caminho_foto,
                sinopse=filme_web.sinopse)

            try:
                banco_filmes.inserir_filme(filme, self.usuario)
            except Exception as mensagem:
                mostrar_mensagem(mensagem, 'aviso')
                tamanho_janela(self.master, 1000, 900)
                frame.pack_forget()
                self.frame.pack()
                return None

            self.limpar_informacoes()
            self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ver_filmes(self.usuario))}'
        else:
            mostrar_mensagem('Todos os filmes foram adicionados','info')
            tamanho_janela(self.master, 1000, 900)
            frame.pack_forget()
            self.frame.pack()


class Filmes_API:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.titulo_anterior = self.master.title()
        self.master.title('INFORMAÇÕES')
        tamanho_janela(self.master, 1000, 900)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.lista_filmes_web = self.app.lista_filmes_web
        self.id = 0
        frame_imagem = Frame(self.frame)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(self.frame)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(self.frame, bg='#154f91', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)

        self.lista_filmes_web[self.id].criar_imagem_tk()

        self.imagem = Label(
            frame_imagem,
            image=self.lista_filmes_web[self.id].imgTk,
            bd=10,
            relief=RIDGE,
            background='#334B49'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text=self.lista_filmes_web[self.id].sinopse,
                             pady=20,
                             padx=20,
                             wraplength=600,
                             background='#1A857F',
                             fg='white',
                             font=('Arial', 11),
                             bd=2,
                             relief=SUNKEN,
                             height=10,
                             width=90
                             )
        self.sinopse.pack()

        self.titulo_informacao = Label(
            frame_informacao,
            text=self.lista_filmes_web[self.id].titulo,
            background='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text=self.lista_filmes_web[self.id].genero,
            background='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.genero_informacao.pack(
            side=BOTTOM
        )

        self.ano_informacao = Label(
            frame_informacao,
            text=self.lista_filmes_web[self.id].ano,
            background='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.ano_informacao.pack(
            side=TOP
        )

        voltar_botao = Button(
            frame_botao,
            text='VOLTAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_add_filmes
        ).pack(
            side=LEFT,
            padx=20
        )

        assistir_botao = Button(
            frame_botao,
            text='PRÓXIMO',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.proximo
        ).pack(
            side=LEFT,
            padx=20
        )

        gerar_botao = Button(
            frame_botao,
            text='ESCOLHER',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=lambda: self.ir_tela_add_filmes(filme_escolhido=self.lista_filmes_web[self.id])
        ).pack(
            side=LEFT,
            padx=20
        )

    def proximo(self):
        print(len(self.lista_filmes_web) , self.id)
        if len(self.lista_filmes_web) > self.id + 1:
            self.id += 1
        else:
            mostrar_mensagem('Todos os filmes achados foram vistos\nSe você não achou seu filme, recomendo revisar o titulo e o ano.','aviso')
            self.id = 0

        self.lista_filmes_web[self.id].criar_imagem_tk()
        self.imagem.configure(image=self.lista_filmes_web[self.id].imgTk)
        self.sinopse.config(text=self.lista_filmes_web[self.id].sinopse)
        self.titulo_informacao.config(text=self.lista_filmes_web[self.id].titulo)
        self.genero_informacao.config(text=self.lista_filmes_web[self.id].genero)
        self.ano_informacao.config(text=self.lista_filmes_web[self.id].ano)

    def tela_auxiliar(self):
        self.frame.pack()

    def ir_tela_add_filmes(self, filme_escolhido=False):
        self.master.title(self.titulo_anterior)
        tamanho_janela(self.master, 1000, 900)
        self.frame.pack_forget()
        if self.titulo_anterior == 'ALTERAR FILME':
            self.app.tela_update_filmes(filme_escolhido)
        else:
            self.app.tela_add_filmes(filme_escolhido)


class READ_Filme:
    def __init__(self, master=None, app=None, filme=Filme):
        self.master = master
        self.app = app
        self.master.title('CONSULTAR FILME')
        tamanho_janela(self.master, 1000, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.filme = filme
        self.id = 0
        frame_imagem = Frame(self.frame)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(self.frame)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(self.frame, bg='#1A857F', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        self.frame_botao = Frame(self.frame, bg='#154f91')
        self.frame_botao.pack(pady=20)
        largura = 600
        altura = 250
        if isfile(self.filme.cam_imagem):
            try:
                im = Image.open(self.filme.cam_imagem)
                im.thumbnail((largura, altura))
                self.img = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((largura, altura))
                self.img = ImageTk.PhotoImage(im)
        else:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((largura, altura))
            self.img = ImageTk.PhotoImage(im)

        self.imagem = Label(
            frame_imagem,
            image=self.img,
            bd=10,
            relief=RIDGE,
            background='#334B49'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text=self.filme.sinopse,
                             pady=20,
                             padx=20,
                             wraplength=600,
                             bg='#1A857F',
                             fg='white',
                             font=('Arial', 11),
                             bd=2,
                             relief=SUNKEN,
                             height=10,
                             width=90
                             )
        self.sinopse.pack()

        self.titulo_informacao = Label(
            frame_informacao,
            text=self.filme.titulo,
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text=self.filme.genero,
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.genero_informacao.pack(
            side=BOTTOM
        )

        frame_informacao_auxiliar = Frame(frame_informacao, bg='#1A857F')
        frame_informacao_auxiliar.pack(side=TOP)

        self.ano_informacao = Label(
            frame_informacao_auxiliar,
            text=self.filme.ano,
            bg='#1A857F',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.ano_informacao.pack(
            side=LEFT
        )

        self.nota_informacao = Label(
            frame_informacao_auxiliar,
            text=self.filme.nota,
            bg='#1A857F',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.nota_informacao.pack(
            side=RIGHT
        )

        voltar_botao = Button(
            self.frame_botao,
            text='VOLTAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_inicio
        ).pack(
            side=LEFT,
            padx=40
        )

        self.combobox_nota = Combobox(self.frame_botao,
                                          state='readonly',
                                          values=['ASSISTIR', 'ALTERAR', 'DELETAR'],
                                          font=('Arial', 16),
                                          justify=CENTER,
                                          width=20)
        self.combobox_nota.current(0)
        self.aux = self.combobox_nota.get()
        self.combobox_nota.pack(fill="both", expand="yes", side=LEFT)
        self.combobox_nota.bind('<<ComboboxSelected>>', self.crud_filme)

        self.botao_extra = Button(
            self.frame_botao,
            text='ASSISTIR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.assistir_filme
        )
        self.botao_extra.pack(
            side=LEFT,
            padx=40
        )

    def crud_filme(self, evento):
        opcao = self.combobox_nota.get()
        if opcao == 'ASSISTIR' and self.aux != opcao:
            self.aux = self.combobox_nota.get()
            self.botao_extra.destroy()
            self.botao_extra = Button(
                self.frame_botao,
                text='ASSISTIR',
                bg='#154f91',
                fg='white',
                height=3,
                width=30,
                font=('Arial', 10),
                border=15,
                command=self.assistir_filme
            )
            self.botao_extra.pack(
                side=LEFT,
                padx=40
            )
        if opcao == 'ALTERAR' and self.aux != opcao:
            self.aux = self.combobox_nota.get()
            self.botao_extra.destroy()
            self.botao_extra = Button(
                self.frame_botao,
                text='ALTERAR',
                bg='#154f91',
                fg='white',
                height=3,
                width=30,
                font=('Arial', 10),
                border=15,
                command=self.alterar_filme
            )
            self.botao_extra.pack(
                side=LEFT,
                padx=40
            )
        if opcao == 'DELETAR' and self.aux != opcao:
            self.aux = self.combobox_nota.get()
            self.botao_extra.destroy()
            self.botao_extra = Button(
                self.frame_botao,
                text='DELETAR',
                bg='#154f91',
                fg='white',
                height=3,
                width=30,
                font=('Arial', 10),
                border=15,
                command=self.deletar_filme
            )
            self.botao_extra.pack(
                side=LEFT,
                padx=40
            )

    def alterar_filme(self):
        self.frame.pack_forget()
        self.page_UPDATE_Filme = UPDATE_Filme(master=self.master, app=self)
        self.page_UPDATE_Filme.tela_update_filmes()

    def deletar_filme(self):
        resposta = perguntar('DELETAR FILME',f'Deseja mesmo deletar o filme {self.filme.titulo} do ano {self.filme.ano}?')
        if resposta:
            try:
                banco_filmes.deletar_filme(self.filme, self.app.usuario)
            except Exception as mensagem:
                mostrar_mensagem(mensagem, 'erro')
                return None
            self.ir_tela_inicio()
            mostrar_mensagem('Sem Problemas\nFeito!!!')
        else:
            mostrar_mensagem('Tudo bem')

    def assistir_filme(self):
        try:
            banco_filmes.somar_atributo_filme(self.filme, self.app.usuario)
        except Exception as mensagem:
            mostrar_mensagem(mensagem,'erro')
            return None
        try:
            startfile(self.filme.cam_filme)
        except:
            mostrar_mensagem(f'Ocorreu um erro ao tentar assistir o filme: {self.filme.titulo}\nVerifique se o caminho: {self.filme.cam_filme} está correto.', 'erro')
            return None
        self.master.destroy()
        exit()

    def tela_read_filme(self, novo_filme=None):
        if type(novo_filme) != type(None):
            if isfile(novo_filme.cam_imagem):
                try:
                    im = Image.open(novo_filme.cam_imagem)
                    im.thumbnail((550, 300))
                except:
                    im = 'Images/naoEncontrado.jpg'
                    im = Image.open(rf'{Path(im).absolute()}')
                    im.thumbnail((550, 300))
            else:
                im = 'Images/naoEncontrado.jpg'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((550, 300))
            self.img = ImageTk.PhotoImage(im)
            self.imagem.config(image=self.img)
            self.sinopse.config(text=novo_filme.sinopse)
            self.titulo_informacao.config(text=novo_filme.titulo)
            self.genero_informacao.config(text=novo_filme.genero)
            self.ano_informacao.config(text=novo_filme.ano)
            self.nota_informacao.config(text=novo_filme.nota)
            self.filme = novo_filme
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id)
        self.app.tela_inicio()


class UPDATE_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.master.title('ALTERAR FILME')
        tamanho_janela(self.master, 1000, 900)
        self.app = app
        self.pastas = self.app.app.pastas
        self.usuario = self.app.app.usuario
        self.filme = self.app.filme
        self.lista_generos = self.app.filme.genero.split('/')
        self.frame = Frame(self.master, bg='#154f91')
        frame_imagem = Frame(self.frame, bg='#154f91')
        frame_imagem.pack(pady=30)
        self.caminho_filme = self.filme.cam_filme
        self.caminho_foto = self.filme.cam_imagem
        if isfile(self.caminho_foto):
            try:
                im = Image.open(self.caminho_foto)
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
        else:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((150, 150))
            self.photoImg = ImageTk.PhotoImage(im)
        self.id_filme = self.filme.id
        self.filmes = []
        #slc = SELECIONAR
        self.botao_slc_imagem = Button(
            frame_imagem,
            image=self.photoImg,
            bg='#006266',
            height = 150,
            width = 150,
            border=5,
            relief=RIDGE,
            command=lambda: self.selecionar_arquivo((("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")),'Escolha uma imagem'))
        self.botao_slc_imagem.pack()

        frame_sinopse = Frame(self.frame, bg='#154f91')
        frame_sinopse.pack(pady=15)

        label_sinopse = Label(
            frame_sinopse,
            text='SINOPSE',
            background='#154f91',
            anchor=W,
            justify=LEFT,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_sinopse.pack(side=TOP)

        self.entrada_sinopse = Text(
            frame_sinopse,
            #bg='#1e99be',
            #fg='white',
            wrap=WORD,
            width=60,
            height=3,
            font=('Arial', 12),
            bd=2,
            relief=GROOVE
        )
        self.entrada_sinopse.pack(fill=Y, expand="yes")
        self.entrada_sinopse.insert('1.0', self.filme.sinopse.strip())

        frame_titulo = Frame(self.frame, bg='#154f91')
        frame_titulo.pack(pady=15)

        auxiliar = self.caminho_filme.split('/')

        self.botao_slc_arquivo = Button(frame_titulo,
                                        text=auxiliar[-1],
                                        bg='#006266',
                                        fg='white',
                                        height=4,
                                        width=38,
                                        border=5,
                                        relief=RIDGE,
                                        wraplength=470,
                                        font=('Arial', 18),
                                        command=lambda: self.selecionar_arquivo('','Escolha um filme'))
        self.botao_slc_arquivo.pack()

        frame_genero = Frame(self.frame, bg='#154f91')
        frame_genero.pack(pady=15)

        self.var_list = []
        check_list = []
        self.genero_list = ['Animação', 'Aventura', 'Ação', 'Cinema TV', 'Comédia', 'Crime', 'Documentário', 'Drama',
                            'Família', 'Fantasia', 'Faroeste', 'Ficção Científica', 'Guerra', 'História', 'Mistério',
                            'Música', 'Romance', 'Terror', 'Thriller']
        linha = -1
        for index, task in enumerate(self.genero_list):
            coluna = index % 5
            if coluna == 0:
                linha += 1
            self.var_list.append(IntVar(value=0))
            check = Checkbutton(frame_genero,
                                variable=self.var_list[index],
                                font=('Arial', 12),
                                text=task,
                                fg='white',
                                bg='#154f91',
                                selectcolor='#154f91',
                                command=lambda a=index, b=task: self.pegar_genero(a, b),
                                padx=10
                                )
            check_list.append(check)
            check_list[index].grid(column=coluna, row=linha)
        for i, g in enumerate(self.genero_list):
            if g in self.lista_generos:
                self.var_list[i].set(1)

        frame_nota = Frame(self.frame, bg='#154f91')
        frame_nota.pack(pady=15)

        label_nota = Label(
            frame_nota,
            text='NOTA',
            background='#154f91',
            anchor=W,
            justify=LEFT,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_nota.pack(side=TOP)
        notas = ['NÃO ASSISTIDO', 'PÉSSIMO', 'MUITO RUIM', 'MAIS OU MENOS', 'MUITO BOM','EXCELENTE']
        self.combobox_slc_nota = Combobox(frame_nota,
                                          state='readonly',
                                          values=notas,
                                          font=('Arial', 18),
                                          justify=CENTER,
                                          width=40)
        self.combobox_slc_nota.current(notas.index(self.filme.nota))
        self.combobox_slc_nota.pack(fill="both", expand="yes")

        frame_botoes = Frame(self.frame, bg='#154f91')
        frame_botoes.pack(pady=15)

        self.botao_tela_gerenciar = Button(frame_botoes,
                                      text='VOLTAR',
                                      bg='#154f91',
                                      fg='white',
                                      height=3,
                                      width=30,
                                      font=('Arial', 10),
                                      border=15,
                                      command=self.ir_tela_consultar)
        self.botao_tela_gerenciar.pack(padx=20, side=LEFT)
        self.botao_popular_informacao = Button(frame_botoes,
                                 text='PROCURAR\nINFORMAÇÕES',
                                 bg='#154f91',
                                 fg='white',
                                 height=3,
                                 width=30,
                                 font=('Arial', 10),
                                 border=15,
                                 command=self.procurar_informacao)
        self.botao_popular_informacao.pack(padx=20, side=LEFT)

        self.botao_add_filme = Button(frame_botoes,
                                 text='ALTERAR',
                                 bg='#154f91',
                                 fg='white',
                                 height=3,
                                 width=30,
                                 font=('Arial', 10),
                                 border=15,
                                 command=self.alterar_informacoes_filme)
        self.botao_add_filme.pack(padx=20, side=LEFT)

    def monitor(self):
        if self.auxiliar.is_alive():
            # check the thread every 100ms
            self.master.after(500, lambda: self.monitor())
        else:
            self.botao_slc_imagem['state'] = NORMAL
            self.botao_slc_arquivo['state'] = NORMAL
            self.botao_tela_gerenciar['state'] = NORMAL
            self.botao_popular_informacao['state'] = NORMAL
            self.botao_add_filme['state'] = NORMAL
            self.lista_filmes_web = self.auxiliar.filmes_api
            if type(self.lista_filmes_web) == bool:
                mostrar_mensagem(
                    f'O filme: {self.caminho_filme.split("/")[-1]}\nNão foi encontrado na base. Procure seu filme na tela de pesquisa')
            else:
                self.frame.pack_forget()
                self.page_Filmes_API = Filmes_API(master=self.master, app=self)
                self.page_Filmes_API.tela_auxiliar()
            return None

    def pegar_genero(self, indice, tarefa):
        valor = self.var_list[indice].get()
        if valor == 0:
            self.lista_generos.remove(tarefa)
        else:
            self.lista_generos.append(tarefa)
            self.lista_generos.sort()

    def limpar_informacoes(self):
        self.caminho_foto = ''
        self.botao_slc_imagem.config(
            image='',
            height=5,
            width=15,
            text='SELECIONAR\nIMAGEM\nDO FILME',
            font=('Arial', 18))
        self.combobox_slc_nota.current(0)
        for componente in self.var_list:
            if componente.get() == 1:
                componente.set(0)
        self.lista_generos.clear()
        self.entrada_sinopse.delete(1.0,END)
        self.botao_slc_arquivo.config(text='SELECIONAR\nARQUIVO\nDO FILME')

    def alterar_informacoes_filme(self):
        self.imagens = verificar_arquivos(self.pastas.caminho_imagem)
        nota = self.combobox_slc_nota.get()
        if self.caminho_filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para alterar o filme, você deve selecionar um arquivo')
            return None
        genero = '/'.join(self.lista_generos)
        sinopse = self.entrada_sinopse.get('1.0', END)

        aux_filme = re.split(r"[/()]\s*", self.caminho_filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()

        if type(self.caminho_foto) == FilmeWEB:
            arquivos = ('png', 'jpg', 'jfif', 'jpeg')
            for ext in arquivos:
                caminho = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).{ext}'
                if caminho in self.imagens:
                    break
            else:
                caminho = fr'{self.pastas.caminho_imagem}/{self.caminho_foto.titulo} ({self.caminho_foto.ano}).png'
                self.caminho_foto.download_imagem(caminho)
            self.caminho_foto = caminho
        elif self.caminho_foto == '':
            self.botao_slc_imagem.focus_set()
            mostrar_mensagem('Para alterar o filme, você deve selecionar uma imagem')
            return None

        auxiliar_filme = f'{titulo} ({ano})'
        auxiliar_imagem = self.caminho_foto.split('/')
        auxiliar_imagem = auxiliar_imagem[-1].split('.')
        auxiliar_imagem = '.'.join(auxiliar_imagem[:-1])
        if auxiliar_filme != auxiliar_imagem.strip():
            mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem estão com titulo ou ano diferentes\n'
                             f'Para prosseguir você tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem}',
                             'erro')
            return None

        filme = Filme(self.id_filme, titulo, ano, nota, genero, extensao, self.caminho_filme, self.caminho_foto,
                      sinopse)

        try:
            banco_filmes.alterar_filme(filme, self.usuario)
        except Exception as mensagem:
            mostrar_mensagem(mensagem, 'aviso')
            return None

        mostrar_mensagem('Filme alterado com sucesso')
        self.limpar_informacoes()
        self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ver_filmes(self.usuario))}'

    def procurar_informacao(self):
        if self.caminho_filme == '':
            mostrar_mensagem('Para procurar e adicionar as informações de um filme, você deve selecionar um filme')
            return ''
        aux_filme = re.split(r"[/()]\s*", self.caminho_filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        self.auxiliar = TMDB_Consulta(arquivo=f'{titulo} ({ano})')
        self.auxiliar.daemon = True
        self.botao_slc_imagem['state'] = DISABLED
        self.botao_slc_arquivo['state'] = DISABLED
        self.botao_tela_gerenciar['state'] = DISABLED
        self.botao_popular_informacao['state'] = DISABLED
        self.botao_add_filme['state'] = DISABLED
        self.auxiliar.start()
        self.monitor()

    def selecionar_arquivo(self, tipo_arquivo, title):
        if title == 'Escolha uma imagem':
            inicio = self.pastas.caminho_imagem
        else:
            inicio = self.pastas.caminho_filme
        while True:
            caminho = filedialog.askopenfilename(
                title=title,
                initialdir=inicio)
            if caminho == '':
                resposta = perguntar("AVISO", "Deseja continuar")
                if not resposta:
                    mostrar_mensagem('Tudo bem')
                    return self.caminho_filme
            else:
                break
        if title == 'Escolha uma imagem':
            try:
                tam_caminho_imagem = self.pastas[2].caminho_imagem
                if caminho[:len(tam_caminho_imagem)] != self.pastas[2].caminho_imagem:
                    mostrar_mensagem(f'Arquivo da imagem não está dentro da pasta = {self.pastas[2].caminho_imagem}',
                                     'erro')
                    return ''
                self.caminho_foto = caminho
                im = Image.open(self.caminho_foto)
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
                self.botao_slc_imagem.configure(image=self.photoImg, height=150, width=150)
                self.botao_slc_imagem.update()
            except:
                self.caminho_foto = ''
                mostrar_mensagem('Arquivo de imagem corrompido ou inválido', 'erro')
        else:
            try:
                tam_caminho_filme = self.pastas.caminho_filme
                if caminho[:len(tam_caminho_filme)] != self.pastas.caminho_filme:
                    mostrar_mensagem(f'Arquivo do filme não está dentro da pasta = {self.pastas.caminho_filme}', 'erro')
                    return ''
                self.caminho_filme = caminho
                arquivo = self.caminho_filme.split('/')
                self.botao_slc_arquivo.config(text=arquivo[-1])
            except:
                self.caminho_filme = ''
                mostrar_mensagem('Arquivo do filme corrompido ou inválido', 'erro')

    def tela_update_filmes(self, filme_web=False):
        self.frame.pack()
        if type(filme_web) != bool:
            if filme_web.imgURL != None:
                resposta = perguntar('ARQUIVO DE MENSAGEM',
                                     'Deseja utilizar a imagem do filme mostrada na tela anterior?')
                if resposta:
                    self.caminho_foto = filme_web
                    filme_web.criar_imagem_tk(150, 150)
                    self.botao_slc_imagem.config(image=filme_web.imgTk, height=150, width=150)

            if filme_web.genero != None:
                for componente in self.var_list:
                    if componente.get() == 1:
                        componente.set(0)

                genero = filme_web.genero.split('/')
                self.lista_generos = genero
                for i, g in enumerate(self.genero_list):
                    if g in genero:
                        self.var_list[i].set(1)

            if filme_web.sinopse != None:
                self.entrada_sinopse.delete(1.0, END)
                self.entrada_sinopse.insert('1.0', filme_web.sinopse)
            self.id_filme = f'{self.usuario.id}.{filme_web.id}'

    def ir_tela_consultar(self,auxiliar=None):
        self.master.title('CONSULTAR FILME')
        tamanho_janela(self.master, 1000, 850)
        self.frame.pack_forget()
        self.app.app.atualiza_filmes(self.app.app.id)
        self.app.tela_read_filme(novo_filme=auxiliar)


class Aleatorio_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.master.title('FILME ALEATÓRIO')
        tamanho_janela(self.master, 1000, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.filmes = self.app.filmes
        self.salvar_numeros = []
        self.id_filme = self.gerar_numero_aleatorio()
        self.filme = self.filmes[self.id_filme]
        self.id = 0
        frame_imagem = Frame(self.frame)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(self.frame)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(self.frame, bg='#1A857F', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        self.frame_botao = Frame(self.frame, bg='#154f91')
        self.frame_botao.pack(pady=20)
        if isfile(self.filme.cam_imagem):
            try:
                im = Image.open(self.filme.cam_imagem)
                im.thumbnail((550, 250))
                self.img = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((550, 250))
                self.img = ImageTk.PhotoImage(im)
        else:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((550, 250))
            self.img = ImageTk.PhotoImage(im)

        self.imagem = Label(
            frame_imagem,
            image=self.img,
            bd=10,
            relief=RIDGE,
            background='#334B49'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text=self.filme.sinopse,
                             pady=20,
                             padx=20,
                             wraplength=600,
                             bg='#1A857F',
                             fg='white',
                             font=('Arial', 11),
                             bd=2,
                             relief=SUNKEN,
                             height=10,
                             width=90
                             )
        self.sinopse.pack()

        self.titulo_informacao = Label(
            frame_informacao,
            text=self.filme.titulo,
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text=self.filme.genero,
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.genero_informacao.pack(
            side=BOTTOM
        )

        frame_informacao_auxiliar = Frame(frame_informacao, bg='#1A857F')
        frame_informacao_auxiliar.pack(side=TOP)

        self.ano_informacao = Label(
            frame_informacao_auxiliar,
            text=self.filme.ano,
            bg='#1A857F',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.ano_informacao.pack(
            side=LEFT
        )

        self.nota_informacao = Label(
            frame_informacao_auxiliar,
            text=self.filme.nota,
            bg='#1A857F',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.nota_informacao.pack(
            side=RIGHT
        )

        voltar_botao = Button(
            self.frame_botao,
            text='VOLTAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_inicio
        ).pack(
            side=LEFT,
            padx=40
        )

        voltar_botao = Button(
            self.frame_botao,
            text='GERAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.gerar_filme
        ).pack(
            side=LEFT
        )

        self.botao_extra = Button(
            self.frame_botao,
            text='ASSISTIR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.assistir_filme
        )
        self.botao_extra.pack(
            side=LEFT,
            padx=40
        )

    def gerar_numero_aleatorio(self):
        while True:
            numero = randint(0, len(self.filmes)-1)
            if numero in self.salvar_numeros:
                if len(self.salvar_numeros) == len(self.filmes):
                    self.salvar_numeros.clear()
                    mostrar_mensagem('Todos os filmes foram vistos, agora voltaremos para o primeiro filme','aviso')
                    self.salvar_numeros.append(0)
                    return 0
                else:
                    continue
            else:
                self.salvar_numeros.append(numero)
                return numero

    def gerar_filme(self):
        self.id_filme = self.gerar_numero_aleatorio()
        self.filme = self.filmes[self.id_filme]

        if isfile(self.filme.cam_imagem):
            try:
                im = Image.open(self.filme.cam_imagem)
                im.thumbnail((550, 250))
                self.img = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((550, 250))
                self.img = ImageTk.PhotoImage(im)
        else:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((550, 250))
            self.img = ImageTk.PhotoImage(im)

        self.imagem.config(image=self.img)
        self.sinopse.config(text=self.filme.sinopse)
        self.titulo_informacao.config(text=self.filme.titulo)
        self.genero_informacao.config(text=self.filme.genero)
        self.ano_informacao.config(text=self.filme.ano)
        self.nota_informacao.config(text=self.filme.nota)

    def assistir_filme(self):
        try:
            banco_filmes.somar_atributo_filme(self.filme, self.app.usuario)
        except Exception as mensagem:
            mostrar_mensagem(mensagem,'erro')
            return None
        try:
            startfile(self.filme.cam_filme)
        except:
            mostrar_mensagem(f'Ocorreu um erro ao tentar assistir o filme: {self.filme.titulo}\nVerifique se o caminho: {self.filme.cam_filme} está correto.', 'erro')
            return None
        self.master.destroy()
        exit()

    def tela_filme_aleatorio(self):
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id,pesquise=False)
        self.app.tela_inicio()


class Recomendacao_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.master.title('RECOMENDAÇÃO DE FILMES')
        tamanho_janela(self.master, 1000, 900)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.lista_filmes = []
        self.id = 0

        frame_filme = Frame(self.frame, bg='#154f91')
        frame_filme.pack()

        frame_imagem = Frame(frame_filme)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(frame_filme)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(frame_filme, bg='#1A857F', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        self.frame_botao = Frame(frame_filme, bg='#154f91')
        self.frame_botao.pack(pady=20)
        im = 'Images/naoEncontrado.png'
        im = Image.open(rf'{Path(im).absolute()}')
        im.thumbnail((550, 300))
        self.img = ImageTk.PhotoImage(im)

        self.imagem = Label(
            frame_imagem,
            image=self.img,
            bd=10,
            relief=RIDGE,
            background='#334B49'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text="",
                             pady=20,
                             padx=20,
                             wraplength=600,
                             bg='#1A857F',
                             fg='white',
                             font=('Arial', 11),
                             bd=2,
                             relief=SUNKEN,
                             height=10,
                             width=90
                             )
        self.sinopse.pack()

        self.titulo_informacao = Label(
            frame_informacao,
            text="",
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text="",
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.genero_informacao.pack(
            side=BOTTOM
        )

        self.ano_informacao = Label(
            frame_informacao,
            text="",
            bg='#1A857F',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.ano_informacao.pack(
            side=BOTTOM
        )

        self.voltar_botao = Button(
            self.frame_botao,
            text='VOLTAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_inicio
        )
        self.voltar_botao.pack(
            side=LEFT,
            padx=20
        )

        self.gerar_botao = Button(
            self.frame_botao,
            text='GERAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.filmes_recomendados
        )
        self.gerar_botao.pack(
            side=LEFT,
            padx=20
        )

        self.proximo_botao = Button(
            self.frame_botao,
            text='PRÓXIMO',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.proximo_filme
        )
        self.proximo_botao.pack(
            side=LEFT,
            padx=20
        )

    def monitor(self):
        if self.auxiliar.is_alive():
            # check the thread every 100ms
            self.master.after(500, lambda: self.monitor())
        else:
            self.gerar_botao['state'] = NORMAL
            self.voltar_botao['state'] = NORMAL
            self.proximo_botao['state'] = NORMAL
            self.lista_filmes = self.auxiliar.filmes_api
            if type(self.lista_filmes) == bool:
                mostrar_mensagem('Nenhum filme foi encontrado', 'alerta')
                return None
            else:
                mostrar_mensagem(f'Posso te recomendar {len(self.lista_filmes)} filmes!')
            self.alterar_eventos()

    def filmes_recomendados(self):
        filme_indicado = banco_filmes.achar_filme_recomendado(self.app.usuario)
        id_indicado = [id[2:] for id in filme_indicado if '.-1.' not in id]
        if len(id_indicado) == 0:
            mostrar_mensagem('Não foi possível recomendar filmes para você','erro')
            return None
        self.id = 0
        self.auxiliar = TMDB_Recomenda(id=id_indicado[0])
        self.auxiliar.daemon = True
        self.auxiliar.start()
        self.gerar_botao['state'] = DISABLED
        self.voltar_botao['state'] = DISABLED
        self.proximo_botao['state'] = DISABLED
        self.monitor()

    def alterar_eventos(self):
        filme: FilmeWEB = self.lista_filmes[self.id]
        filme.criar_imagem_tk()
        self.imagem.config(image=filme.imgTk)
        self.sinopse.config(text=filme.sinopse)
        self.titulo_informacao.config(text=filme.titulo)
        self.genero_informacao.config(text=filme.genero)
        self.ano_informacao.config(text=filme.ano)

    def proximo_filme(self):
        if self.lista_filmes == []:
            mostrar_mensagem('Nenhum filme foi encontrado','erro')
            return None
        if self.id+1 < len(self.lista_filmes):
            self.id += 1
        else:
            mostrar_mensagem('A lista de recomendações acabou.\nVou voltar para o primeiro filme', 'info')
            self.id = 0
        self.alterar_eventos()

    def tela_recomendacao_filme(self):
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id,pesquise=False)
        self.app.tela_inicio()


class Pesquisar_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.master.title('PESQUISAR FILME')
        tamanho_janela(self.master, 1000, 980)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.lista_filmes = []
        self.id = 0

        frame_pesquisa = Frame(self.frame, bg='#154f91')
        frame_pesquisa.pack(pady=10)
        frame_pesquisa_auxiliar1 = Frame(frame_pesquisa, bg='#154f91')
        frame_pesquisa_auxiliar1.pack(side=LEFT, padx=20)
        label_titulo = Label(
            frame_pesquisa_auxiliar1,
            text='TITULO',
            bg='#154f91',
            fg='white',
            anchor=W,
            justify=LEFT,
            width=40,
            font=('Arial', 12)
        )
        label_titulo.pack(side=TOP)
        self.entry_titulo = Entry(
            frame_pesquisa_auxiliar1,
            width=20,
            font=('Arial', 20),
            border=2,
            relief=GROOVE
        )
        self.entry_titulo.pack(fill="both", expand="yes")
        frame_pesquisa_auxiliar2 = Frame(frame_pesquisa, bg='#154f91')
        frame_pesquisa_auxiliar2.pack(side=LEFT,padx=10)
        label_ano = Label(
            frame_pesquisa_auxiliar2,
            text='ANO',
            bg='#154f91',
            fg='white',
            anchor=W,
            justify=LEFT,
            width=12,
            font=('Arial', 12)
        )
        label_ano.pack(side=TOP)
        self.entry_ano = Entry(
            frame_pesquisa_auxiliar2,
            width=6,
            font=('Arial', 20),
            border=2,
            relief=GROOVE
        )
        self.entry_ano.pack(fill="both", expand="yes")
        im = Image.open(r'Images/lupa.png')
        im.thumbnail((50, 50))
        self.pesquisar = ImageTk.PhotoImage(im)
        self.bt_pesquisar = Button(frame_pesquisa, image=self.pesquisar, bg='#154f91', command=self.pesquisar_filme)
        self.bt_pesquisar.pack(side=LEFT, fill="both", expand="yes", padx=20)

        frame_filme = Frame(self.frame, bg='#154f91')
        frame_filme.pack()

        frame_imagem = Frame(frame_filme)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(frame_filme)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(frame_filme, bg='#1A857F', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        self.frame_botao = Frame(frame_filme, bg='#154f91')
        self.frame_botao.pack(pady=20)
        im = 'Images/naoEncontrado.png'
        im = Image.open(rf'{Path(im).absolute()}')
        im.thumbnail((550, 300))
        self.img = ImageTk.PhotoImage(im)

        self.imagem = Label(
            frame_imagem,
            image=self.img,
            bd=10,
            relief=RIDGE,
            background='#334B49'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text="",
                             pady=20,
                             padx=20,
                             wraplength=600,
                             bg='#1A857F',
                             fg='white',
                             font=('Arial', 11),
                             bd=2,
                             relief=SUNKEN,
                             height=10,
                             width=90
                             )
        self.sinopse.pack()

        self.titulo_informacao = Label(
            frame_informacao,
            text="",
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text="",
            bg='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.genero_informacao.pack(
            side=BOTTOM
        )

        self.ano_informacao = Label(
            frame_informacao,
            text="",
            bg='#1A857F',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.ano_informacao.pack(
            side=BOTTOM
        )

        self.voltar_botao = Button(
            self.frame_botao,
            text='VOLTAR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_inicio
        )
        self.voltar_botao.pack(
            side=LEFT,
            padx=80
        )

        self.proximo_botao = Button(
            self.frame_botao,
            text='PRÓXIMO',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.proximo_filme
        )
        self.proximo_botao.pack(
            side=LEFT,
            padx=80
        )

    def monitor(self):
        if self.auxiliar.is_alive():
            # check the thread every 100ms
            self.master.after(500, lambda: self.monitor())
        else:
            self.bt_pesquisar['state'] = NORMAL
            self.voltar_botao['state'] = NORMAL
            self.proximo_botao['state'] = NORMAL
            self.lista_filmes = self.auxiliar.filmes_api
            if type(self.lista_filmes) == bool:
                mostrar_mensagem('Nenhum filme foi encontrado', 'alerta')
                return None
            else:
                mostrar_mensagem(f'Foram encontrados {len(self.lista_filmes)} de acordo com a seua pesquisa')
            self.alterar_eventos()

    def pesquisar_filme(self):
        self.id = 0
        ano = self.entry_ano.get()
        titulo = self.entry_titulo.get()
        if titulo == '':
            mostrar_mensagem('O campo titulo deve ser preenchido','alerta')
            return None

        if ano == '':
            self.auxiliar = TMDB_Consulta(arquivo=f'{titulo} ({ano})', pesquisa_completa=False)
        else:
            try:
                ano = int(ano)
            except:
                mostrar_mensagem('O campo ano deve ser preenchido apenas com números', 'alerta')
                return None

            self.auxiliar = TMDB_Consulta(arquivo=f'{titulo} ({ano})')
        self.auxiliar.daemon = True
        self.auxiliar.start()
        self.bt_pesquisar['state'] = DISABLED
        self.voltar_botao['state'] = DISABLED
        self.proximo_botao['state'] = DISABLED
        self.monitor()

    def alterar_eventos(self):
        filme: FilmeWEB = self.lista_filmes[self.id]
        filme.criar_imagem_tk()
        self.imagem.config(image=filme.imgTk)
        self.sinopse.config(text=filme.sinopse)
        self.titulo_informacao.config(text=filme.titulo)
        self.genero_informacao.config(text=filme.genero)
        self.ano_informacao.config(text=filme.ano)

    def proximo_filme(self):
        if self.lista_filmes == []:
            mostrar_mensagem('Nenhum filme foi encontrado','erro')
            return None
        if self.id+1 < len(self.lista_filmes):
            self.id += 1
        else:
            self.id = 0
        self.alterar_eventos()

    def tela_pesquisar_filme(self):
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id,pesquise=False)
        self.app.tela_inicio()


class Menu_Usuario:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.pasta_usuario = self.app.pastas
        self.usuario = self.app.usuario
        self.caminhos = [self.usuario.foto, self.pasta_usuario.caminho_imagem, self.pasta_usuario.caminho_filme]
        self.master.title('MENU DO USUÁRIO')
        tamanho_janela(self.master, 1130, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        frame_foto = Frame(self.frame, bg='#154f91')
        frame_foto.pack(side=LEFT, fill="both", expand="yes",padx=10)

        im = Image.open(r'Images/movies.png')
        im.thumbnail((100, 100))
        self.photoImg = ImageTk.PhotoImage(im)

        self.voltar = Button(
            frame_foto,
            image=self.photoImg,
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=100,
            width=100,
            command=self.ir_tela_inicio
        )
        self.voltar.pack(anchor=NW,fill="both", expand="yes")

        label_voltar = Label(
            frame_foto,
            text='FILMES',
            fg='white',
            font=('Arial', 16),
            bg = '#1A857F',
            width=10,
            bd=2,
            relief=SOLID,
            wraplength=110
        )
        label_voltar.pack(fill="both", expand="yes")

        self.botoes = []

        dicionario_botao = {
            0: ['FICAR ON-LINE',self.logoff],
            1: ['LOGOFF', self.logoff],
            2: ['ENTRAR NO CHAT', self.ir_tela_chat],
            3: ['ALTERAR\nUSUÁRIO', self.alterar_pasta_usuario],
            4: ['DELETAR\nUSUÁRIO', self.logoff]
        }

        for id in range(5):
            botao = Button(frame_foto, text=dicionario_botao[id][0], bg='#154f91', fg='white',
                       font=('Arial', 10), border=15, relief=RAISED, command=dicionario_botao[id][1])
            self.botoes.append(botao)
            botao.pack(pady=30, anchor=S, fill="both", expand="yes")

        frame_informacoes = Frame(self.frame, bg='#154f91')
        frame_informacoes.pack(side=LEFT, fill="both", expand="yes", padx=200, pady=30)

        try:
            im = Image.open(self.usuario.foto)
            im.thumbnail((200, 200))
            self.photoImg2 = ImageTk.PhotoImage(im)
        except:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((200, 200))
            self.photoImg2 = ImageTk.PhotoImage(im)

        self.foto_usuario = Button(
            frame_informacoes,
            image=self.photoImg2,
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=200,
            width=200,
            command=self.selecionar_arquivo
        )
        self.foto_usuario.pack()

        frame_informacoes_2 = Frame(frame_informacoes, bg='#154f91')
        frame_informacoes_2.pack(pady=30)

        label_nome = Label(
            frame_informacoes_2,
            text="NOME:",
            fg='white',
            font=('Arial', 16),
            bg = '#154f91',
            width=40,
            anchor=NW
        )
        label_nome.pack()

        self.entry_nome = Entry(
            frame_informacoes_2,
            font=('Arial', 16),
            width=40,
            bd=2,
            relief=GROOVE
        )
        self.entry_nome.pack(side=BOTTOM)
        self.entry_nome.insert(0, self.usuario.nome)

        frame_informacoes_3 = Frame(frame_informacoes, bg='#154f91')
        frame_informacoes_3.pack(pady=30)

        label_email = Label(
            frame_informacoes_3,
            text="EMAIL:",
            fg='white',
            font=('Arial', 16),
            bg='#154f91',
            width=40,
            anchor=NW
        )
        label_email.pack()

        self.entry_email = Entry(
            frame_informacoes_3,
            font=('Arial', 16),
            width=40,
            bd=2,
            relief=GROOVE
        )
        self.entry_email.pack(side=BOTTOM)
        self.entry_email.insert(0, self.usuario.email)

        frame_informacoes_4 = Frame(frame_informacoes, bg='#154f91')
        frame_informacoes_4.pack(pady=30)

        label_senha = Label(
            frame_informacoes_4,
            text="SENHA:",
            fg='white',
            font=('Arial', 16),
            bg='#154f91',
            width=40,
            anchor=NW
        )
        label_senha.pack()

        self.entry_senha = Entry(
            frame_informacoes_4,
            font=('Arial', 16),
            width=40,
            bd=2,
            relief=GROOVE,
            show='*'
        )
        self.entry_senha.pack(side=BOTTOM)
        self.entry_senha.insert(0, self.usuario.senha)

        frame_informacoes_5 = Frame(frame_informacoes, bg='#154f91')
        frame_informacoes_5.pack(pady=30)

        self.btn_imagem = Button(
            frame_informacoes_5,
            text=f'Diretório de imagens:\n{self.pasta_usuario.caminho_imagem}',
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=50,
            width=30,
            fg='white',
            font=('Arial', 10),
            command=lambda x='Novo diretório de imagens': self.escolher_diretorio(x)
        )
        self.btn_imagem.pack(side=LEFT, padx=10)

        self.btn_filme = Button(
            frame_informacoes_5,
            text=f'Diretório de filmes:\n{self.pasta_usuario.caminho_filme}',
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=50,
            width=30,
            fg='white',
            font=('Arial', 10),
            command=lambda x='Novo diretório de filmes': self.escolher_diretorio(x)
        )
        self.btn_filme.pack(side=LEFT, padx=10)

    def logoff(self):
        resposta = perguntar('AVISO','Você tem certeza que deseja fazer logoff?')
        if resposta:
            self.master.title('LOGIN')
            tamanho_janela(self.master, 700, 300)
            self.frame.pack_forget()
            self.app.app.tela_login()

    def tela_menu_usuario(self):
        self.frame.pack()

    def ir_tela_chat(self):
        self.frame.pack_forget()
        self.page_Chat = Chat(master=self.master, app=self)
        self.page_Chat.tela_chat()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id,pesquise=True)
        self.app.usuario = self.usuario
        self.app.pastas = self.pasta_usuario
        self.app.tela_inicio()

    def escolher_diretorio(self, title):
        diretorio = filedialog.askdirectory(
            title=title,
            initialdir='/'
        )

        if diretorio == '':
            mostrar_mensagem(f'Operação cancelada', 'Diretório')
        else:
            mostrar_mensagem(f'Pasta = {diretorio}', 'Diretório Alterado')
            if title == 'Novo diretório de imagens':
                self.btn_imagem.config(text=f'Diretório de imagens:\n{diretorio}')
                self.caminhos[1] = diretorio
            else:
                self.btn_filme.config(text=f'Diretório de filmes:\n{diretorio}')
                self.caminhos[2] = diretorio
        return None

    def selecionar_arquivo(self):
        while True:
            caminho = filedialog.askopenfilename(
                filetypes=(("Arquivos jpg", "*.jpg"), ("Arquivos jpeg", "*.jpeg"), ("Arquivos jfif", "*.jfif"), ("Arquivos png", "*.png")),
                title='Selecione uma nova imagem',
                initialdir='/')
            if caminho == '':
                resposta = perguntar("AVISO", "Deseja continuar")
                if not resposta:
                    mostrar_mensagem('Tudo bem')
                    return None
            else:
                break
        try:
            self.caminhos[0] = caminho
            im = Image.open(caminho)
            im.thumbnail((200, 200))
            self.photoImg5 = ImageTk.PhotoImage(im)
            self.foto_usuario.configure(image=self.photoImg5, height=200, width=200)
            self.foto_usuario.update()
        except:
            self.caminhos[0] = self.usuario.foto
            mostrar_mensagem('Arquivo de imagem corrompido ou inválido', 'erro')

    def alterar_pasta_usuario(self):
        foto = self.caminhos[0]
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        alterar_usuario = self.usuario.foto != foto or self.usuario.nome != nome or self.usuario.email != email or self.usuario.senha != senha
        if senha != self.usuario.senha:
            resposta = perguntar('TROCAR A SENHA?','Você tem certeza sobre a alteração da senha?')
            if not resposta:
                self.entry_senha.delete(0, END)
                self.entry_senha.insert(0, self.usuario.senha)
                senha = self.usuario.senha
        dir_imagem = self.caminhos[1]
        dir_filme = self.caminhos[2]
        alterar_pasta = dir_imagem != self.pasta_usuario.caminho_imagem or dir_filme != self.pasta_usuario.caminho_filme
        if dir_filme != self.pasta_usuario.caminho_filme:
            resposta = perguntar('TROCAR DIRETÓRIO', 'Você deseja alterar o diretório dos filmes?\nAviso que essa alteração irá deletar todos os filmes do banco')
            if not resposta:
                mostrar_mensagem('Nenhuma alteração foi feita','info')
                return None

        if not (alterar_usuario or alterar_pasta):
            mostrar_mensagem('Nenhuma alteração foi identificada', 'erro')
            return None

        if alterar_pasta:
            if dir_filme != self.pasta_usuario.caminho_filme:
                banco_filmes.deletar_todos_filmes(self.usuario)
            else:
                pass
            try:
                banco_pastas.alterar_pastas(Pasta(self.pasta_usuario.id, self.usuario.id, dir_filme, dir_imagem, self.pasta_usuario.caminho_banco), self.usuario)
            except Exception as mensagem:
                mostrar_mensagem(mensagem,'erro')
                return None
            try:
                self.pasta_usuario = banco_pastas.ler_pastas_usuario(self.usuario)
            except Exception as msg:
                mostrar_mensagem(msg, 'erro')
                return None
            verifica_caminho_filmes(self.pasta_usuario)
            verifica_caminho_imagens(self.pasta_usuario)

        if alterar_usuario:
            try:
                banco_usuarios.alterar_dados(self.usuario, Usuario(0, nome, email, senha, foto))
            except Exception as mensagem:
                mostrar_mensagem(mensagem,'erro2')
                return None
            try:
                self.usuario = banco_usuarios.ler_dados_usuario(Usuario(0, nome, email, senha, foto))
            except Exception as msg:
                mostrar_mensagem(msg,'erro')
                return None
        mostrar_mensagem('Todas as alterações requisitadas foram realizadas','info')
        return None


class Chat:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.id_chat = None
        self.dentro_chat = True
        self.usuario = self.app.usuario
        self.criar_usuario()
        self.mensagens_chat = []
        self.master.title('CHAT')
        tamanho_janela(self.master, 600, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        frame_auxiliar = Frame(self.frame, width=600, height=850)
        frame_auxiliar.pack()
        self.labelHead = Label(frame_auxiliar,
                               bg="#1A857F",
                               fg="#EAECEE",
                               text=f'NICKNAME: {self.usuario.nome}',
                               font=('Arial', 13),
                               pady=5)
        self.labelHead.place(relwidth=1,relheight=0.075)
        self.line = Label(frame_auxiliar,
                          width=450,
                          bg="#154f91")
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
        self.textCons = Text(frame_auxiliar,
                             width=20,
                             height=2,
                             bg="#334B49",
                             fg="#EAECEE",
                             font=('Arial', 14),
                             padx=5,
                             pady=5)
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
        self.labelBottom = Label(frame_auxiliar,
                                 bg="#154f91",
                                 height=80)
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
        self.entryMsg = Entry(self.labelBottom,
                              font=('Arial', 14))

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
                                text="Enviar",
                                bg='#154f91',
                                fg='white',
                                font=('Arial', 10),
                                border=10,
                                relief=RAISED,
                                width=20,
                                command=lambda: self.enviar_mensagem(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

        self.btn_voltar = Button(
            frame_auxiliar,
            text=f'Voltar',
            border=10,
            height=5,
            width=15,
            fg='white',
            bg='#154f91',
            font=('Arial', 10),
            relief=RAISED,
            command=self.ir_tela_menu_usuario)
        self.btn_voltar.place(relx=0.01,
                             rely=0.93,
                             relheight=0.06,
                             relwidth=0.98)

        """
        self.btn_criar = Button(
            self.frame,
            text=f'Mensagem',
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=5,
            width=15,
            fg='white',
            font=('Arial', 10),
            command=self.ver_mensagem
        )
        self.btn_criar.pack()
        """

    def monitor_receber_mensagens(self):
        if self.thread.is_alive():
            self.master.after(1000, lambda: self.monitor_receber_mensagens())
        else:
            if len(self.mensagens_chat) != len(self.thread.mensagens):
                self.mensagens_chat = self.thread.mensagens
                self.carregar_mensagens()
            if self.dentro_chat:
                data = re.split(r"[ :.]\s*", str(datetime.datetime.now() - datetime.timedelta(seconds=5)))
                hora = f'{data[-4]}:{data[-3]}:{data[-2]}'
                self.thread = API_SM(user=self.usuario, funcao='receber_mensagens', hora=hora)
                self.thread.start()
                self.monitor_receber_mensagens()

    def monitor_criar_usuario(self):
        if self.thread.is_alive():
            self.master.after(500, lambda: self.monitor_criar_usuario())
        else:
            self.id_chat = self.thread.id
            data = re.split(r"[ :.]\s*", str(datetime.datetime.now()))
            hora = f'{data[-4]}:{data[-3]}:{data[-2]}'
            self.thread = API_SM(user=self.usuario, funcao='receber_mensagens', hora=hora)
            self.thread.start()
            self.monitor_receber_mensagens()

    def criar_usuario(self):
        self.thread = API_SM(user=self.usuario, funcao='verificar_usuario')
        self.thread.start()
        self.monitor_criar_usuario()

    def tela_chat(self):
        self.frame.pack()

    def carregar_mensagens(self):
        for mensagem in self.mensagens_chat:
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, mensagem)
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)
            self.entryMsg.delete(0, END)

    def monitor_enviar_mensagem(self):
        if self.thread2.is_alive():
            self.master.after(500, lambda: self.monitor_enviar_mensagem())
        else:
            self.btn_voltar.config(state=NORMAL)
            self.buttonMsg.config(state=NORMAL)

    def enviar_mensagem(self, msg):
        data = re.split(r"[ :.]\s*", str(datetime.datetime.now()))
        hora = f'{data[-4]}:{data[-3]}:{data[-2]}'

        self.thread2 = API_SM(user=self.usuario, funcao='enviar_mensagem', mensagem=msg, hora=hora)
        self.thread2.start()
        self.entryMsg.delete(0, END)
        self.btn_voltar.config(state=DISABLED)
        self.buttonMsg.config(state=DISABLED)
        self.monitor_enviar_mensagem()

    def ir_tela_menu_usuario(self):
        self.dentro_chat = False
        self.frame.pack_forget()
        self.master.title('MENU DO USUÁRIO')
        tamanho_janela(self.master, 1130, 850)
        self.app.tela_menu_usuario()

if __name__ == '__main__':
    app = SM(root)
    root.mainloop()