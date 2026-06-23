import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from src.movimentacoes import mostrar_movimentacoes, excluir_movimentacao

# Popup para excluir movimentações
def abrir_popup_excluir(master):
    popup = tk.Toplevel(master)
    popup.title("Excluir movimentação")
    popup.geometry("600x400")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    # Centralizar
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (1000 // 2)
    y = (popup.winfo_screenheight() // 2) - (900 // 2)
    popup.geometry(f"1000x900+{x}+{y}")

    # Título
    tk.Label(
        popup,
        text="Selecione uma movimentação para excluir",
        bg="#1e1e1e",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    # =========================
    # TABELA DE MOVIMENTAÇÕES
    # =========================
    frame_tabela = tk.Frame(popup, bg="#1e1e1e")
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=(0, 10))
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
        frame_tabela,
        columns=("id","data", "origem", "valor", "descricao"),
        show="headings"
    )

    tree.heading("data", text="Data")
    tree.heading("origem", text="Origem")
    tree.heading("valor", text="Valor")
    tree.heading("descricao", text="Descrição")

    tree.column("id", width=0, stretch=False)
    tree.column("data", width=90, anchor="center")
    tree.column("origem", width=150, anchor="center")
    tree.column("valor", width=100, anchor="center")
    tree.column("descricao", width=280, anchor="center")

    tree.tag_configure("ganho", foreground="#2ecc71")     
    tree.tag_configure("despesa", foreground="#e74c3c")   
    tree.pack(fill="both", expand=True)

    # Preencher a tabela
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
    # BOTÕES
    # =========================
    frame_botoes = tk.Frame(popup, bg="#1e1e1e")
    frame_botoes.pack(pady=15)

    # Função para confirmar exclusão
    def confirmar_exclusao():
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma movimentação para excluir"
            )
            return

        valores = tree.item(selecionado)["values"]
        id_mov = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir a movimentação ID {id_mov}?"
        )

        if confirmar:
            excluir_movimentacao(id_mov)
            popup.destroy()

    tk.Button(
        frame_botoes,
        text="Excluir",
        bg="#8e2a2a",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=6,
        command=confirmar_exclusao
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes,
        text="Cancelar",
        bg="#333333",
        fg="white",
        font=("Arial", 10),
        relief="flat",
        padx=15,
        pady=6,
        command=popup.destroy
    ).pack(side="left", padx=10)