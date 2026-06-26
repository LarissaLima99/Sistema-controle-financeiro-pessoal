import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from src.movimentacoes import nova_movimentacao

# Popup para nova movimentação
def abrir_popup_nova_movimentacao(master):
    popup = tk.Toplevel(master)
    popup.title("Nova movimentação")
    popup.geometry("500x400")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    # Centralizar
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (500 // 2)
    y = (popup.winfo_screenheight() // 2) - (400 // 2)
    popup.geometry(f"500x400+{x}+{y}")

    # =========================
    # TÍTULO
    # =========================
    tk.Label(
        popup,
        text="Nova Movimentação",
        font=("Arial", 14, "bold"),
        bg="#1e1e1e",
        fg="white"
    ).pack(pady=15)

    # =========================
    # DATA
    # =========================
    tk.Label(popup, text="Data *", bg="#1e1e1e", fg="white").pack(anchor="w", padx=40)

    entry_data = DateEntry(
        popup,
        locale='pt_BR',
        showweeknumbers=False,
        font=("Arial", 11),
        date_pattern="dd/MM/yyyy",        
        background="#282929"
    )
    entry_data.pack(padx=40, pady=5, fill="x")

    # =========================
    # TIPO (G / D)
    # =========================
    tk.Label(popup, text="Tipo *", bg="#1e1e1e", fg="white").pack(anchor="w", padx=40, pady=(10, 0))

    tipo_var = tk.StringVar(value="D")

    frame_tipo = tk.Frame(popup, bg="#1e1e1e")
    frame_tipo.pack(padx=40, pady=5)

    tk.Radiobutton(
        frame_tipo,
        text="Ganho",
        variable=tipo_var,
        value="G",
        fg="#2ecc71",
        bg="#1e1e1e",
        selectcolor="#121212",
        activebackground="#1e1e1e"
    ).pack(side="left", padx=10)

    tk.Radiobutton(
        frame_tipo,
        text="Despesa",
        variable=tipo_var,
        value="D",
        fg="#e74c3c",
        bg="#1e1e1e",
        selectcolor="#121212",
        activebackground="#1e1e1e"
    ).pack(side="left", padx=10)

    # =========================
    # VALOR
    # =========================
    tk.Label(popup, text="Valor *", bg="#1e1e1e", fg="white").pack(anchor="w", padx=40)
    entry_valor = tk.Entry(popup)
    entry_valor.pack(padx=40, pady=5, fill="x")

    # =========================
    # ORIGEM
    # =========================
    tk.Label(popup, text="Origem *", bg="#1e1e1e", fg="white").pack(anchor="w", padx=40)
    entry_origem = tk.Entry(popup)
    entry_origem.pack(padx=40, pady=5, fill="x")

    # =========================
    # DESCRIÇÃO
    # =========================
    tk.Label(popup, text="Descrição", bg="#1e1e1e", fg="white").pack(anchor="w", padx=40)
    entry_desc = tk.Entry(popup)
    entry_desc.pack(padx=40, pady=5, fill="x")

    # =========================
    # SALVAR
    # =========================
    def salvar():
        tipo = tipo_var.get()
        data = entry_data.get()
        origem = entry_origem.get()
        descricao = entry_desc.get()

        valor_str = entry_valor.get().strip().replace(",", ".")

        if not valor_str or not origem:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios")
            return

        try:
            valor_float = float(valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")
            return

        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")

        #insere a movimentação no banco de dados
        nova_movimentacao(tipo, data_formatada, valor_float, origem, descricao)

        messagebox.showinfo("Sucesso", "Movimentação cadastrada")
        popup.destroy()

    # ==========================
    # BOTÕES
    # ==========================
    frame_botoes = tk.Frame(popup, bg="#1e1e1e")
    frame_botoes.pack(pady=20)

    tk.Button(
        frame_botoes,
        text="Salvar",
        bg="#0C4E3C",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        command=salvar
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes,
        text="Cancelar",
        bg="#333333",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        command=popup.destroy
    ).pack(side="left", padx=10)