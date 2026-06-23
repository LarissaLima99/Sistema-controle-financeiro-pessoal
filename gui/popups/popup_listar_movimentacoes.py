import tkinter as tk
from datetime import date
from datetime import datetime, date
from tkinter import ttk
from src.movimentacoes import mostrar_movimentacoes

# Popup para listar todas as movimentações
def abrir_popup_listar(master):
    popup = tk.Toplevel(master)
    popup.title("Movimentações")
    popup.geometry("700x400")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    # Centralizar
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (1000 // 2)
    y = (popup.winfo_screenheight() // 2) - (900 // 2)
    popup.geometry(f"1000x900+{x}+{y}")

    # =========================
    # TÍTULO
    # =========================
    tk.Label(
        popup,
        text="Lista de Movimentações",
        bg="#1e1e1e",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    # =========================
    # TABELA
    # =========================
    frame = tk.Frame(popup, bg="#1e1e1e")
    frame.pack(fill="both", expand=True, padx=20)

    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview",
        background="#121212",
        foreground="white",
        fieldbackground="#121212",
        relief="solid",
        rowheight=30,
        borderwidth=3
    )
    style.map("Treeview", background=[("selected", "#0C4E3C")])
    
    #style.map("Treeview.Heading",relief=[("active", "flat"), ("pressed", "flat")])


    style.configure(
        "Treeview.Heading",
        background="#1e1e1e",
        foreground="white",
        font=("Arial", 12, "bold"),        
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        padding=(8, 8)
    )

    tree = ttk.Treeview(
        frame,
        columns=("id", "data", "origem", "valor", "descricao"),
        show="headings"
    )

    # Cabeçalho da tabela
    tree.heading("data", text="Data",)
    tree.heading("origem", text="Origem")
    tree.heading("valor", text="Valor")
    tree.heading("descricao", text="Descrição")
    tree.pack(padx=10, pady=10)



    # Colunas 
    tree.column("id", width=0, stretch=False)
    tree.column("data", width=90, anchor="center")
    tree.column("origem", width=150, anchor="center")
    tree.column("valor", width=100, anchor="center")
    tree.column("descricao", width=280, anchor="center")

    # Cores por tipo
    tree.tag_configure("ganho", foreground="#2ecc71")
    tree.tag_configure("despesa", foreground="#e74c3c")

    tree.pack(fill="both", expand=True)

    # Preencher dados
    movimentacoes = mostrar_movimentacoes()

    for mov in movimentacoes:
        id_mov = mov[0]
        data = mov[1]
        valor = mov[2]
        origem = mov[3]
        tipo = mov[4]
        descricao = mov[5]

        tag = "ganho" if tipo == "G" else "despesa"

        if isinstance(data, date):
            data_formatada = data.strftime("%d-%m-%Y")
        elif isinstance(data, str):
            try:
                data_formatada = datetime.fromisoformat(data).strftime("%d-%m-%Y")
            except ValueError:
                data_formatada = data
        else:
            data_formatada = ""

        
        try:
            valor_float = float(valor)
        except (TypeError, ValueError):
            valor_float = 0.0

        valor_formatado = (
            f"R$ {valor_float:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


        tree.insert(
            "",
            "end",
            values=(id_mov, data_formatada, origem, valor_formatado, descricao),
            tags=(tag,)
        )



    # =========================
    # BOTÃO FECHAR
    # =========================
    tk.Button(
        popup,
        text="Fechar",
        bg="#333333",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=20,
        pady=8,
        command=popup.destroy
    ).pack(pady=15)