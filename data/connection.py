import sqlite3
from pathlib import Path


def get_db_path():
    """
    Retorna o caminho persistente do banco de dados.
    O banco fica fora do .exe e não é apagado.
    """
    base_dir = Path.home() / "ControleFinanceiro"
    base_dir.mkdir(exist_ok=True)
    return base_dir / "database.db"


def conectar():
    return sqlite3.connect(get_db_path())


def conexao():
    return conectar()


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    #tabela principal MOVIMENTACOES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            valor DECIMAL(8, 2) NOT NULL,
            origem VARCHAR(100) NOT NULL,
            tipo CHAR(1) NOT NULL,
            descricao VARCHAR(255)
        );
    """)

    # índice por tipo
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_movimentacoes_tipo
        ON movimentacoes(tipo);
    """)

    #índice por data
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_movimentacoes_data
        ON movimentacoes(data);
    """)

    conn.commit()
    conn.close()