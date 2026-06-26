import tkinter as tk
from gui.popups.popup_relatorio_ganhos import abrir_popup_relatorio_ganhos
from gui.popups.popup_relatorio_mensal import abrir_popup_relatorio_mensal
from gui.popups.popup_relatorio_despesas import abrir_popup_relatorio_despesas

# Tela de relatórios
class TelaRelatorios(tk.Frame):
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
            text="Relatórios",
            font=("Arial", 18, "bold"),
            bg="#1e1e1e",
            fg="white"            
        ).grid(row=0, column=0, pady=(0, 25))

        # ==========================
        # BOTÕES
        # ==========================
        tk.Button(
        card,
        text="Relatório mensal",
        font=("Arial", 12, "bold"),
        bg="#005b97",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
        command=lambda: abrir_popup_relatorio_mensal(self)
        ).grid(row=1, column=0, sticky="ew", pady=10)

        tk.Button(
            card,
            text="Ganhos",
            font=("Arial", 10, "bold"),
            bg="#005b97",
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
            command=lambda: abrir_popup_relatorio_ganhos(self)
        ).grid(row=2, column=0, sticky="ew", pady=6)

        tk.Button(
            card,
            text="Despesas",
            font=("Arial", 10, "bold"),
            bg="#005b97",
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
            command=lambda: abrir_popup_relatorio_despesas(self)
        ).grid(row=3, column=0, sticky="ew", pady=6)

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