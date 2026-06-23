from src import movimentacoes_repository
from datetime import date

#insere nova movimentação
def nova_movimentacao(tipo, data, valor, origem, descricao):
    return movimentacoes_repository.inserir_movimentacao(tipo, data, valor, origem, descricao)

#retorna todas as movimentações cadastradas
def mostrar_movimentacoes():
    return movimentacoes_repository.buscar_movimentacoes()

#retorna as movimentações da data passada como parâmetro
def movimentacoes_diaria(data):
    return movimentacoes_repository.buscar_movimentacoes_por_data(data)

#retorna as movimentações do mês/ano passado como parâmetro
def movimentacoes_mensal(mes):
    return movimentacoes_repository.buscar_movimentacoes_mes(mes)

#retorna o saldo atual
def saldo():
    return movimentacoes_repository.calcular_saldo()

#Função para renovar o salário e a bolsa automaticamente no início de cada mês, com base no ultimo valor cadastrado
def renovar_salario():
    ultimo_salario = movimentacoes_repository.pegar_ultimo_salario()
    ultima_bolsa = movimentacoes_repository.pegar_ultima_bolsa()

    if ultimo_salario is not None and ultima_bolsa is not None:
        nova_movimentacao("G", date.today().strftime('%Y-%m-%d'), ultimo_salario, "SALARIO", "Salário atualizado automaticamente.")
        nova_movimentacao("G", date.today().strftime('%Y-%m-%d'), ultima_bolsa, "BOLSA", "Bolsa atualizada automaticamente.")


#retorna os meses disponíveis com movimentações para gerar relatórios mensais
def meses_disponiveis():
    meses = movimentacoes_repository.listar_meses_disponiveis()
    mes_atual = date.today().strftime('%Y-%m')

    # relatório só pode ser gerado após fechar o mês
    meses_fechados = [m for m in meses if m < mes_atual]

    return meses_fechados

#retorna as movimentações do mês anterior para gerar o relatório mensal
def dados_relatorio_mensal(ano_mes):
    return movimentacoes_repository.buscar_movimentacoes_mes(ano_mes)

#retorna as movimentações do tipo "G" para gerar o relatório de ganhos
def dados_relatorio_ganhos():
    return movimentacoes_repository.buscar_movimentacoes_por_tipo("G")

#retorna as movimentações do tipo "D" para gerar o relatório de despesas
def dados_relatorio_despesas():
    return movimentacoes_repository.buscar_movimentacoes_por_tipo("D")

#exclui uma movimentação com base no id passado como parâmetro
def excluir_movimentacao(id):
    return movimentacoes_repository.deletar_movimentacao(id)

