import sys
import os

# Garantir que o diretório base do projeto esteja no sys.path para evitar problemas de importação
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from data.connection import inicializar_banco
from gui.app import App


def main():
    # Inicializa o banco de dados 
    inicializar_banco()
    # Inicia a aplicação GUI
    app = App() 
    # Mantém a aplicação rodando    
    app.mainloop()


if __name__ == "__main__":
    main()