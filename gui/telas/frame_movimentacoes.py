import tkinter as tk
from datetime import date
from gui.popups.popup_excluir import abrir_popup_excluir
from gui.popups.popup_buscar_data import movimentacoes_por_data
from gui.popups.popup_listar_movimentacoes import abrir_popup_listar
from gui.popups.popup_nova_movimentacao import abrir_popup_nova_movimentacao
from gui.popups.popup_movimentacoes_dia import abrir_popup_movimentacoes_dia

# Tela de movimentações
class TelaMovimentacoes(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#121212")
        self.pack(fill="both", expand=True)

        # ==========================
        # CARD CENTRAL
        # ==========================
        card = tk.Frame(
            self,
            bg="#1e1e1e",
            padx=40,
            pady=30
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Tornar responsivo
        card.columnconfigure(0, weight=1)

        # ==========================
        # TÍTULO
        # ==========================
        tk.Label(
            card,
            text="Movimentações",
            font=("Arial", 18, "bold"),
            bg="#1e1e1e",
            fg="white"
        ).grid(row=0, column=0, pady=(0, 25))

        # ==========================
        # BOTÕES
        # ==========================
        tk.Button(
            card,
            text="Nova movimentação",
            font=("Arial", 11, "bold"),
            bg="#0C4E3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: abrir_popup_nova_movimentacao(self)
        ).grid(row=1, column=0, sticky="ew", pady=6)

        tk.Button(
            card,
            text="Movimentações do dia",
            font=("Arial", 11, "bold"),
            bg="#0C4E3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: abrir_popup_movimentacoes_dia(self, date.today().strftime("%Y-%m-%d"))
        ).grid(row=2, column=0, sticky="ew", pady=6)

        tk.Button(
            card,
            text="Movimentações por data",
            font=("Arial", 11, "bold"),
            bg="#0C4E3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: movimentacoes_por_data(self)
        ).grid(row=3, column=0, sticky="ew", pady=6)

        tk.Button(
            card,
            text="Listar movimentações",
            font=("Arial", 11, "bold"),
            bg="#0C4E3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: abrir_popup_listar(self)
        ).grid(row=4, column=0, sticky="ew", pady=6)

        tk.Button(
            card,
            text="Excluir movimentação",
            font=("Arial", 11, "bold"),
            bg="#8e2a2a",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: abrir_popup_excluir(self)
        ).grid(row=5, column=0, sticky="ew", pady=6)

        tk.Button(
            card,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
            command=lambda: master.mostrar_tela("principal")
        ).grid(row=6, column=0, sticky="ew", pady=(20, 0))
