from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk
from PIL import Image
from BACK_END.ControleDasPastas import *
from BACK_END.Usuario import Usuario
from BACK_END.PastasDAO import PastaDAO
from pathlib import Path
from BACK_END.RecomendaFilme import *
import urllib.request
import io
import re
from os.path import isfile
from os import startfile

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

class Login:
    def __init__(self, root=None):
        self.root = root
        self.root.title('LOGIN')
        tamanho_janela(self.root, 700, 330)
        self.frame = Frame(self.root, bg='#154f91')
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
        self.entrada_email.insert(0,'chap@')
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
        self.entrada_senha.insert(0,'malok')
        self.entrada_senha.pack()

        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)
        botao = Button(
            frame_botao,
            text='CADASTRAR USUÁRIO',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.ir_tela_cadastro
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
            usuarios = cdu.atualiza_banco(cdu.banco_usuarios)
            lista_pastas = banco_pastas.ler_dados()
            for usuario in usuarios:
                if usuario.email == email and usuario.senha == senha:
                    self.usuario = usuario
                    self.indice = usuarios[usuarios.index(usuario)]
                    for pasta in lista_pastas:
                        if pasta[1] == self.indice.id:
                            self.pasta_usuario = pasta
                            break
                    else:
                        mostrar_mensagem('Usuário Encontrado e validado, mas para continuarmos vamos procurar a pasta dos filmes e a pasta das imagens', 'aviso')
                        caminhos = criar_pastas()
                        banco_pastas.inserir_dados(len(lista_pastas) + 1, indice, caminhos[0], caminhos[1],
                                                       caminho.caminho_banco)
                        mostrar_mensagem('Pastas Criadas\nPodemos prosseguir','info')
                    self.ir_tela_inicio()
                    break
                elif usuario.email == email and usuario.senha != senha:
                    mostrar_mensagem('Usuário encontrado, mas a senha está incorreta', 'aviso')
                    break
            else:
                mostrar_mensagem('Usuário não encontrado','aviso')

    def tela_login(self):
        self.frame.pack()
        self.entrada_email.delete(0,END)
        self.entrada_senha.delete(0,END)

    def ir_tela_cadastro(self):
        self.page_1 = Cadastro(master=self.root, app=self)
        self.frame.pack_forget()
        self.page_1.tela_cadastro()

    def ir_tela_inicio(self):
        verifica_caminho_filmes(self.pasta_usuario[2])
        verifica_caminho_imagens(self.pasta_usuario[2])
        self.frame.pack_forget()
        self.page_2 = Inicio(master=self.root, app=self, usuario=self.usuario, pastas=self.pasta_usuario)
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
            bg='#006266',
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
                       border=15, command=self.ir_tela_login)
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
            resposta = perguntar('Aviso','Campo FOTO não foi preenchido\nDeseja continuar mesmo assim ?')
            if not resposta:
                self.botao_2.focus_set()
                return None
            else:
                self.caminho_foto = 'Images/foto.png'
                im = Image.open(self.caminho_foto)
                im.thumbnail((150, 150))
                self.photoImg = ImageTk.PhotoImage(im)
                self.botao_2.configure(text='', image=self.photoImg)

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
            indice = len(cdu.lista_usuarios)+1
            novo_usuario = Usuario(indice,nome.title(), email, senha, foto)
            banco_usuarios.inserir_dados(novo_usuario)
            mostrar_mensagem('Usuário Criado\nAgora vamos procurar a pasta dos filmes e a pasta das imagens', 'info')
            caminho.caminho_filme, caminho.caminho_imagem = criar_pastas()
            banco_pastas.inserir_dados(len(lista_pastas)+1,indice,caminho)
            mostrar_mensagem('Pastas Criadas\nPodemos prosseguir', 'info')
            self.ir_tela_login()

    def tela_cadastro(self):
        self.frame.pack()

    def ir_tela_login(self):
        self.frame.pack_forget()
        self.master.title('LOGIN')
        tamanho_janela(self.master, 700, 300)
        self.app.tela_login()

class Inicio:
    def __init__(self, master=None, app=None, usuario=Usuario, pastas=[]):
        self.master = master
        self.app = app
        self.pastas = pastas
        self.usuario = usuario
        self.usuario
        self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1125, 850)
        self.frame = Frame(self.master, bg='#154f91')
        self.frame.pack()

        self.objeto = [[0,840],[24,420],[48,210],[96,105],[192,57],[384,28]]

        self.id = 0
        self.end_barra = len(self.filmes) // 6 if len(self.filmes) % 6 != 0 else len(self.filmes) // 6 - 1
        #self.end_barra = 24
        self.sliderlength = [dado[1] for dado in self.objeto if self.end_barra <= dado[0]][0]
        #self.sliderlength = 420
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
            bg='#006266',
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
            bg = '#006266',
            width=10,
            wraplength=110
        )
        label_nome.pack(fill="both", expand="yes")

        self.botoes = []
        dicionario_botao = {
            0:['GERENCIAR\nFILMES',self.ir_tela_gerenciar],
            1:['FILME\nALEATÓRIO', self.aleatorio],
            2:['RECOMENDAÇÃO\nDE FILMES', self.recomendacao],
            3:['GERAR\nRELATÓRIO', self.relatorio]
        }

        for id in range(4):
            botao = Button(frame_foto, text=dicionario_botao[id][0], bg='#154f91', fg='white',
                       font=('Arial', 10), border=15, command=dicionario_botao[id][1], relief=RAISED)
            self.botoes.append(botao)
            botao.pack(pady=50, side=BOTTOM, anchor=S, fill="both", expand="yes")

        frame_usuario2 = Frame(self.frame, bg='#154f91')
        frame_usuario2.pack(side=RIGHT, anchor=NE,padx=15)

        frame_pesquisa = Frame(frame_usuario2, bg='#154f91')
        frame_pesquisa.pack()

        entry = Entry(
            frame_pesquisa,
            #bg='#863700',
            #fg='white',
            width=40,
            font=('Arial', 20),
            border=2,
            relief=GROOVE
        )
        entry.pack(side=LEFT,fill="both", expand="yes")
        im = Image.open(r'Images/lupa.png')
        im.thumbnail((30, 30))
        self.pesquisar = ImageTk.PhotoImage(im)
        bt = Button(frame_pesquisa, image=self.pesquisar, bg='#154f91')
        bt.pack(side=LEFT,fill="both", expand="yes")
        im = Image.open(r'Images/eng.png')
        im.thumbnail((30, 30))
        self.ico = ImageTk.PhotoImage(im)
        filtro = Button(frame_pesquisa, image=self.ico, bg='#154f91')
        filtro.pack(side=LEFT)

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
                bg='#006266',
                border=5,
                relief=RIDGE,
                height=150,
                width=100,
                command=lambda m=self.nomes_filmes[numero]: self.ver_filme(m)
            )
            self.foto_filmes.append([foto_filme, numero])
            foto_filme.pack(side=TOP,fill="both", expand="yes")
            self.label_titulo = Label(
                self.frame_foto,
                text=self.nomes_filmes[numero][0],
                fg='white',
                font=('Arial', 10),
                bg='#006266',
                height=3,
                width=21,
                wraplength=170
            )
            self.titulo_filmes.append([self.label_titulo, numero])
            self.label_titulo.pack(fill="both", expand="yes")

    def relatorio(self):
        print('Gerar relatório')
        for filme in self.filmes:
            print(filme)

    def ver_filme(self,filme):
        if filme[0] == 'Filme Não Encontrado':
            mostrar_mensagem('Não foi encontrado um filme\nSe deseja visulizar um filme, você deve adicionar um filme','aviso')
        else:
            self.frame.pack_forget()
            self.page_4 = READ_Filme(master=self.master, app=self, filme=filme[1])
            self.page_4.tela_read_filme()

    def recomendacao(self):
        print('Gerar recomendação de filme')
        print(self.titulo_filmes)

    def aleatorio(self):
        print('Gerar filme aleatório')
        self.atualiza_filmes(self.id)

    def atualiza_filmes(self, indice=0):
        self.photoFilme.clear()
        self.nomes_filmes.clear()
        self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
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
                self.nomes_filmes.append(['Filme Não Encontrado',''])
        for numero in range(6):
            self.foto_filmes[numero][0].config(image=self.photoFilme[numero], command=lambda m=self.nomes_filmes[numero]: self.ver_filme(m))
            self.titulo_filmes[numero][0].config(text=self.nomes_filmes[numero][0])

    def vervalor(self,v):
        self.id = int(v)*6
        self.atualiza_filmes(self.id)

    def logoff(self):
        resposta = perguntar('AVISO','Você tem certeza que deseja fazer logoff?')
        if resposta:
            self.master.title('LOGIN')
            tamanho_janela(self.master, 700, 300)
            self.frame.pack_forget()
            self.app.tela_login()

    def tela_inicio(self):
        self.frame.pack()

    def ir_tela_gerenciar(self):
        self.filmes = banco_filmes.ler_dados(usuario_id=self.usuario.id)
        self.page_3 = GerenciarFilmes(master=self.master, app=self, usuario=self.usuario, pastas=self.pastas,filmes=self.filmes)
        self.frame.pack_forget()
        self.page_3.tela_gerenciar()

class GerenciarFilmes:
    def __init__(self, master=None, app=None, usuario=Usuario, pastas=[], filmes=[]):
        self.master = master
        self.master.title('GERENCIAR FILMES')
        tamanho_janela(self.master, 350, 750)
        self.app = app
        self.pastas = pastas
        self.usuario = usuario
        self.filmes = filmes
        self.frame = Frame(self.master, bg='#154f91')
        frame_filmes = Frame(self.frame, bg='#154f91')
        frame_filmes.pack(pady=20)
        frame_usuarios = Frame(self.frame, bg='#154f91')
        frame_usuarios.pack(pady=20, side=LEFT)

        self.texto = Label(frame_filmes, text=f'VOCÊ TEM\n{len(self.filmes)} FILMES', background='#154f91', fg='white', height=3, width=20,
                      font=('Arial', 20))
        self.texto.pack(pady=10)
        botao = Button(frame_filmes, text='ADICIONAR FILMES', bg='#154f91', fg='white', height=5, width=30,
                       font=('Arial', 10), border=15, command=self.ir_tela_add_filmes)
        botao.pack(pady=10)
        botao = Button(frame_filmes, text='ALTERAR FILMES', bg='#154f91', fg='white', height=5, width=30,
                       font=('Arial', 10), border=15, command=self.ir_tela_inicio)
        botao.pack(pady=10)
        botao = Button(frame_filmes, text='DELETAR FILMES', bg='#154f91', fg='white', height=5, width=30,
                       font=('Arial', 10), border=15, command=self.ir_tela_inicio)
        botao.pack(pady=10)
        botao = Button(frame_filmes, text='VOLTAR', bg='#154f91', fg='white', height=5, width=30, font=('Arial', 10), border=15,
                       command=self.ir_tela_inicio)
        botao.pack(pady=10)

    def tela_gerenciar(self):
        self.texto.config(text=f'VOCÊ TEM\n{len(banco_filmes.ler_dados(usuario_id=self.usuario.id))} FILMES')
        self.frame.pack()

    def ir_tela_add_filmes(self):
        self.page_4 = ADD_Filme(master=self.master, app=self, usuario=self.usuario, pastas=self.pastas, lista_filmes=self.filmes)
        self.frame.pack_forget()
        self.page_4.tela_add_filmes()

    def ir_tela_inicio(self):
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.frame.pack_forget()
        self.app.tela_inicio()

class ADD_Filme:
    def __init__(self, master=None, app=None, usuario=Usuario, pastas=[], lista_filmes=[]):
        self.master = master
        self.master.title('ADICIONAR FILME')
        tamanho_janela(self.master, 950, 820)
        self.app = app
        self.pastas = pastas
        self.usuario = usuario
        self.lista = lista_filmes
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
            bg='#006266',
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
                                      command=self.ir_tela_gerenciar)
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
                                       text='PROCURAR FILMES\nE ADICIONAR',
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
            mostrar_mensagem('Para adicionar um filme, você deve selecionar uma imagem')
            return ''
        nota = self.combobox_slc_nota.get()
        filme = self.caminho_filme
        if filme == '':
            self.botao_slc_arquivo.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve selecionar um arquivo')
            return ''
        genero = ''.join(char.replace(char, '/') if not char.isalnum() and not '/' == char else char for char in self.entrada_genero.get())
        if 'Ficção/Científica' in genero:
            genero = genero.replace('Ficção/Científica','Ficção Científica')
        if 'Cinema/TV' in genero:
            genero = genero.replace('Cinema/TV','Cinema TV')
        if genero == '':
            self.entrada_genero.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve adicionar texto ao campo genêro')
            return ''
        sinopse = self.entrada_sinopse.get('1.0','end')
        if sinopse == '':
            self.entrada_sinopse.focus_set()
            mostrar_mensagem('Para adicionar um filme, você deve adicionar texto ao campo sinopse')
            return ''

        aux_filme = re.split(r"[/()]\s*", filme)
        titulo = aux_filme[-3].strip()
        ano = int(aux_filme[-2])
        extensao = aux_filme[-1].strip()
        valores = banco_filmes.ler_dados(usuario_id=self.usuario.id)

        for valor in valores:
            if valor.titulo == titulo and valor.ano == ano:
                mostrar_mensagem(f'{titulo} JÁ ESTÁ CADASTRADO','aviso')
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
                resposta = perguntar("AVISO", f"Já existe essa imagem({existe_arquivo})\nDeseja substituir a imagem?")
                if not resposta:
                    resposta2 = perguntar("AVISO", f"Deseja utilizar a imagem existente no caminho ({existe_arquivo})?")
                    if resposta2:
                        imagem = existe_arquivo
                        aux = Image.open(existe_arquivo)
                        aux.thumbnail((150, 150))
                        self.photoImg = ImageTk.PhotoImage(aux)
                        self.botao_slc_imagem.config(image=self.photoImg, height=150, width=150)
                    else:
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
                                 Para prosseguir você tem que arrumar os arquivos\nArquivo do filme = {auxiliar_filme}\nArquivo da imagem = {auxiliar_imagem}','erro')
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
            genero=genero,
            extensao=extensao,
            cam_filme=filme,
            cam_imagem=imagem,
            sinopse=sinopse)
        banco_filmes.inserir_dados(self.usuario.id, aux)
        mostrar_mensagem('Filme adicionado com sucesso')
        self.limpar_informacoes()
        self.id_filme = f'{self.usuario.id}.-1.{len(banco_filmes.ler_dados(usuario_id=self.usuario.id))}'

    def procurar_informacao(self):
        filme = self.caminho_filme
        if filme == '':
            mostrar_mensagem('Para procurar e adicionar as informações de um filme, você deve selecionar um filme')
            return ''
        arquivo = self.caminho_filme.split('/')
        self.frame.pack_forget()
        self.page_4_auxiliar = Add_Auxiliar(master=self.master, app=self, arquivo=arquivo[-1])
        self.page_4_auxiliar.tela_auxiliar()

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
                tam_caminho_filme = self.pastas[2].caminho_filme
                if caminho[:len(tam_caminho_filme)] != self.pastas[2].caminho_filme:
                    mostrar_mensagem(f'Arquivo do filme não está dentro da pasta = {self.pastas[2].caminho_filme}', 'erro')
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

    def ir_tela_gerenciar(self):
        self.master.title('GERENCIAR FILMES')
        tamanho_janela(self.master, 350, 750)
        self.frame.pack_forget()
        self.app.app.atualiza_filmes(self.app.app.id)
        self.app.tela_gerenciar()

    def procurar_filmes(self):
        self.filmes = verificar_arquivos(self.pastas[2].caminho_filme)
        print(len(self.filmes))

class Add_Auxiliar:
    def __init__(self, master=None, app=None, arquivo=''):
        self.master = master
        self.app = app
        self.master.title('MENU INICIAL')
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

        self.lista = informacoes3(self.arquivo)

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

        frame_informacao = Frame(self.frame, bg='#006266', bd=5, relief=SOLID)
        frame_informacao.pack(side=TOP, pady=10)

        frame_botao = Frame(self.frame, bg='#154f91')
        frame_botao.pack(pady=20)
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

        self.imagem = Label(
            frame_imagem,
            image=self.img,
            bd=10,
            relief=RIDGE,
            background='#006266'
        )
        self.imagem.pack()

        self.sinopse = Label(frame_sinopse,
                             text=self.filme.sinopse,
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
            text=self.filme.titulo,
            background='#006266',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.titulo_informacao.pack()

        self.genero_informacao = Label(
            frame_informacao,
            text=self.filme.genero,
            background='#006266',
            fg='white',
            height=2,
            width=60,
            font=('Arial', 14)
        )
        self.genero_informacao.pack(
            side=BOTTOM
        )

        frame_informacao_auxiliar = Frame(frame_informacao, bg='#006266')
        frame_informacao_auxiliar.pack(side=TOP)

        self.ano_informacao = Label(
            frame_informacao_auxiliar,
            text=self.filme.ano,
            background='#006266',
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
            background='#006266',
            fg='white',
            height=2,
            width=29,
            font=('Arial', 14)
        )
        self.nota_informacao.pack(
            side=RIGHT
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
            command=self.ir_tela_inicio
        ).pack(
            side=LEFT,
            padx=100
        )

        gerar_botao = Button(
            frame_botao,
            text='ASSISTIR',
            bg='#154f91',
            fg='white',
            height=3,
            width=30,
            font=('Arial', 10),
            border=15,
            command=self.assistir_filme
        ).pack(
            side=LEFT,
            padx=120
        )

    def assistir_filme(self):
        self.filme.aumentar_assistido()
        banco_filmes.alterar_like_dados(valor=self.filme.assistido, id=self.filme.id)
        startfile(self.filme.cam_filme)
        self.master.destroy()

    def tela_read_filme(self):
        self.frame.pack()

    def ir_tela_inicio(self):
        self.frame.pack_forget()
        self.master.title('MENU INICIAL')
        tamanho_janela(self.master, 1135, 850)
        self.app.tela_inicio()

if __name__ == '__main__':
    app = Login(root)
    root.mainloop()
