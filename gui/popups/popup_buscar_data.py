import tkinter as tk

from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
from gui.popups import popup_movimentacoes_dia

# Popup para buscar movimentações por data
def movimentacoes_por_data(self):
        popup = tk.Toplevel(self)
        popup.title("Selecionar data")
        popup.geometry("350x250")
        popup.configure(bg="#1e1e1e")
        popup.grab_set()  # trava foco no popup

        # Centralizar popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup.winfo_screenheight() // 2) - (350 // 2)
        popup.geometry(f"400x350+{x}+{y}")

        # Título
        tk.Label(
            popup,
            text="Informe a data",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=(30, 20))

        # Campo de entrada de data com calendário        
        entry_data = DateEntry(
            popup,
            locale='pt_BR',
            showweeknumbers=False,
            font=("Arial", 11),
            date_pattern="dd/MM/yyyy",
            justify="center",
            background="#282929",         
        )
        entry_data.pack(pady=10)        

        # Botão confirmar
        tk.Button(
            popup,
            text="Buscar",
            bg="#0C4E3C",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=lambda: confirmar_data(self, entry_data.get(), popup)
        ).pack(pady=50)

# Função para validar a data e abrir o popup de movimentações do dia
def confirmar_data(self, data_informada, popup):
    try:
        data_iso = datetime.strptime(
            data_informada, "%d/%m/%Y"
        ).strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Erro",
            "Data inválida. Use o calendário."
        )
        return

    # fecha o popup de seleção de data
    popup.destroy()

    # abrir o popup de movimentações do dia, passando a data selecionada
    popup_movimentacoes_dia.abrir_popup_movimentacoes_dia(self, data_iso)

