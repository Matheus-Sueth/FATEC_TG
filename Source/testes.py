from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk
from PIL import Image
from BACK_END.ControleDasPastas import *
from BACK_END.Usuario import Usuario
from BACK_END.PastasDAO import PastaDAO, Pasta, Colecao
from pathlib import Path
from BACK_END.RecomendaFilme import *
import urllib.request
import io
import re
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
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

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

    def logoff(self):
        resposta = messagebox.askquestion(
            "AVISO", "Voc?? tem certeza ?")

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
        self.entrada_email.insert(0,'matheus')
        self.entrada_email.pack()

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
        self.entrada_senha.insert(0,'1234')
        self.entrada_senha.pack()

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
            mostrar_mensagem('campo EMAIL n??o foi preenchido','aviso')
            self.entrada_email.focus_set()
        elif senha == '':
            mostrar_mensagem('campo SENHA n??o foi preenchido', 'aviso')
            self.entrada_senha.focus_set()
        else:
            usuario_login = Usuario(-1,'',email,senha,'')
            usuarios = cdu.atualiza_banco(cdu.banco_usuarios)
            lista_pastas = banco_pastas.ler_dados()
            for usuario in usuarios:
                if usuario == usuario_login:
                    self.usuario = usuario
                    self.indice = usuario.id
                    #self.indice = usuarios[usuarios.index(usuario)]
                    for pasta in lista_pastas:
                        if pasta[1] == self.indice:
                            self.pasta_usuario = pasta
                            break
                    else:
                        mostrar_mensagem('Usu??rio Encontrado e validado, mas para continuarmos vamos procurar a pasta dos filmes e a pasta das imagens', 'aviso')
                        caminho.caminho_filme, caminho.caminho_imagem = criar_pastas()
                        self.pasta_usuario = caminho
                        banco_pastas.inserir_dados(len(lista_pastas) + 1, self.indice, self.pasta_usuario)
                        mostrar_mensagem('Pastas Criadas\nPodemos prosseguir','info')
                    self.ir_tela_inicio()
                    break
                elif (usuario == usuario_login) == False:
                    mostrar_mensagem('Usu??rio encontrado, mas a senha est?? incorreta', 'aviso')
                    break
            else:
                mostrar_mensagem('Usu??rio n??o encontrado','aviso')

    def tela_login(self):
        self.frame.pack()
        # self.entrada_email.delete(0,END)
        # self.entrada_senha.delete(0,END)

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
        verifica_caminho_filmes(self.pasta_usuario[2])
        verifica_caminho_imagens(self.pasta_usuario[2])
        self.frame.pack_forget()
        self.page_2 = Inicio(master=self.master, app=self)
        self.page_2.tela_inicio()

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
            mostrar_mensagem('Arquivo de imagem corrompido ou inv??lido', 'erro')

    def cadastro(self):
        if self.caminho_foto == '':
            resposta = perguntar('Aviso','Campo FOTO n??o foi preenchido\nDeseja continuar mesmo assim ?')
            if not resposta:
                self.botao_2.focus_set()
                return None
            else:
                self.caminho_foto = 'Images/foto.png'
                im = Image.open(self.caminho_foto)
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
                self.botao_2.configure(text='', image=self.photoImg, height=150, width=150)

        if self.entrada_nome.get() == '':
            mostrar_mensagem('Campo NOME n??o foi preenchido', 'aviso')
            self.entrada_nome.focus_set()
        elif self.entrada_email.get() == '':
            mostrar_mensagem('Campo EMAIL n??o foi preenchido', 'aviso')
            self.entrada_email.focus_set()
        elif self.entrada_senha.get() == '':
            mostrar_mensagem('Campo SENHA n??o foi preenchido', 'aviso')
            self.entrada_senha.focus_set()
        else:
            foto = self.caminho_foto
            nome = self.entrada_nome.get()
            email = self.entrada_email.get()
            senha = self.entrada_senha.get()
            indice = len(cdu.lista_usuarios)+1
            novo_usuario = Usuario(indice,nome.title(), email, senha, foto)
            banco_usuarios.inserir_dados(novo_usuario)
            mostrar_mensagem('Usu??rio Criado\nAgora vamos procurar a pasta dos filmes e a pasta das imagens', 'info')
            caminho.caminho_filme, caminho.caminho_imagem = criar_pastas()
            banco_pastas.inserir_dados(len(lista_pastas)+1,indice,caminho)
            mostrar_mensagem('Pastas Criadas\nPodemos prosseguir', 'info')
            self.ir_tela_login()

    def ir_tela_login(self):
        self.frame.pack_forget()
        self.page_Login = Login(master=self.master, app=self.app)
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
        # with Linux OS
        self.master.bind("<Button-4>", self.mouse_wheel)
        self.master.bind("<Button-5>", self.mouse_wheel)
        self.app = app
        self.pastas = self.app.pasta_usuario
        self.usuario = self.app.usuario
        self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1125, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        self.objeto = [[0,840],[24,420],[48,210],[96,105],[192,57],[384,28]]

        self.id = 0
        self.mouse = 0
        self.end_barra = len(self.filmes) // 6 if len(self.filmes) % 6 != 0 or len(self.filmes) == 0 else len(self.filmes) // 6 - 1
        self.sliderlength = [dado[1] for dado in self.objeto if self.end_barra <= dado[0]][0]
        self.barra = Scale(self.frame, from_=self.id, to=self.end_barra, width=20, sliderlength=self.sliderlength, length=850, command=self.vervalor)
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
            1: ['FILME\nALEAT??RIO', self.aleatorio],
            2: ['RECOMENDA????O\nDE FILMES', self.recomendacao],
            3: ['GERAR\nRELAT??RIO', self.relatorio],
            4: ['ORDENAR\nFILMES', self.ordenar]
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
        bt = Button(frame_pesquisa, image=self.pesquisar, bg='#154f91', command=self.pesquisar_filmes)
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

        for numero in range(6):
            try:
                self.nomes_filmes.append([self.filmes[numero].titulo, self.filmes[numero]])
            except:
                self.nomes_filmes.append(['Filme N??o Encontrado', ''])

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

    def pesquisar_filmes(self):
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
        #print(f'Ordenar {self.filmes} por ?')

    def relatorio(self):
        print('Gerar relat??rio')
        for filme in self.filmes:
            print(filme)

    def ir_tela_ver_filme(self,filme):
        if filme[0] == 'Filme N??o Encontrado':
            mostrar_mensagem('N??o foi encontrado um filme\nSe deseja visulizar um filme, voc?? deve adicionar um filme','aviso')
        else:
            self.frame.pack_forget()
            self.page_READ_Filme = READ_Filme(master=self.master, app=self, filme=filme[1])
            self.page_READ_Filme.tela_read_filme()

    def recomendacao(self):
        print('Gerar recomenda????o de filme')
        print(self.titulo_filmes)

    def aleatorio(self):
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
        self.end_barra = len(self.filmes) // 6 if len(self.filmes) % 6 != 0 else len(self.filmes) // 6 - 1
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
        for numero in range(indice, indice+6):
            try:
                self.nomes_filmes.append([self.filmes[numero].titulo,self.filmes[numero]])
            except:
                self.nomes_filmes.append(['Filme N??o Encontrado',''])
        for numero in range(6):
            self.foto_filmes[numero][0].config(image=self.photoFilme[numero], command=lambda m=self.nomes_filmes[numero]: self.ir_tela_ver_filme(m))
            self.titulo_filmes[numero][0].config(text=self.nomes_filmes[numero][0])

    def vervalor(self,v):
        self.mouse = int(v)
        self.id = int(v)*6
        self.atualiza_filmes(self.id,False)

    def logoff(self):
        resposta = perguntar('AVISO','Voc?? tem certeza que deseja fazer logoff?')
        if resposta:
            self.master.title('LOGIN')
            tamanho_janela(self.master, 700, 300)
            self.frame.pack_forget()
            self.app.tela_login()

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
            text='GEN??RO',
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
                                          values=['N??O ASSISTIDO', 'P??SSIMO', 'MUITO RUIM', 'MAIS OU MENOS', 'MUITO BOM','EXCELENTE'],
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
                                 text='PROCURAR\nINFORMA????ES',
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
        imagem = self.caminho_foto
        if imagem == '':
            self.botao_slc_imagem.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve selecionar uma imagem')
            return ''
        nota = self.combobox_slc_nota.get()
        filme = self.caminho_filme
        if filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve selecionar um arquivo')
            return ''
        genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in self.entrada_genero.get())
        if 'Fic????o/Cient??fica' in genero:
            genero = genero.replace('Fic????o/Cient??fica','Fic????o Cient??fica')
        if 'Cinema/TV' in genero:
            genero = genero.replace('Cinema/TV','Cinema TV')
        if genero == '':
            self.entrada_genero.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve adicionar texto ao campo gen??ro')
            return ''
        sinopse = self.entrada_sinopse.get('1.0','end').strip()
        if sinopse == '':
            self.entrada_sinopse.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve adicionar texto ao campo sinopse')
            return ''

        aux_filme = re.split(r"[/()]\s*", filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)

        aux = fl.Filme('',titulo,ano,'','','','','','')

        for valor in valores:
            if valor == aux:
                mostrar_mensagem(f'{titulo} J?? EST?? CADASTRADO','aviso')
                return ''

        arquivos = ['png', 'jpg', 'jfif', 'jpeg']
        arquivo_encontrado = False
        for ext in arquivos:
            existe_arquivo = fr'{self.pastas[2].caminho_imagem}/{titulo} ({ano}).{ext}'
            if isfile(existe_arquivo):
                arquivo_encontrado = True
                break
        else:
            existe_arquivo = fr'{self.pastas[2].caminho_imagem}/{titulo} ({ano}).png'

        if arquivo_encontrado and 'http://image.tmdb.org/' in imagem:
                self.photoImg = WebImage(imagem, 350, 150).get()
                self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                resposta = perguntar("AVISO", f"J?? existe essa imagem({existe_arquivo})\nDeseja substituir a imagem?")
                if not resposta:
                    imagem = existe_arquivo
                    aux = Image.open(existe_arquivo)
                    aux.thumbnail((150, 150))
                    self.photoImg = ImageTk.PhotoImage(aux)
                    self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                    resposta2 = perguntar("AVISO", f"Deseja utilizar a imagem existente no caminho ({existe_arquivo})?")
                    if not resposta2:
                        mostrar_mensagem('Ent??o o filme n??o ser?? adicionado','aviso')
                        return ''
                else:
                    with open(existe_arquivo, 'wb') as imagem:
                        respost = requests.get(self.caminho_foto, stream=True)

                        if not respost.ok:
                            mostrar_mensagem('Desculpe, mas n??o ?? poss??vel fazer o download da imagem\nPe??o para entrar em contato com o desenvolvedor e n??o realizar download de imagem at?? o problema ser corrigido','erro')
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
                    mostrar_mensagem('Desculpe, mas n??o ?? poss??vel fazer o download da imagem\nPe??o para entrar em contato com o desenvolvedor e n??o realizar download de imagem at?? o problema ser corrigido','erro')
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
                mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem est??o com titulo ou ano diferentes\n \
                                 Para prosseguir voc?? tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem[-2]}','erro')
                return ''

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

        aux = fl.Filme(
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
            mostrar_mensagem('Para procurar e adicionar as informa????es de um filme, voc?? deve selecionar um filme')
            return ''
        arquivo = self.caminho_filme.split('/')
        self.frame.pack_forget()
        lista = informacoes3(arquivo[-1])
        self.page_ADD_Auxiliar = ADD_Auxiliar(master=self.master, app=self, lista=lista)
        self.page_ADD_Auxiliar.tela_auxiliar()

    def selecionar_arquivo(self, tipo_arquivo, title):
        if title == 'Escolha uma imagem':
            inicio = self.pastas[2].caminho_imagem
        else:
            inicio = self.pastas[2].caminho_filme
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
                    mostrar_mensagem(f'Arquivo da imagem n??o est?? dentro da pasta = {self.pastas[2].caminho_imagem}',
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
                mostrar_mensagem('Arquivo de imagem corrompido ou inv??lido', 'erro')
        else:
            try:
                tam_caminho_filme = self.pastas[2].caminho_filme
                if caminho[:len(tam_caminho_filme)] != self.pastas[2].caminho_filme:
                    mostrar_mensagem(f'Arquivo do filme n??o est?? dentro da pasta = {self.pastas[2].caminho_filme}', 'erro')
                    return ''
                self.caminho_filme = caminho
                arquivo = self.caminho_filme.split('/')
                self.botao_slc_arquivo.config(text=arquivo[-1])
            except:
                self.caminho_filme = ''
                mostrar_mensagem('Arquivo do filme corrompido ou inv??lido', 'erro')

    def tela_add_filmes(self, filme=''):
        self.frame.pack()
        if filme != '':
            if filme == 'Filme n??o Encontrado':
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
        self.filmes = verificar_arquivos(self.pastas[2].caminho_filme)
        self.imagens = verificar_arquivos(self.pastas[2].caminho_imagem)
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        for indice in range(len(self.filmes)):
            self.caminho_filme = self.filmes[indice]
            self.caminho_foto = ''
            #self.botao_slc_arquivo.config(text=filme)
            aux_filme = re.split(r"[/()]\s*", self.filmes[indice])
            titulo = aux_filme[-3].strip()
            ano = int(aux_filme[-2])
            extensao = aux_filme[-1].strip()
            aux = fl.Filme('', titulo, ano, '', '', extensao, self.filmes[indice], '', '')
            if aux in valores:
                continue
            arquivo = self.caminho_filme.split('/')
            lista = informacoes3(arquivo[-1])
            auxiliar_lista = lista[0][0].replace(':',' -')
            print(lista[0][0].strip())
            print(auxiliar_lista.lower(), titulo.lower())
            if auxiliar_lista.lower() != titulo.lower():
                mostrar_mensagem(f'O filme: {aux} est?? com o nome errado no arquivo.\nAltere para {auxiliar_lista} ({lista[0][2][:4]}){extensao}')
                return ''

            if int(lista[0][2][:4]) != ano:
                mostrar_mensagem(f'O filme: {aux} est?? com o ano errado no arquivo.\nAltere para {lista[0][0]} ({lista[0][2][:4]}){extensao}')
                return ''

            self.caminho_foto = lista[0][4]

            #for imagem in self.imagens:
             #   aux_imagem = re.split(r"[/()]\s*", imagem)
              #  if titulo.strip() == aux_imagem[-3].strip() and ano == int(aux_imagem[-2]):
               #     self.caminho_foto = imagem
                #    aux_img = Image.open(self.caminho_foto)
                 #   aux_img.thumbnail((150, 150))
                  #  self.photoImg = ImageTk.PhotoImage(aux_img)
                   # self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                    #break

            arquivos = ['png', 'jpg', 'jfif', 'jpeg']
            arquivo_encontrado = False
            for ext in arquivos:
                existe_arquivo = fr'{self.pastas[2].caminho_imagem}/{titulo} ({ano}).{ext}'
                if isfile(existe_arquivo):
                    self.caminho_foto = existe_arquivo
                    arquivo_encontrado = True
                    break
            else:
                existe_arquivo = fr'{self.pastas[2].caminho_imagem}/{titulo} ({ano}).png'

            if arquivo_encontrado and 'http://image.tmdb.org/' in self.caminho_foto:
                resposta = perguntar("AVISO", f"J?? existe essa imagem({existe_arquivo})\nDeseja substituir a imagem?")
                if not resposta:
                    self.caminho_foto = existe_arquivo
                    resposta2 = perguntar("AVISO", f"Deseja utilizar a imagem existente no caminho ({existe_arquivo})?")
                    if not resposta2:
                        mostrar_mensagem('Ent??o o filme n??o ser?? adicionado', 'aviso')
                        return ''
                else:
                    with open(existe_arquivo, 'wb') as self.caminho_foto:
                        respost = requests.get(self.caminho_foto, stream=True)

                        if not respost.ok:
                            mostrar_mensagem(
                                'Desculpe, mas n??o ?? poss??vel fazer o download da imagem\nPe??o para entrar em contato com o desenvolvedor e n??o realizar download de imagem at?? o problema ser corrigido',
                                'erro')
                            return ''
                        else:
                            for dado in respost.iter_content(1024):
                                if not dado:
                                    break

                                self.caminho_foto.write(dado)

                            #mostrar_mensagem('Imagem salva com sucesso')
                    self.caminho_foto = existe_arquivo
            elif 'http://image.tmdb.org/' in self.caminho_foto:
                with open(existe_arquivo, 'wb') as imagem:
                    respost = requests.get(self.caminho_foto, stream=True)

                    if not respost.ok:
                        mostrar_mensagem(
                            'Desculpe, mas n??o ?? poss??vel fazer o download da imagem\nPe??o para entrar em contato com o desenvolvedor e n??o realizar download de imagem at?? o problema ser corrigido',
                            'erro')
                        return ''
                    else:
                        for dado in respost.iter_content(1024):
                            if not dado:
                                break

                            imagem.write(dado)

                        #mostrar_mensagem('Imagem salva com sucesso')
                self.caminho_foto = existe_arquivo
            else:
                auxiliar_filme = f'{titulo} ({ano})'
                auxiliar_imagem = re.split(r"[/)]\s*", self.caminho_foto)
                auxiliar_imagem2 = auxiliar_imagem[-2] + ')'
                if auxiliar_filme != auxiliar_imagem2:
                    mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem est??o com titulo ou ano diferentes\n \
                                             Para prosseguir voc?? tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem2}',
                                     'erro')
                    return ''

            if len(lista) == 1:
                #self.entrada_genero.delete(0, "end")
                #self.entrada_sinopse.delete(1.0, END)
                #self.entrada_genero.insert(0, lista[0][1].strip())
                #self.entrada_sinopse.insert('1.0', lista[0][3].strip())
                genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in
                                 lista[0][1])
                if 'Fic????o/Cient??fica' in genero:
                    genero = genero.replace('Fic????o/Cient??fica', 'Fic????o Cient??fica')
                if 'Cinema/TV' in genero:
                    genero = genero.replace('Cinema/TV', 'Cinema TV')
                if '/' in genero:
                    genero = genero.title()
                sinopse = lista[0][3].strip()
                id = lista[0][5]
                aux = fl.Filme(
                    id=f'{self.usuario.id}.{id}',
                    titulo=titulo,
                    ano=ano,
                    nota='N??O ASSISTIDO',
                    genero=genero.strip(),
                    extensao=extensao,
                    cam_filme=self.caminho_filme,
                    cam_imagem=self.caminho_foto,
                    sinopse=sinopse.replace("'", '"'))
                banco_filmes.inserir_dados(self.usuario.id, aux)
                mostrar_mensagem(f'Filme: {aux} foi adicionado com sucesso')
                self.limpar_informacoes()
                self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ler_dados(usuario_id=self.usuario.id))}'
            else:
                self.botao_slc_arquivo.config(text=self.filmes[indice])
                self.frame.pack_forget()
                self.page_ADD_Auxiliar = ADD_Auxiliar(master=self.master, app=self, lista=lista)
                self.page_ADD_Auxiliar.tela_auxiliar()
                mostrar_mensagem(f'Vamos adicionar agora o filme:\n{aux}')
                return ''
        else:
            mostrar_mensagem('Todos os filmes foram adicionados','info')

class ADD_Auxiliar:
    def __init__(self, master=None, app=None, lista=[]):
        self.master = master
        self.app = app
        self.master.title('INFORMA????ES')
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
            text='PR??XIMO',
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
            mostrar_mensagem('Todos os filmes achados foram vistos\nSe voc?? n??o achou seu filme, recomendo revisar o titulo e o ano.','aviso')
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
    def __init__(self, master=None, app=None, filme=fl.Filme):
        self.master = master
        self.app = app
        self.master.title('CONSULTAR FILME')
        tamanho_janela(self.master, 1000, 900)
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
        if isfile(self.filme.cam_imagem):
            try:
                im = Image.open(self.filme.cam_imagem)
                im.thumbnail((550, 300))
                self.img = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((550, 300))
                self.img = ImageTk.PhotoImage(im)
        else:
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
                im.thumbnail((550, 300))
                self.photoImg = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((550, 300))
                self.photoImg = ImageTk.PhotoImage(im)
        else:
            im = 'Images/naoEncontrado.png'
            im = Image.open(rf'{Path(im).absolute()}')
            im.thumbnail((550, 300))
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
            text='GEN??RO',
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
        notas = ['N??O ASSISTIDO', 'P??SSIMO', 'MUITO RUIM', 'MAIS OU MENOS', 'MUITO BOM','EXCELENTE']
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
                                 text='PROCURAR\nINFORMA????ES',
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
            mostrar_mensagem('Para adicionar um filme, voc?? deve selecionar uma imagem')
            return ''
        nota = self.combobox_slc_nota.get()
        filme = self.caminho_filme
        if filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve selecionar um arquivo')
            return ''
        genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in
                         self.entrada_genero.get())
        if 'Fic????o/Cient??fica' in genero:
            genero = genero.replace('Fic????o/Cient??fica', 'Fic????o Cient??fica')
        if 'Cinema/TV' in genero:
            genero = genero.replace('Cinema/TV', 'Cinema TV')
        if genero == '':
            self.entrada_genero.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve adicionar texto ao campo gen??ro')
            return ''
        sinopse = self.entrada_sinopse.get('1.0', 'end').strip()
        if sinopse == '':
            self.entrada_sinopse.focus_set()
            mostrar_mensagem('Para adicionar um filme, voc?? deve adicionar texto ao campo sinopse')
            return ''

        aux_filme = re.split(r"[/()]\s*", filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)

        arquivos = ['png', 'jpg', 'jfif', 'jpeg']
        arquivo_encontrado = False
        for ext in arquivos:
            existe_arquivo = fr'{self.pastas[2].caminho_imagem}/{titulo} ({ano}).{ext}'
            if isfile(existe_arquivo):
                arquivo_encontrado = True
                break
        else:
            existe_arquivo = fr'{self.pastas[2].caminho_imagem}/{titulo} ({ano}).png'

        if arquivo_encontrado and 'http://image.tmdb.org/' in imagem:
            self.photoImg = WebImage(imagem, 350, 150).get()
            self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
            resposta = perguntar("AVISO", f"J?? existe essa imagem({existe_arquivo})\nDeseja substituir a imagem?")
            if not resposta:
                imagem = existe_arquivo
                aux = Image.open(existe_arquivo)
                aux.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(aux)
                self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                resposta2 = perguntar("AVISO", f"Deseja utilizar a imagem existente no caminho ({existe_arquivo})?")
                if not resposta2:
                    mostrar_mensagem('Ent??o o filme n??o ser?? adicionado', 'aviso')
                    return ''
            else:
                with open(existe_arquivo, 'wb') as imagem:
                    respost = requests.get(self.caminho_foto, stream=True)

                    if not respost.ok:
                        mostrar_mensagem(
                            'Desculpe, mas n??o ?? poss??vel fazer o download da imagem\nPe??o para entrar em contato com o desenvolvedor e n??o realizar download de imagem at?? o problema ser corrigido',
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
                        'Desculpe, mas n??o ?? poss??vel fazer o download da imagem\nPe??o para entrar em contato com o desenvolvedor e n??o realizar download de imagem at?? o problema ser corrigido',
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
                mostrar_mensagem(f'O arquivo do filme e o arquivo da imagem est??o com titulo ou ano diferentes\n \
                                         Para prosseguir voc?? tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem}',
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

        auxiliar_arquivo = fl.Filme(
            id=self.filme.id,
            titulo=titulo,
            ano=ano,
            nota=nota,
            genero=genero.strip(),
            extensao=extensao,
            cam_filme=filme,
            cam_imagem=imagem,
            sinopse=sinopse.replace("'", '"'))

        banco_filmes.alterar_dados(self.filme.id, auxiliar_arquivo, self.app.app.usuario.id)
        self.ir_tela_consultar(auxiliar_arquivo)
        mostrar_mensagem('Filme alterado com sucesso')

    def procurar_informacao(self):
        filme = self.caminho_filme
        if filme == '':
            mostrar_mensagem('Para procurar e adicionar as informa????es de um filme, voc?? deve selecionar um filme')
            return ''
        arquivo = self.caminho_filme.split('/')
        auxiliar = informacoes3(arquivo[-1])
        self.frame.pack_forget()
        self.page_UPDATE_Auxiliar = UPDATE_Auxiliar(master=self.master, app=self, arquivo=arquivo[-1], lista=auxiliar)
        self.page_UPDATE_Auxiliar.tela_auxiliar()

    def selecionar_arquivo(self, tipo_arquivo, title):
        if title == 'Escolha uma imagem':
            inicio = self.pastas[2].caminho_imagem
        else:
            inicio = self.pastas[2].caminho_filme
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
                    mostrar_mensagem(f'Arquivo da imagem n??o est?? dentro da pasta = {self.pastas[2].caminho_imagem}',
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
                mostrar_mensagem('Arquivo de imagem corrompido ou inv??lido', 'erro')
        else:
            try:
                tam_caminho_filme = self.pastas[2].caminho_filme
                if caminho[:len(tam_caminho_filme)] != self.pastas[2].caminho_filme:
                    mostrar_mensagem(f'Arquivo do filme n??o est?? dentro da pasta = {self.pastas[2].caminho_filme}', 'erro')
                    return ''
                self.caminho_filme = caminho
                arquivo = self.caminho_filme.split('/')
                self.botao_slc_arquivo.config(text=arquivo[-1])
            except:
                self.caminho_filme = ''
                mostrar_mensagem('Arquivo do filme corrompido ou inv??lido', 'erro')

    def tela_add_filmes(self, filme=''):
        self.frame.pack()
        if filme != '':
            if filme == 'Filme n??o Encontrado':
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
        self.master.title('INFORMA????ES')
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
            text='PR??XIMO',
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
            mostrar_mensagem('Todos os filmes achados foram vistos\nSe voc?? n??o achou seu filme, recomendo revisar o titulo e o ano.','aviso')
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
        self.master.title('FILME ALEAT??RIO')
        tamanho_janela(self.master, 1000, 900)
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
                im.thumbnail((550, 300))
                self.img = ImageTk.PhotoImage(im)
            except:
                im = 'Images/naoEncontrado.png'
                im = Image.open(rf'{Path(im).absolute()}')
                im.thumbnail((550, 300))
                self.img = ImageTk.PhotoImage(im)
        else:
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
        self.app.atualiza_filmes(self.app.id)
        self.app.tela_inicio()

if __name__ == '__main__':
    app = SM(root)
    root.mainloop()
