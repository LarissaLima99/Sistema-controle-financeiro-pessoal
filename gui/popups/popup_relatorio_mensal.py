import tkinter as tk
import os
from tkinter import messagebox
from src.movimentacoes import meses_disponiveis, dados_relatorio_mensal
from gui.popups.gerar_relatorio import gerar_relatorio_mensal_pdf

# Popup para gerar relatório mensal
def abrir_popup_relatorio_mensal(master):
    popup = tk.Toplevel(master)
    popup.title("Relatório mensal")
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

    meses = meses_disponiveis()

    if not meses:
        messagebox.showinfo(
            "Sem relatórios",
            "Ainda não há meses fechados com movimentações."
        )
        popup.destroy()
        return

    # Inserção dos meses
    for mes in meses:
        ano, mes_num = mes.split("-")
        nomes_meses = [
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        lista.insert("end", f"{nomes_meses[int(mes_num)-1]} / {ano}")

    # Gerar relatório ao clicar no botão
    def gerar():
        sel = lista.curselection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um mês.")
            return

        mes_index = sel[0]
        ano_mes = meses[mes_index]

        movimentacoes = dados_relatorio_mensal(ano_mes)

        pasta = "relatorios"
        os.makedirs(pasta, exist_ok=True)

        caminho = os.path.join(
            pasta,
            f"relatorio_{ano_mes}.pdf"
        )

        gerar_relatorio_mensal_pdf(movimentacoes, caminho)

        messagebox.showinfo(
            "Relatório gerado",
            f"Relatório {ano_mes} gerado com sucesso. Clique em OK para abrir."
        )

        os.startfile(caminho)
        popup.destroy()

    # Botão gerar
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


