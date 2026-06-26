import tkinter as tk
import os
from tkinter import messagebox
from src.movimentacoes import dados_relatorio_ganhos
from gui.popups.gerar_relatorio import gerar_relatorio_ganhos_anual

def abrir_popup_relatorio_ganhos(master):
    popup = tk.Toplevel(master)
    popup.title("Relatório Anual de Ganhos")
    popup.geometry("350x350")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    tk.Label(
        popup,
        text="Selecione o ano do relatório",
        bg="#1e1e1e",
        fg="white",
        font=("Arial", 13, "bold")
    ).pack(pady=15)

    movimentacoes = dados_relatorio_ganhos()
    if not movimentacoes:
        messagebox.showinfo("Sem ganhos", "Não há ganhos registrados.")
        popup.destroy()
        return

    # extrai apenas os anos
    anos = sorted({mov[1][:4] for mov in movimentacoes})

    lista = tk.Listbox(
        popup,
        font=("Arial", 11),
        height=10,
        bg="#2b2b2b",
        fg="white",
        selectbackground="#0C4E3C",
        selectforeground="white",
        relief="flat",
        activestyle="none"
    )
    lista.pack(padx=30, pady=10, fill="both", expand=True)

    for ano in anos:
        lista.insert("end", f"Ganhos de /{ano}")

    # função interna chamada pelo botão
    def gerar():
        sel = lista.curselection()
        if not sel:
            messagebox.showwarning(
                "Atenção", 
                "Selecione um ano.")
            return

        ano = anos[sel[0]]

        pasta = "relatorios"
        os.makedirs(pasta, exist_ok=True)

        caminho = os.path.join(pasta, f"ganhos_{ano}.pdf")

        gerar_relatorio_ganhos_anual(ano, caminho) 

        os.startfile(caminho)
        popup.destroy()

    tk.Button(
        popup,
        text="Gerar relatório",
        bg="#0C4E3C",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=20,
        pady=8,
        command=gerar
    ).pack(pady=(15, 20))

