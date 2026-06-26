import tkinter as tk

from gui.telas.frame_principal import TelaPrincipal
from gui.telas.frame_movimentacoes import TelaMovimentacoes
from gui.telas.frame_relatorios import TelaRelatorios

# Classe principal da aplicação, responsável por gerenciar as telas e a navegação entre elas
class App(tk.Tk):
    def __init__(self):
        # Inicializa a janela principal da aplicação
        super().__init__()

        #titulo da janela
        self.title("Controle Financeiro")

        #centraliza a janela na tela
        self.centralizar_janela(600, 500)
        self.resizable(False, False)
        
        self.frames = {
            "principal": TelaPrincipal(self),
            "movimentacoes": TelaMovimentacoes(self),
            "relatorios": TelaRelatorios(self),
        }

        # Posiciona todas as telas no mesmo local, para que possam ser alternadas usando tkraise()
        for frame in self.frames.values():
            frame.place(relwidth=1, relheight=1)

        self.mostrar_tela("principal")
    
    def mostrar_tela(self, nome):
        self.frames[nome].tkraise()

    # Função para centralizar a janela na tela, recebendo a largura e altura desejadas como parâmetros
    def centralizar_janela(self, largura, altura):
        self.update_idletasks()

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{x}+{y}")