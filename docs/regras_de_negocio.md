# Regras de Negócio – Sistema de Controle Financeiro Pessoal

## Funcionalidades do sistema
- Inserir novas movimentação financeiras
- Listar todas as movimentações cadastradas
- Listar movimentações por data
- Listar movimentações do dia atual
- Deletar movimentação 
- Consultar saldo atual
- Gerar relatório geral mensal
- Gerar relatório anual de ganhos
- Gerar relatório mensal de despesas

## Regras de movimentação
- O tipo da movimentação deve ser:
  - `G` para ganhos
  - `D` para despesas
- A data de inserção é preenchida automaticamente com a data atual
- O valor deve ser um número válido (aceita ponto ou vírgula como separador decimal)
- A origem é um campo obrigatório para a movimentação
- A descrição é opcional
- O registro é salvo na tabela `movimentacoes` com os campos:
  - `tipo`
  - `data`
  - `valor`
  - `origem`
  - `descricao`

## Regras de saldo
- O saldo atual é calculado como:
  - `soma dos ganhos` menos `soma das despesas`
- O saldo diário considera todas as movimentações com data menor ou igual à data informada