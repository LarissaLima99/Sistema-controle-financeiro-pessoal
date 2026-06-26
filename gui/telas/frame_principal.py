import tkinter as tk
from gui.popups.popup_nova_movimentacao import abrir_popup_nova_movimentacao
from src.movimentacoes import saldo
from src.movimentacoes import renovar_salario

# Tela principal da aplicação
class TelaPrincipal(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#121212")
        self.pack(fill="both", expand=True)


        # ==========================
        # CARD CENTRAL
        # ==========================
        card = tk.Frame(
            self, 
            bg="#1a1919", 
            padx=40, 
            pady=30
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # ==========================
        # TÍTULO
        # ==========================
        tk.Label(
            card,
            text="Menu Principal",
            font=("Arial", 18, "bold"),
            bg="#1e1e1e",
            fg="white"
        ).grid(row=0, column=0, pady=(0, 25))

        # ==========================
        # BOTÕES
        # ==========================
        tk.Button(
            card,
            text="Movimentações",
            font=("Arial", 12, "bold"),
            bg="#0C4E3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: master.mostrar_tela("movimentacoes")
        ).grid(row=1, column=0, sticky="ew", pady=10)

        tk.Button(
            card,
            text="Relatórios",
            font=("Arial", 12, "bold"),
            bg="#005b97",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: master.mostrar_tela("relatorios")
        ).grid(row=2, column=0, sticky="ew", pady=10)

        tk.Button(
            card,
            text="Renovar Salário",
            font=("Arial", 12, "bold"),
            bg="#949700",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.confirmar_renovacao_salario
        ).grid(row=3, column=0, sticky="ew", pady=10)

        tk.Button(
            card,
            text="Ver saldo",
            font=("Arial", 12, "bold"),
            bg="#444444",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.on_ver_saldo
        ).grid(row=4, column=0, sticky="ew", pady=10)

        # mensagem para exbir o saldo
        self.lbl_mensagem = tk.Label(
            card,
            text="",
            fg="#f1c40f",
            bg="#1e1e1e",
            font=("Arial", 10, "italic")
        )
        self.lbl_mensagem.grid(row=5, column=0, pady=(15, 0))

        card.columnconfigure(0, weight=1)

    #valida o saldo atual e exibe a mensagem correspondente
    def on_ver_saldo(self):
        saldo_atual = saldo()

        if saldo_atual != 0:
            self.lbl_mensagem.config(
                text=f"Saldo atual: R$ {saldo_atual:.2f}"
            )
        else:
            self.lbl_mensagem.config(
                text="Nenhuma movimentação registrada ainda."
            )
            
    #renovação do salário
    def confirmar_renovacao_salario(self):
        modal = tk.Toplevel(self)
        modal.title("Confirmar Renovação")
        modal.geometry("500x300")
        modal.configure(bg="#1c1c1c")
        modal.transient(self.master)
        modal.grab_set()
        modal.update_idletasks()

        largura = 500
        altura = 300

        x_pai = self.master.winfo_x()
        y_pai = self.master.winfo_y()
        w_pai = self.master.winfo_width()
        h_pai = self.master.winfo_height()

        # cálculo do centro
        x = x_pai + (w_pai // 2) - (largura // 2)
        y = y_pai + (h_pai // 2) - (altura // 2)

        modal.geometry(f"{largura}x{altura}+{x}+{y}")

        tk.Label(
            modal,
            text="Tem certeza que deseja renovar o salário?",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#1c1c1c",
            wraplength=460,
            justify="center"
        ).pack(pady=(25, 10))


        tk.Label(
            modal,
            text=(
                "Caso o salário tenha sido alterado, insira uma nova movimentação "
                "com o valor atualizado ao invés de renovar o salário."
            ),
            font=("Segoe UI", 10),
            fg="#f1c40f",
            bg="#1c1c1c",
            wraplength=460,
            justify="center"

        ).pack(pady=(0, 25))

        # Frame dos botões
        frame_botoes = tk.Frame(modal, bg="#1c1c1c")
        frame_botoes.pack(pady=5)

        tk.Button(
            frame_botoes,
            text="Sim, renovar",
            bg="#1e7f63",
            fg="white",
            activebackground="#16614c",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=16,
            height=2,
            cursor="hand2",
            command=lambda: self.executar_renovacao(modal)
        ).grid(row=0, column=0, padx=12)

        tk.Button(
            frame_botoes,
            text="Cancelar",
            bg="#3a3a3a",
            fg="white",
            activebackground="#2c2c2c",
            activeforeground="white",
            font=("Segoe UI", 10),
            relief="flat",
            width=16,
            height=2,
            cursor="hand2",
            command=modal.destroy
        ).grid(row=0, column=1, padx=12)


        #Botão Nova Movimentação
        tk.Button(
            modal,
            text="Inserir Nova Movimentação",
            bg="#949700",
            fg="white",
            #activebackground="#004570",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=34,
            height=2,
            cursor="hand2",
            command=lambda: abrir_popup_nova_movimentacao(modal)
        ).pack(pady=(20, 10))
    
    #executa a renovação do salário
    def executar_renovacao(self, modal):
        mensagem = renovar_salario()
        modal.destroy()

        self.lbl_mensagem.config(
            text=mensagem[0] if mensagem else "Salário renovado com sucesso."
        )

