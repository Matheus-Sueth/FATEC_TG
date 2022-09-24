from tkinter import *
from tkinter.ttk import Combobox, Progressbar
from PIL import ImageTk
from PIL import Image
from BACK_END.ControleDeTela import *
from BACK_END.Usuario import Usuario
from BACK_END.PastasDAO import PastaDAO
from BACK_END.Pastas import Pasta
from BACK_END.Filme import Filme
from BACK_END.Colecao import Colecao
from BACK_END.RecomendaFilme import *
import urllib.request
import io
import re
from pathlib import Path
from os.path import isfile
from os import startfile
from random import randint

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

class WebImage:
    def __init__(self, url, largura=600, altura=400):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        image.thumbnail((largura, altura))
        self.__image = ImageTk.PhotoImage(image)

    @property
    def image(self):
        return self.__image

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
            command=self.testes
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
            command=self.testes
        ).pack(pady=10)

    def testes(self):
        print('funciona')

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
            usuario_login = Usuario(0,'Usuario',email,senha,'Images/foto.png')
            resultado = banco_usuarios.ler_dados_usuario(usuario_login)
            if type(resultado) != Usuario:
                if resultado == False:
                    mostrar_mensagem('E-mail ou senha com valores fora das diretrizes do sistema', 'aviso')
                if resultado == None:
                    mostrar_mensagem('Usuário não encontrado', 'aviso')
                return ''
            if usuario_login != resultado:
                mostrar_mensagem('Usuário encontrado, mas a senha está incorreta', 'aviso')
                return ''

            self.usuario = resultado
            self.indice = resultado.id
            pasta_usuario = banco_pastas.ler_pastas_usuario(self.usuario)
            if type(pasta_usuario) != Pasta:
                mostrar_mensagem(f'Nenhuma pasta foi encontrada para o usuário {usuario.nome}. Então nós iremos procurar os diretórios de imagem e de filme', 'aviso')
                self.pasta_usuario = Pasta(0,self.usuario.id,'','',banco_usuarios.banco)
                self.pasta_usuario.caminho_filme, self.pasta_usuario.validar_caminho_imagem = criar_pastas()
                banco_pastas.inserir_dados(self.pasta_usuario)
            else:
                self.pasta_usuario = pasta_usuario
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
            command=lambda: self.selecionar_arquivo((("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")),'Escolha sua foto de perfil'))
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

    def selecionar_arquivo(self, tipo_arquivo, title):
        while True:
            caminho = filedialog.askopenfilename(
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
        elif self.entrada_nome.get() == '':
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
            result = banco_usuarios.inserir_dados(self.novo_usuario)
            if result == None:
                mostrar_mensagem('Os dados não condizem com as diretrizes do sistema, por favor verifique se elas estão corretas')
                return None
            elif not result:
                mostrar_mensagem('Já existe esse email no sistema, a criação de usuário foi cancelada\nPara continuar troque o email')
                return None
            else:
                mostrar_mensagem('Usuário Criado\nAgora vamos para a tela de login', 'info')
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
        self.pastas = self.app.pasta_usuario
        self.usuario = self.app.usuario
        self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1130, 850)
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

        im = Image.open(self.usuario.foto)
        im.thumbnail((140, 100))
        self.photoImg = ImageTk.PhotoImage(im)

        self.foto_usuario = Button(
            frame_foto,
            image=self.photoImg,
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=100,
            width=100,
            command=self.logoff
        )
        self.foto_usuario.pack(anchor=NW,fill="both", expand="yes")

        label_nome = Label(
            frame_foto,
            text=self.usuario.nome.title(),
            fg='white',
            font=('Arial', 16),
            bg = '#1A857F',
            width=10,
            bd=2,
            relief=SOLID,
            wraplength=110
        )
        label_nome.pack(fill="both", expand="yes")

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
            self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        else:
            if opcao == 'TITULO':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(),texto)
            if opcao == 'ANO':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto)
            if opcao == 'GENERO':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto)
            if opcao == 'NOTA':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto)
            if opcao == 'SINOPSE':
                self.filmes = banco_filmes.procurar_filmes(opcao.lower(), texto)
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
        print('Gerar recomendação de filme')

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
                self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
            else:
                self.filmes = banco_filmes.ler_dados_ordenados(usuario_id=self.usuario.id)
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
        self.page_Consultar_Usuario = Consultar_Usuario(master=self.master, app=self)
        self.page_Consultar_Usuario.tela_consultar_usuario()

    def tela_inicio(self):
        self.frame.pack()

    def ir_tela_add_filmes(self):
        self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        self.frame.pack_forget()
        self.page_ADD_Filme = ADD_Filme(master=self.master, app=self)
        self.page_ADD_Filme.tela_add_filmes()

class ADD_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.master.title('ADICIONAR FILME')
        tamanho_janela(self.master, 950, 820)
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
        #slc = SELECIONAR
        self.botao_slc_imagem = Button(
            frame_imagem,
            text='SELECIONAR\nIMAGEM\nDO FILME',
            bg='#334B49',
            fg='white',
            height=5,
            width=15,
            font=('Arial', 18),
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

        frame_titulo = Frame(self.frame, bg='#154f91')
        frame_titulo.pack(pady=15)

        self.botao_slc_arquivo = Button(frame_titulo,
                                        text='SELECIONAR\nARQUIVO\nDO FILME',
                                        bg='#334B49',
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

        label_genero = Label(
            frame_genero,
            text='GENÊRO',
            background='#154f91',
            anchor=W,
            justify=LEFT,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_genero.pack(side=TOP)

        self.entrada_genero = Entry(
            frame_genero,
            #bg='#1e99be',
            #fg='white',
            width=45,
            font=('Arial', 16),
            border=2,
            relief=GROOVE
        )
        self.entrada_genero.pack(fill="both", expand="yes")

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

    def limpar_informacoes(self):
        self.caminho_foto = ''
        self.botao_slc_imagem.config(
            image='',
            height=5,
            width=15,
            text='SELECIONAR\nIMAGEM\nDO FILME',
            font=('Arial', 18))
        self.combobox_slc_nota.current(0)
        self.entrada_genero.delete(0,END)
        self.entrada_sinopse.delete(1.0,END)
        self.botao_slc_arquivo.config(text='SELECIONAR\nARQUIVO\nDO FILME')

    def adicionar_filmes(self):
        if self.caminho_foto == '':
            self.botao_slc_imagem.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar uma imagem')
            return ''
        nota = self.combobox_slc_nota.get()
        if self.caminho_filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar um arquivo')
            return ''
        if self.entrada_genero.get() == '':
            self.entrada_genero.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve adicionar texto ao campo genêro')
            return ''
        sinopse = self.entrada_sinopse.get('1.0','end')
        if sinopse == '':
            self.entrada_sinopse.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve adicionar texto ao campo sinopse')
            return ''

        arquivo = self.caminho_filme.split('/')
        lista = informacoes3(arquivo[-1])
        for dados in lista:
            if titulo == dados[0]:
                id = dados[5]
                break
        else:
            id = self.id_filme

        aux_filme = re.split(r"[/()]\s*", self.caminho_filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)

        aux = Filme(id, titulo, ano, nota, self.entrada_genero.get(), extensao, self.caminho_filme , self.caminho_foto, self.entrada_sinopse.get('1.0','end'))

        for valor in valores:
            if valor == aux:
                mostrar_mensagem(f'{titulo} JÁ ESTÁ CADASTRADO','aviso')
                return ''

        arquivos = ['png', 'jpg', 'jfif', 'jpeg']
        arquivo_encontrado = False
        for ext in arquivos:
            existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).{ext}'
            if isfile(existe_arquivo):
                arquivo_encontrado = True
                break
        else:
            existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).png'

        if arquivo_encontrado and 'http://image.tmdb.org/' in imagem:
                self.photoImg = WebImage(imagem, 350, 150).get()
                self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                resposta = perguntar("AVISO", f"Já existe essa imagem({existe_arquivo})\nDeseja substituir a imagem?")
                if not resposta:
                    imagem = existe_arquivo
                    aux = Image.open(existe_arquivo)
                    aux.thumbnail((150, 150))
                    self.photoImg = ImageTk.PhotoImage(aux)
                    self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                    resposta2 = perguntar("AVISO", f"Deseja utilizar a imagem existente no caminho ({existe_arquivo})?")
                    if not resposta2:
                        mostrar_mensagem('Então o filme não será adicionado','aviso')
                        return ''
                else:
                    with open(existe_arquivo, 'wb') as imagem:
                        respost = requests.get(self.caminho_foto, stream=True)

                        if not respost.ok:
                            mostrar_mensagem('Desculpe, mas não é possível fazer o download da imagem\nPeço para entrar em contato com o desenvolvedor e não realizar download de imagem até o problema ser corrigido','erro')
                            return ''
                        else:
                            for dado in respost.iter_content(1024):
                                if not dado:
                                    break

                                imagem.write(dado)

                            mostrar_mensagem('Imagem salva com sucesso')
                    imagem = existe_arquivo
        elif 'http://image.tmdb.org/' in imagem:
            with open(existe_arquivo, 'wb') as imagem:
                respost = requests.get(self.caminho_foto, stream=True)

                if not respost.ok:
                    mostrar_mensagem('Desculpe, mas não é possível fazer o download da imagem\nPeço para entrar em contato com o desenvolvedor e não realizar download de imagem até o problema ser corrigido','erro')
                    return ''
                else:
                    for dado in respost.iter_content(1024):
                        if not dado:
                            break

                        imagem.write(dado)

                    mostrar_mensagem('Imagem salva com sucesso')
            imagem = existe_arquivo
        else:
            auxiliar_filme = f'{titulo} ({ano})'
            auxiliar_imagem = re.split(r"[/.]\s*", imagem)
            if auxiliar_filme != auxiliar_imagem[-2]:
                mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem estão com titulo ou ano diferentes\n \
                                 Para prosseguir você tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem[-2]}','erro')
                return ''



        if '/' in genero:
            genero = genero.title()

        aux = Filme(
            id=f'{self.usuario.id}.{id}',
            titulo=titulo,
            ano=ano,
            nota=nota,
            genero=genero.strip(),
            extensao=extensao,
            cam_filme=filme,
            cam_imagem=imagem,
            sinopse=sinopse.replace("'",'"'))
        banco_filmes.inserir_dados(self.usuario.id, aux)
        mostrar_mensagem('Filme adicionado com sucesso')
        self.limpar_informacoes()
        self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ler_dados(usuario_id=self.usuario.id))}'

    def procurar_informacao(self):
        filme = self.caminho_filme
        if filme == '':
            mostrar_mensagem('Para procurar e adicionar as informações de um filme, você deve selecionar um filme')
            return None
        arquivo = self.caminho_filme.split('/')
        lista = procurar_filme_api(arquivo[-1],True)
        if not lista:
            mostrar_mensagem(f'O filme: {arquivo[-1]}\nNão foi encontrado na base. Procure seu filme na tela de pesquisa')
        else:
            self.frame.pack_forget()
            self.page_ADD_Auxiliar = ADD_Auxiliar(master=self.master, app=self, lista=lista)
            self.page_ADD_Auxiliar.tela_auxiliar()
        return None

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
                tam_caminho_imagem = self.pastas.caminho_imagem
                if caminho[:len(tam_caminho_imagem)] != self.pastas.caminho_imagem:
                    mostrar_mensagem(f'Arquivo da imagem não está dentro da pasta = {self.pastas.caminho_imagem}',
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

    def tela_add_filmes(self, filme=''):
        self.frame.pack()
        if filme != '':
            if filme == 'Filme não Encontrado':
                mostrar_mensagem('Nenhum filme foi encontrado, recomendo revisar o titulo e o ano.','aviso')
                filme = ''
            if not filme[4] in 'None':
                resposta = perguntar('ARQUIVO DE MENSAGEM','Deseja utilizar a imagem do filme mostrada na tela anterior?')
                if resposta:
                    self.caminho_foto = filme[4]
                    self.photoImg = WebImage(filme[4], 350, 150).get()
                    self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                else:
                    mostrar_mensagem('Sem problemas')
            self.entrada_genero.delete(0, "end")
            self.entrada_sinopse.delete(1.0, END)
            self.entrada_genero.insert(0, filme[1].strip())
            self.entrada_sinopse.insert('1.0', filme[3].strip())
            self.id_filme = filme[5]

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
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        for indice in range(len(self.filmes)):
            pb['value'] = int(((indice+1)*100)/len(self.filmes))
            value_label['text'] = f"Progresso: {pb['value']}%"
            self.master.update_idletasks()
            self.caminho_filme = self.filmes[indice]
            self.caminho_foto = ''
            #self.botao_slc_arquivo.config(text=filme)
            aux_filme = re.split(r"[/()]\s*", self.filmes[indice])
            titulo = aux_filme[-3].strip()
            ano = int(aux_filme[-2])
            extensao = aux_filme[-1].strip()
            auxliar_filme = Filme('', titulo, ano, '', '', extensao, self.filmes[indice], '', '')
            if auxliar_filme in valores:
                continue
            arquivo = self.caminho_filme.split('/')
            lista = procurar_filme_api(arquivo[-1], True)
            if not lista:
                lista = procurar_filme_api(arquivo[-1], False)
                if not lista:
                    mostrar_mensagem(
                        f'O filme: {auxliar_filme}\nNão foi encontrado na base. Procure seu filme na tela de pesquisa')
                    tamanho_janela(self.master, 950, 820)
                    frame.pack_forget()
                    self.frame.pack()
                    return None
                elif len(lista) > 1:
                    self.botao_slc_arquivo.config(text=self.filmes[indice])
                    frame.pack_forget()
                    self.page_ADD_Auxiliar = ADD_Auxiliar(master=self.master, app=self, lista=lista)
                    self.page_ADD_Auxiliar.tela_auxiliar()
                    mostrar_mensagem(f'Vamos adicionar agora o filme:\n{auxliar_filme}')
                    return None
            elif len(lista) > 1:
                self.botao_slc_arquivo.config(text=self.filmes[indice])
                frame.pack_forget()
                self.page_ADD_Auxiliar = ADD_Auxiliar(master=self.master, app=self, lista=lista)
                self.page_ADD_Auxiliar.tela_auxiliar()
                mostrar_mensagem(f'Vamos adicionar agora o filme:\n{auxliar_filme}')
                return None

            filme_api = lista[0]

            if filme_api.verificar_null():


            if filme_api.ano != ano:
                mostrar_mensagem(f'O filme: {auxliar_filme} está com o ano errado no arquivo.\nAltere para {filme_api.titulo} ({filme_api.ano}){extensao}')
                tamanho_janela(self.master, 950, 820)
                frame.pack_forget()
                self.frame.pack()
                return None

            arquivos = ('png', 'jpg', 'jfif', 'jpeg')
            for ext in arquivos:
                existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).{ext}'
                if existe_arquivo in self.imagens:
                    self.caminho_foto = existe_arquivo
                    break
            else:
                existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).png'
                if filme_api.imgURL == None:
                    mostrar_mensagem(f'Não foi possível realizar o download do filme: {self.filmes[indice]}\n'
                                    'Você vai ter que fazer o download do filme manualmente, completando os campos em branco','Problema com a imagem do filme')
                    self.caminho_foto = ''
                    self.botao_slc_imagem.config(
                        image='',
                        height=5,
                        width=15,
                        text='SELECIONAR\nIMAGEM\nDO FILME',
                        font=('Arial', 18))
                    self.combobox_slc_nota.current(0)
                    self.entrada_genero.delete(0, END)
                    self.entrada_sinopse.delete(1.0, END)
                    self.botao_slc_arquivo.config(text='SELECIONAR\nARQUIVO\nDO FILME')

                if not filme_api.download_imagem(existe_arquivo):
                    mostrar_mensagem(
                        f'Desculpe houve uma falha no download da imagem do filme: {self.filmes[indice]}\nPeço para entrar em contato com o desenvolvedor e não realizar download de imagem até o problema ser corrigido',
                        'erro')
                    tamanho_janela(self.master, 950, 820)
                    frame.pack_forget()
                    self.frame.pack()
                    return None
                self.caminho_foto = existe_arquivo
            auxliar_filme = Filme(
                id=f'{self.usuario.id}.{filme_api.id}',
                titulo=titulo,
                ano=ano,
                nota='NÃO ASSISTIDO',
                genero=filme_api.genero,
                extensao=extensao,
                cam_filme=self.caminho_filme,
                cam_imagem=self.caminho_foto,
                sinopse=filme_api.sinopse)
            banco_filmes.inserir_dados(self.usuario.id, auxliar_filme)
            self.limpar_informacoes()
            self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ler_dados(usuario_id=self.usuario.id))}'
            self.botao_slc_arquivo.config(text=self.caminho_filme)
        else:
            mostrar_mensagem('Todos os filmes foram adicionados','info')
            tamanho_janela(self.master, 950, 820)
            frame.pack_forget()
            self.frame.pack()

class ADD_Auxiliar:
    def __init__(self, master=None, app=None, lista=[]):
        print(lista)
        self.master = master
        self.app = app
        self.master.title('INFORMAÇÕES')
        tamanho_janela(self.master, 1000, 900)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.lista = lista
        self.id = 0
        frame_imagem = Frame(self.frame)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(self.frame)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(self.frame, bg='#154f91', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)

        #self.filmes = verificar_arquivos(r'D:\Filmes')
        #self.id = 0

        if self.lista[self.id][4] != 'None':
            self.img = WebImage(self.lista[self.id][4], largura=550, altura=300).get()
        else:
            im = 'Images/naoEncontrado.jpg'
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
                             text=self.lista[self.id][3],
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
            text=self.lista[self.id][0],
            background='#1A857F',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text=self.lista[self.id][1],
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
            text=self.lista[self.id][2][:4],
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
        print()
        gerar_botao = Button(
            frame_botao,
            text='ESCOLHER',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=lambda: self.ir_tela_add_filmes(filme_escolhido=self.lista[self.id])
        ).pack(
            side=LEFT,
            padx=20
        )

    def somar_id(self, novo_id):
        self.id = self.id + novo_id

    def zerar_id(self):
        self.id = 0

    def proximo(self):
        if len(self.lista) > self.id + 1:
            self.somar_id(1)
        else:
            mostrar_mensagem('Todos os filmes achados foram vistos\nSe você não achou seu filme, recomendo revisar o titulo e o ano.','aviso')
            self.zerar_id()

        if self.lista[self.id][4] != 'None':
            self.img = WebImage(self.lista[self.id][4], largura=550, altura=300).get()
            self.imagem.config(image=self.img)
        else:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((550, 300))
            self.img = ImageTk.PhotoImage(im)
            self.imagem.configure(image=self.img)
        self.sinopse.config(text=self.lista[self.id][3])
        self.titulo_informacao.config(text=self.lista[self.id][0])
        self.genero_informacao.config(text=self.lista[self.id][1])
        self.ano_informacao.config(text=self.lista[self.id][2][:4])

    def tela_auxiliar(self):
        self.frame.pack()

    def ir_tela_add_filmes(self, filme_escolhido=''):
        self.master.title('ADICIONAR FILME')
        tamanho_janela(self.master, 950, 820)
        self.frame.pack_forget()
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
        self.page_6 = UPDATE_Filme(master=self.master, app=self)
        self.page_6.tela_add_filmes()

    def deletar_filme(self):
        resposta = perguntar('DELETAR FILME',f'Deseja mesmo deletar o filme {self.filme.titulo} do ano {self.filme.ano}?')
        if resposta:
            banco_filmes.deletar_dados(self.filme.id)
            self.ir_tela_inicio()
            mostrar_mensagem('Sem Problemas\nFeito!!!')
        else:
            mostrar_mensagem('Tudo bem')

    def assistir_filme(self):
        self.filme.aumentar_assistido()
        banco_filmes.alterar_like_dados(valor=self.filme.assistido, id=self.filme.id)
        startfile(self.filme.cam_filme)
        self.master.destroy()
        exit()

    def tela_read_filme(self, novo_filme=None):
        if type(novo_filme) != type(None):
            if isfile(novo_filme.cam_imagem):
                try:
                    im = Image.open(novo_filme.cam_imagem)
                    im.thumbnail((550, 300))
                    self.img = ImageTk.PhotoImage(im)
                except:
                    im = 'Images/naoEncontrado.jpg'
                    im = Image.open(rf'{Path(im).absolute()}')
                    im.thumbnail((550, 300))
                    self.img = ImageTk.PhotoImage(im)
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
        tamanho_janela(self.master, 950, 820)
        self.app = app
        self.pastas = self.app.app.pastas
        self.usuario = self.app.app.usuario
        self.filme = self.app.filme
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

        label_genero = Label(
            frame_genero,
            text='GENÊRO',
            background='#154f91',
            anchor=W,
            justify=LEFT,
            width=60,
            fg='white',
            font=('Arial', 12))
        label_genero.pack(side=TOP)

        self.entrada_genero = Entry(
            frame_genero,
            #bg='#1e99be',
            #fg='white',
            width=45,
            font=('Arial', 16),
            border=2,
            relief=GROOVE
        )
        self.entrada_genero.pack(fill="both", expand="yes")
        self.entrada_genero.insert(0, self.filme.genero)

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

        botao_tela_gerenciar = Button(frame_botoes,
                                      text='VOLTAR',
                                      bg='#154f91',
                                      fg='white',
                                      height=3,
                                      width=30,
                                      font=('Arial', 10),
                                      border=15,
                                      command=self.ir_tela_consultar)
        botao_tela_gerenciar.pack(padx=20, side=LEFT)
        botao_popular_informacao = Button(frame_botoes,
                                 text='PROCURAR\nINFORMAÇÕES',
                                 bg='#154f91',
                                 fg='white',
                                 height=3,
                                 width=30,
                                 font=('Arial', 10),
                                 border=15,
                                 command=self.procurar_informacao)
        botao_popular_informacao.pack(padx=20, side=LEFT)
        #add = ADICIONAR
        botao_add_filme = Button(frame_botoes,
                                 text='ALTERAR',
                                 bg='#154f91',
                                 fg='white',
                                 height=3,
                                 width=30,
                                 font=('Arial', 10),
                                 border=15,
                                 command=self.alterar_informacoes_filme)
        botao_add_filme.pack(padx=20, side=LEFT)

    def limpar_informacoes(self):
        self.caminho_foto = ''
        self.botao_slc_imagem.config(
            image='',
            height=5,
            width=15,
            text='SELECIONAR\nIMAGEM\nDO FILME',
            font=('Arial', 18))
        self.combobox_slc_nota.current(0)
        self.entrada_genero.delete(0,END)
        self.entrada_sinopse.delete(1.0,END)
        self.botao_slc_arquivo.config(text='SELECIONAR\nARQUIVO\nDO FILME')

    def alterar_informacoes_filme(self):
        imagem = self.caminho_foto
        if imagem == '':
            self.botao_slc_imagem.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar uma imagem')
            return ''
        nota = self.combobox_slc_nota.get()
        filme = self.caminho_filme
        if filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar um arquivo')
            return ''
        genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in
                         self.entrada_genero.get())
        if 'Ficção/Científica' in genero:
            genero = genero.replace('Ficção/Científica', 'Ficção Científica')
        if 'Cinema/TV' in genero:
            genero = genero.replace('Cinema/TV', 'Cinema TV')
        if genero == '':
            self.entrada_genero.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve adicionar texto ao campo genêro')
            return ''
        sinopse = self.entrada_sinopse.get('1.0', 'end').strip()
        if sinopse == '':
            self.entrada_sinopse.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve adicionar texto ao campo sinopse')
            return ''

        aux_filme = re.split(r"[/()]\s*", filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)

        arquivos = ['png', 'jpg', 'jfif', 'jpeg']
        arquivo_encontrado = False
        for ext in arquivos:
            existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).{ext}'
            if isfile(existe_arquivo):
                arquivo_encontrado = True
                break
        else:
            existe_arquivo = fr'{self.pastas.caminho_imagem}/{titulo} ({ano}).png'

        if arquivo_encontrado and 'http://image.tmdb.org/' in imagem:
            self.photoImg = WebImage(imagem, 350, 150).get()
            self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
            resposta = perguntar("AVISO", f"Já existe essa imagem({existe_arquivo})\nDeseja substituir a imagem?")
            if not resposta:
                imagem = existe_arquivo
                aux = Image.open(existe_arquivo)
                aux.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(aux)
                self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                resposta2 = perguntar("AVISO", f"Deseja utilizar a imagem existente no caminho ({existe_arquivo})?")
                if not resposta2:
                    mostrar_mensagem('Então o filme não será adicionado', 'aviso')
                    return ''
            else:
                with open(existe_arquivo, 'wb') as imagem:
                    respost = requests.get(self.caminho_foto, stream=True)

                    if not respost.ok:
                        mostrar_mensagem(
                            'Desculpe, mas não é possível fazer o download da imagem\nPeço para entrar em contato com o desenvolvedor e não realizar download de imagem até o problema ser corrigido',
                            'erro')
                        return ''
                    else:
                        for dado in respost.iter_content(1024):
                            if not dado:
                                break

                            imagem.write(dado)

                        mostrar_mensagem('Imagem salva com sucesso')
                imagem = existe_arquivo
        elif 'http://image.tmdb.org/' in imagem:
            with open(existe_arquivo, 'wb') as imagem:
                respost = requests.get(self.caminho_foto, stream=True)

                if not respost.ok:
                    mostrar_mensagem(
                        'Desculpe, mas não é possível fazer o download da imagem\nPeço para entrar em contato com o desenvolvedor e não realizar download de imagem até o problema ser corrigido',
                        'erro')
                    return ''
                else:
                    for dado in respost.iter_content(1024):
                        if not dado:
                            break

                        imagem.write(dado)

                    mostrar_mensagem('Imagem salva com sucesso')
            imagem = existe_arquivo
        else:
            auxiliar_filme = f'{titulo} ({ano})'
            auxiliar_imagem = re.split(r"[/.]\s*", imagem)
            if auxiliar_filme != auxiliar_imagem[-2]:
                mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem estão com titulo ou ano diferentes\n \
                                         Para prosseguir você tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem}',
                                 'erro')

        if filme == '':
            arquivo = self.caminho_filme.split('/')
            lista = informacoes3(arquivo[-1])
            for dados in lista:
                if titulo == dados[0]:
                    id = dados[5]
                    break
            else:
                id = self.id_filme
        else:
            id = self.id_filme

        if '/' in genero:
            genero = genero.title()

        auxiliar_arquivo = Filme(
            id=self.filme.id,
            titulo=titulo,
            ano=ano,
            nota=nota,
            genero=genero.strip(),
            extensao=extensao,
            cam_filme=filme,
            cam_imagem=imagem,
            sinopse=sinopse.replace("'",'"'))

        banco_filmes.alterar_dados(self.filme.id, auxiliar_arquivo, self.app.app.usuario.id)
        self.ir_tela_consultar(auxiliar_arquivo)
        mostrar_mensagem('Filme alterado com sucesso')

    def procurar_informacao(self):
        filme = self.caminho_filme
        if filme == '':
            mostrar_mensagem('Para procurar e adicionar as informações de um filme, você deve selecionar um filme')
            return ''
        arquivo = self.caminho_filme.split('/')
        auxiliar = informacoes3(arquivo[-1])
        self.frame.pack_forget()
        self.page_UPDATE_Auxiliar = UPDATE_Auxiliar(master=self.master, app=self, arquivo=arquivo[-1], lista=auxiliar)
        self.page_UPDATE_Auxiliar.tela_auxiliar()

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

    def tela_add_filmes(self, filme=''):
        self.frame.pack()
        if filme != '':
            if filme == 'Filme não Encontrado':
                mostrar_mensagem('Nenhum filme foi encontrado, recomendo revisar o titulo e o ano.','aviso')
                filme = ''
            if not filme[4] in 'None':
                resposta = perguntar('ARQUIVO DE MENSAGEM','Deseja utilizar a imagem do filme mostrada na tela anterior?')
                if resposta:
                    self.caminho_foto = filme[4]
                    self.photoImg = WebImage(filme[4], 350, 150).get()
                    self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                else:
                    mostrar_mensagem('Sem problemas')
            self.entrada_genero.delete(0, "end")
            self.entrada_sinopse.delete(1.0, END)
            self.entrada_genero.insert(0, filme[1])
            self.entrada_sinopse.insert('1.0', filme[3])
            self.id_filme = filme[5]

    def ir_tela_consultar(self,auxiliar=None):
        self.master.title('CONSULTAR FILME')
        tamanho_janela(self.master, 1000, 900)
        self.frame.pack_forget()
        self.app.app.atualiza_filmes(self.app.app.id)
        self.app.tela_read_filme(novo_filme=auxiliar)

class UPDATE_Auxiliar:
    def __init__(self, master=None, app=None, arquivo='', lista=[]):
        self.master = master
        self.app = app
        self.master.title('INFORMAÇÕES')
        tamanho_janela(self.master, 1000, 900)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()
        self.arquivo = arquivo
        self.id = 0
        frame_imagem = Frame(self.frame)
        frame_imagem.pack(side=TOP, pady=10)

        frame_sinopse = Frame(self.frame)
        frame_sinopse.pack(side=TOP, pady=10)

        frame_informacao = Frame(self.frame, bg='#154f91', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)

        #self.filmes = verificar_arquivos(r'D:\Filmes')
        #self.id = 0

        self.lista = lista

        if self.lista[self.id][4] != 'None':
            self.img = WebImage(self.lista[self.id][4], largura=550, altura=300).get()
        else:
            im = 'Images/naoEncontrado.jpg'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((550, 300))
            self.img = ImageTk.PhotoImage(im)

        self.imagem = Label(
            frame_imagem,
            image=self.img,
            bd=10,
            relief=RIDGE,
            background='#006266'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text=self.lista[self.id][3],
                             pady=20,
                             padx=20,
                             wraplength=600,
                             background='#006266',
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
            text=self.lista[self.id][0],
            background='#006266',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text=self.lista[self.id][1],
            background='#006266',
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
            text=self.lista[self.id][2][:4],
            background='#006266',
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
            command=lambda: self.ir_tela_add_filmes(filme_escolhido=self.lista[self.id])
        ).pack(
            side=LEFT,
            padx=20
        )

    def somar_id(self, novo_id):
        self.id = self.id + novo_id

    def zerar_id(self):
        self.id = 0

    def proximo(self):
        if len(self.lista) > self.id + 1:
            self.somar_id(1)
        else:
            mostrar_mensagem('Todos os filmes achados foram vistos\nSe você não achou seu filme, recomendo revisar o titulo e o ano.','aviso')
            self.zerar_id()
        if self.lista[self.id][4] != 'None':
            self.img = WebImage(self.lista[self.id][4], largura=550, altura=300).get()
            self.imagem.config(image=self.img)
        else:
            im = 'Images/naoEncontrado.jpg'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((550, 300))
            self.img = ImageTk.PhotoImage(im)
            self.imagem.configure(image=self.img)
        self.sinopse.config(text=self.lista[self.id][3])
        self.titulo_informacao.config(text=self.lista[self.id][0])
        self.genero_informacao.config(text=self.lista[self.id][1])
        self.ano_informacao.config(text=self.lista[self.id][2][:4])

    def tela_auxiliar(self):
        self.frame.pack()

    def ir_tela_add_filmes(self, filme_escolhido=''):
        self.master.title('ADICIONAR FILME')
        tamanho_janela(self.master, 950, 820)
        self.frame.pack_forget()
        self.app.tela_add_filmes(filme_escolhido)

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
        self.filme.aumentar_assistido()
        banco_filmes.alterar_like_dados(valor=self.filme.assistido, id=self.filme.id)
        startfile(self.filme.cam_filme)
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

class Pesquisar_Filme:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.master.title('PESQUISAR FILME')
        tamanho_janela(self.master, 1000, 1000)
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
        bt = Button(frame_pesquisa, image=self.pesquisar, bg='#154f91', command=self.pesquisar_filme)
        bt.pack(side=LEFT, fill="both", expand="yes", padx=20)

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
            padx=80
        )

        voltar_botao = Button(
            self.frame_botao,
            text='PRÓXIMO',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.proximo_filme
        ).pack(
            side=LEFT,
            padx=80
        )

    def pesquisar_filme(self):
        self.id = 0
        ano = self.entry_ano.get()

        titulo = self.entry_titulo.get()

        if titulo == '':
            mostrar_mensagem('O campo titulo deve ser preenchido','alerta')
            return ''

        if ano == '':
            self.lista_filmes = informacoes3(f'{titulo} ({ano}).amostra', False)
        else:
            try:
                ano = int(ano)
            except:
                mostrar_mensagem('O campo ano deve ser preenchido apenas com números', 'alerta')
                return ''

            if ano > datetime.datetime.now().year or ano < 1900:
                mostrar_mensagem('O campo ano deve ser preenchido com valores maiores que 1900 e menores ou igual ao ano atual', 'alerta')
                return ''
            self.lista_filmes = informacoes3(f'{titulo} ({ano}).amostra', False)

        if len(self.lista_filmes) == 0 or type(self.lista_filmes) == str:
            mostrar_mensagem('Nenhum filme foi encontrado', 'alerta')
            return ''
        else:
            mostrar_mensagem(f'Foram encontrados {len(self.lista_filmes)} de acordo com a seua pesquisa')

        self.alterar_eventos()

    def alterar_eventos(self):
        filme = self.lista_filmes[self.id]
        self.img = WebImage(filme[4], largura=550, altura=300).get()
        self.imagem.config(image=self.img)
        self.sinopse.config(text=filme[3])
        self.titulo_informacao.config(text=filme[0])
        self.genero_informacao.config(text=filme[1])
        self.ano_informacao.config(text=filme[2][:4])

    def proximo_filme(self):
        if self.id+1 < len(self.lista_filmes):
            self.id+=1
        else:
            self.id*=0
        self.alterar_eventos()

    def tela_pesquisar_filme(self):
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id,pesquise=False)
        self.app.tela_inicio()

class Consultar_Usuario:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.pastas = self.app.app.pasta_usuario
        self.usuario = self.app.app.usuario
        self.master.title('MENU DO USUÁRIO')
        tamanho_janela(self.master, 1130, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        frame_foto = Frame(self.frame, bg='#154f91')
        frame_foto.pack(side=LEFT, fill="both", expand="yes",padx=10)

        im = Image.open(self.usuario.foto)
        im.thumbnail((140, 100))
        self.photoImg = ImageTk.PhotoImage(im)

        self.foto_usuario = Button(
            frame_foto,
            image=self.photoImg,
            bg='#334B49',
            border=5,
            relief=RIDGE,
            height=100,
            width=100,
            command=self.ir_tela_inicio
        )
        self.foto_usuario.pack(anchor=NW,fill="both", expand="yes")

        label_nome = Label(
            frame_foto,
            text=self.usuario.nome.title(),
            fg='white',
            font=('Arial', 16),
            bg = '#1A857F',
            width=10,
            bd=2,
            relief=SOLID,
            wraplength=110
        )
        label_nome.pack(fill="both", expand="yes")

        self.botoes = []
        dicionario_botao = {
            0: ['ADICIONAR\nFILME',self.logoff],
            1: ['FILME\nALEATÓRIO', self.logoff],
            2: ['RECOMENDAÇÃO\nDE FILMES', self.logoff],
            3: ['PESQUISAR\nFILME', self.logoff],
            4: ['ORDENAR FILMES\nA-Z', self.logoff]
        }

        for id in range(4,-1,-1):
            botao = Button(frame_foto, text=dicionario_botao[id][0], bg='#154f91', fg='white',
                       font=('Arial', 10), border=15, command=dicionario_botao[id][1], relief=RAISED)
            self.botoes.append(botao)
            botao.pack(pady=30, side=BOTTOM, anchor=S, fill="both", expand="yes")

    def logoff(self):
        resposta = perguntar('AVISO','Você tem certeza que deseja fazer logoff?')
        if resposta:
            self.master.title('LOGIN')
            tamanho_janela(self.master, 700, 300)
            self.frame.pack_forget()
            self.app.app.tela_login()

    def tela_consultar_usuario(self):
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.atualiza_filmes(self.app.id,pesquise=False)
        self.app.tela_inicio()

if __name__ == '__main__':
    app = SM(root)
    root.mainloop()
