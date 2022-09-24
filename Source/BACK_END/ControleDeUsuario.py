from tkinter import Tk
import BACK_END.Pastas as pt
import BACK_END.UsuarioDAO as usdao

root = Tk()
banco = usdao.UsuarioDAO
usuarios = banco.ler_dados()
print(usuarios)