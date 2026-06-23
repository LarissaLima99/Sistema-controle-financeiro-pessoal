import tkinter as tk
import os
from tkinter import messagebox
from src.movimentacoes import dados_relatorio_despesas
from gui.popups.gerar_relatorio import gerar_relatorio_despesas

# Popup para gerar relatório de despesas
def abrir_popup_relatorio_despesas(master):
    popup = tk.Toplevel(master)
    popup.title("Relatório de Despesas")
    popup.geometry("350x350")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    # Título
    tk.Label(
        popup,
        text="Selecione o mês do relatório",
        bg="#1e1e1e",
        fg="white",
        font=("Arial", 13, "bold")
    ).pack(pady=15)

    # Buscar TODAS as despesas
    movimentacoes = dados_relatorio_despesas()

    if not movimentacoes:
        messagebox.showinfo(
            "Sem despesas",
            "Não há despesas registradas."
        )
        popup.destroy()
        return

    # =========================
    # EXTRAIR MESES DIRETO DAS DESPESAS
    # =========================
    meses = sorted({mov[1][:7] for mov in movimentacoes})  # YYYY-MM

    frame_lista = tk.Frame(
        popup,
        bg="#2b2b2b",
        padx=10,
        pady=10
    )
    frame_lista.pack(padx=30, pady=10, fill="both", expand=True)

    # Listbox para mostrar os meses disponíveis
    lista = tk.Listbox(
        frame_lista,
        font=("Arial", 11),
        height=10,
        bg="#2b2b2b",
        fg="white",
        selectbackground="#0C4E3C",
        selectforeground="white",
        highlightthickness=0,
        relief="flat",
        activestyle="none"
    )
    lista.pack(fill="both", expand=True)

    # Converter meses para formato legível
    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    for mes in meses:
        ano, mes_num = mes.split("-")
        lista.insert("end", f"{nomes_meses[int(mes_num)-1]} / {ano}")

    #gerar relatório ao clicar no botão
    def gerar():
        sel = lista.curselection()
        if not sel:
            messagebox.showwarning(
                "Atenção",
                "Selecione um mês."
            )
            return

        ano_mes = meses[sel[0]]

        pasta = "relatorios"
        os.makedirs(pasta, exist_ok=True)

        caminho = os.path.join(
            pasta,
            f"despesas_{ano_mes}.pdf"
        )

       
        gerar_relatorio_despesas(ano_mes, caminho)
        
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
