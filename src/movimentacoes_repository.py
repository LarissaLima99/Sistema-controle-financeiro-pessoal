from data.connection import conexao

#inserir uma nova movimentação no banco de dados
def inserir_movimentacao(tipo, data, valor, origem, descricao):
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """ 
            INSERT INTO movimentacoes (
                data,
                valor,
                origem,
                tipo,
                descricao
            ) VALUES (?, ?, UPPER(?), UPPER(?), ?)
        """

        cursor.execute(sql, (data, valor, origem, tipo, descricao))
        conn.commit() 

#buscar todas as movimentações do banco de dados
def buscar_movimentacoes():
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """ 
        SELECT id, data, valor, origem, tipo, descricao FROM movimentacoes
        ORDER BY data DESC
        """
        

        cursor.execute(sql)
        return cursor.fetchall()
    
#buscar movimentações por tipo (ganhos ou despesas)
def buscar_movimentacoes_por_tipo(tipo):
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """ 
        SELECT id, data, valor, origem, tipo, descricao FROM movimentacoes 
        WHERE tipo = ?
        """

        cursor.execute(sql,(tipo,))
        return cursor.fetchall()
    
#buscar movimentações por data
def buscar_movimentacoes_por_data(data):    
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """ 
        SELECT id, data, valor, origem, tipo, descricao FROM movimentacoes
        WHERE data = ?
        ORDER BY data DESC
        """

        cursor.execute(sql,(data,))
        return cursor.fetchall()
    
def buscar_movimentacoes_mes(mes):
    with conexao() as conn:
        cursor = conn.cursor()
        
        sql = """
            SELECT id, data, valor, origem, tipo, descricao
            FROM movimentacoes
            WHERE strftime('%Y-%m', data) = ?
            ORDER BY data
        """

        cursor.execute(sql,(mes,))
        return cursor.fetchall()

#saldo atual calculado
def calcular_saldo():
    with conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN tipo = 'G' THEN valor ELSE 0 END), 0) -
                    COALESCE(SUM(CASE WHEN tipo = 'D' THEN valor ELSE 0 END), 0)
            FROM movimentacoes
            """)
            resultado = cursor.fetchone()
            return resultado[0] if resultado and resultado[0] is not None else 0

    
#pega o utimo salário registrado para sugerir o valor na renovação do salário
def pegar_ultimo_salario():
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """
        SELECT valor FROM movimentacoes
        WHERE tipo = 'G' AND origem = 'SALARIO'
        ORDER BY id DESC LIMIT 1;

        """
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0] if result is not None else None

#pega o ultimo valor da bolsa registrado para sugerir o valor na renovação da bolsa  
def pegar_ultima_bolsa():
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """
        SELECT valor FROM movimentacoes
        WHERE tipo = 'G' AND origem = 'BOLSA'
        ORDER BY id DESC LIMIT 1;

        """
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0] if result is not None else None

#deletar uma movimentação do banco de dados
def deletar_movimentacao(id):
    with conexao() as conn:
        cursor = conn.cursor()

        sql = """ 
        DELETE FROM movimentacoes
        WHERE id = ?
        """

        cursor.execute(sql, (id,))
        conn.commit()

#listar meses disponíveis para relatório mensal, considerando apenas meses anteriores ao mês atual para garantir que o relatório só seja gerado após fechar o mês
def listar_meses_disponiveis():
    with conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT strftime('%Y-%m', data) AS ano_mes
            FROM movimentacoes
            ORDER BY ano_mes DESC
        """)
        return [row[0] for row in cursor.fetchall()]
        

#buscar movimentações de um mês específico
def buscar_movimentacoes_mes(ano_mes):
    with conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, data, valor, origem, tipo, descricao
            FROM movimentacoes
            WHERE strftime('%Y-%m', data) = ?
            ORDER BY data
        """, (ano_mes,))
        return cursor.fetchall()



