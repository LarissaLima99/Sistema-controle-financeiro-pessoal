import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from src.movimentacoes import mostrar_movimentacoes, excluir_movimentacao

def abrir_popup_excluir(master):
    popup = tk.Toplevel(master)
    popup.title("Excluir movimentação")
    popup.geometry("1000x900")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    tk.Label(
        popup,
        text="Selecione uma movimentação para excluir",
        bg="#1e1e1e",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    frame_tabela = tk.Frame(popup, bg="#1e1e1e")
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#121212",
                    foreground="white",
                    fieldbackground="#121212",
                    rowheight=30)
    style.map("Treeview", background=[("selected", "#0C4E3C")])
    style.configure("Treeview.Heading",
                    background="#1e1e1e",
                    foreground="white",
                    font=("Arial", 12, "bold"),
                    relief="flat",
                    padding=(8, 8))

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

    # =========================
    # AGRUPAR POR MÊS
    # =========================
    movimentacoes = mostrar_movimentacoes()
    mov_por_mes = {}
    for mov in movimentacoes:
        data = mov[1]
        if isinstance(data, str):
            try:
                data = datetime.fromisoformat(data).date()
            except ValueError:
                continue
        mes_chave = data.strftime("%Y-%m")
        mov_por_mes.setdefault(mes_chave, []).append(mov)

    # inverter ordem: mais novos primeiro
    meses = sorted(mov_por_mes.keys(), reverse=True)
    indice_mes = 0  # começa no mais novo

    # Lista de meses em português
    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    # Label único para mostrar mês atual
    lbl_mes = tk.Label(
        popup,
        text="",
        bg="#1e1e1e",
        fg="white",
        font=("Arial", 12, "bold")
    )
    lbl_mes.pack(pady=5)

    # =========================
    # FUNÇÃO PARA ATUALIZAR TABELA
    # =========================
    def mostrar_mes(indice):
        tree.delete(*tree.get_children())
        mes_atual = meses[indice]

        ano_, mes_num = mes_atual.split("-")
        mes_extenso = f"{nomes_meses[int(mes_num)-1]} de {ano_}"
        lbl_mes.config(text=f"Movimentações de {mes_extenso}")

        for mov in mov_por_mes[mes_atual]:
            id_mov, data, valor, origem, tipo, descricao = mov
            if isinstance(data, date):
                data_fmt = data.strftime("%d-%m-%Y")
            else:
                try:
                    data_fmt = datetime.fromisoformat(data).strftime("%d-%m-%Y")
                except:
                    data_fmt = str(data)

            try:
                valor_float = float(valor)
            except:
                valor_float = 0.0

            valor_fmt = f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tag = "ganho" if tipo == "G" else "despesa"

            tree.insert("", "end", values=(id_mov, data_fmt, origem, valor_fmt, descricao), tags=(tag,))

    # =========================
    # BOTÕES DE NAVEGAÇÃO
    # =========================
    nav_frame = tk.Frame(popup, bg="#1e1e1e")
    nav_frame.pack(pady=10)

    def anterior():
        nonlocal indice_mes
        if indice_mes < len(meses) - 1:  # vai para mais antigo
            indice_mes += 1
            mostrar_mes(indice_mes)

    def proximo():
        nonlocal indice_mes
        if indice_mes > 0:  # volta para mais novo
            indice_mes -= 1
            mostrar_mes(indice_mes)

    tk.Button(
        nav_frame, 
        text="←", 
        command=proximo,
        bg="#333333", 
        fg="white", 
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(side="left", padx=10)

    tk.Button(
        nav_frame, 
        text="→", 
        command=anterior,
        bg="#333333", 
        fg="white", 
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(side="left", padx=10)

    # Mostrar primeiro mês (mais novo)
    mostrar_mes(indice_mes)

    # =========================
    # BOTÕES DE AÇÃO
    # =========================
    frame_botoes = tk.Frame(popup, bg="#1e1e1e")
    frame_botoes.pack(pady=15)

    def confirmar_exclusao():
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma movimentação para excluir")
            return

        valores = tree.item(selecionado)["values"]
        id_mov = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir a movimentação ID {id_mov}?"
        )

        if confirmar:
            excluir_movimentacao(id_mov)

            # Remove direto da Treeview sem esperar atualizar
            tree.delete(selecionado)

            # Limpa a seleção para evitar inconsistência
            tree.selection_remove(selecionado)

            # Se quiser, ainda pode recarregar o mês para refletir o banco
            mostrar_mes(indice_mes)


    tk.Button(
        frame_botoes, 
        text="Excluir", 
        bg="#8e2a2a", 
        fg="white",
        font=("Arial", 10, "bold"), relief="flat",
        padx=15, pady=6, command=confirmar_exclusao
        ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes, 
        text="Cancelar", 
        bg="#333333", 
        fg="white",
        font=("Arial", 10), relief="flat",
        padx=15, pady=6, command=popup.destroy
        ).pack(side="left", padx=10)
