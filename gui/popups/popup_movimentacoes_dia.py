import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
from tkinter import messagebox
from src.movimentacoes import movimentacoes_diaria

# Popup para mostrar movimentações do dia selecionado
def abrir_popup_movimentacoes_dia(master, data):
    popup = tk.Toplevel(master)
    popup.title("Movimentações do dia")
    popup.geometry("700x400")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    # Centralizar
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (700 // 2)
    y = (popup.winfo_screenheight() // 2) - (400 // 2)
    popup.geometry(f"700x400+{x}+{y}")

    # =========================
    # TÍTULO
    # =========================
    tk.Label(
        popup,
        text=f"Movimentações do dia",
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
        rowheight=30,
        borderwidth=3
    )
    style.map("Treeview", background=[("selected", "#0C4E3C")])

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
    tree.heading("data", text="Data")
    tree.heading("origem", text="Origem")
    tree.heading("valor", text="Valor")
    tree.heading("descricao", text="Descrição")

    # Colunas (ID oculto)
    tree.column("id", width=0, stretch=False)
    tree.column("data", width=90, anchor="center")
    tree.column("origem", width=150, anchor="center")
    tree.column("valor", width=100, anchor="center")
    tree.column("descricao", width=280, anchor="center")

    # Cores por tipo
    tree.tag_configure("ganho", foreground="#2ecc71")
    tree.tag_configure("despesa", foreground="#e74c3c")

    tree.pack(fill="both", expand=True)

    # =========================
    # DADOS
    # =========================
    dados = movimentacoes_diaria(data)

    if not dados:
        messagebox.showinfo(
            "Sem movimentações",
            "Nenhuma movimentação encontrada para esta data."
        )
        popup.destroy()
        return

    for mov in dados:
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

        valor_float = float(valor)
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