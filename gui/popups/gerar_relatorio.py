from fpdf import FPDF
from datetime import date, datetime
from collections import defaultdict
from src.movimentacoes import dados_relatorio_despesas, dados_relatorio_ganhos
import os

try:
    import streamlit as st
except ImportError:
    st = None

################################# RELATORIO MENSAL ###############################################
def gerar_relatorio_mensal_pdf(movimentacoes, caminho):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # =========================
    # CABEÇALHO DO PDF
    # =========================
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Controle Financeiro", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Relatório de Movimentações", ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.cell(
        0,
        8,
        f"Gerado em: {date.today().strftime('%d/%m/%Y')}",
        ln=True
    )

    pdf.ln(5)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # =========================
    # CABEÇALHO DA TABELA
    # =========================    
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(235, 235, 235)

    pdf.cell(30, 8, "Data", border=1, align="C", fill=True)
    pdf.cell(50, 8, "Origem", border=1, fill=True)
    pdf.cell(30, 8, "Valor", border=1, align="R", fill=True)
    pdf.cell(150, 8, "Descrição", border=1, fill=True, ln=True)

    # =========================
    # DADOS
    # =========================
    pdf.set_font("Arial", "", 10)

    total_ganhos = 0
    total_despesas = 0

    for mov in movimentacoes:
        _, data_mov, valor, origem, tipo, descricao = mov

        #formata a data para exibir no relatório
        data_formatada = datetime.strptime(data_mov, "%Y-%m-%d").strftime("%d/%m/%Y")

        origem = origem or ""
        descricao = descricao or ""
        valor = float(valor)

        # caso seja um ganho imprimirá nesta formatação
        if tipo == "G":
            pdf.set_text_color(0, 150, 0)
            total_ganhos += valor
            # formata o valor para exibir no relatório
            valor_str = f"+ R$ {valor:.2f}"
        # caso seja uma despesa imprimirá nesta formatação
        else:
            pdf.set_text_color(180, 0, 0)
            total_despesas += abs(valor)
            # formata o valor para exibir no relatório
            valor_str = f"- R$ {abs(valor):.2f}"

        pdf.cell(30, 8, data_formatada, border=1)    
        pdf.cell(50, 8, origem[:25], border=1)    
        pdf.cell(30, 8, valor_str, border=1)
        pdf.cell(150, 8, descricao[:40], border=1, ln=True)

    pdf.set_text_color(0, 0, 0)

    # =========================
    # TOTAL DOS MÊS
    # =========================
    pdf.ln(8)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    saldo = total_ganhos - total_despesas

    LABEL_WIDTH = 40
    VALUE_WIDTH = 40

    pdf.set_font("Arial", "B", 11)

    # Total de ganhos
    pdf.set_text_color(180, 0, 0)
    pdf.cell(LABEL_WIDTH, 8, "Total de ganhos:")
    pdf.cell(
        VALUE_WIDTH,
        8,
        f"R$ {total_ganhos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        align="L",
        ln=True
    )

    # Total de despesas
    pdf.set_text_color(0, 150, 0)
    pdf.cell(LABEL_WIDTH, 8, "Total de despesas:")
    pdf.cell(
        VALUE_WIDTH,
        8,
        f"R$ {total_despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        align="L",
        ln=True
    )

    # Saldo final
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(LABEL_WIDTH, 10, "Saldo final:")

    if saldo >= 0:
        pdf.set_text_color(0, 150, 0)
    else:
        pdf.set_text_color(180, 0, 0)

    pdf.cell(
        VALUE_WIDTH,
        10,
        f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        align="L",
        ln=True
    )

    pdf.set_text_color(0, 0, 0)

    # =========================
    # SALVAR E ABRIR
    # =========================
    pdf.output(caminho) 

################################# RELATORIO GANHOS ###############################################
def gerar_relatorio_ganhos_anual(ano, caminho):
    movimentacoes = dados_relatorio_ganhos()

    # Filtra apenas movimentações do ano
    movimentacoes = [mov for mov in movimentacoes if mov[1].startswith(str(ano))]
    if not movimentacoes:
        print(f"Nenhum ganho encontrado para {ano}.")
        return

    # Agrupa por mês
    ganhos_por_mes = defaultdict(list)
    for mov in movimentacoes:
        _, data_mov, valor, origem, _, descricao = mov
        mes = data_mov[:7]  # YYYY-MM
        ganhos_por_mes[mes].append(mov)

    pdf = FPDF()
    pdf.set_auto_page_break(True, 15)
    pdf.add_page()

    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    # Cabeçalho principal
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Controle Financeiro", ln=True)
    pdf.set_font("Arial", "", 13)
    pdf.cell(0, 8, f"Relatório Anual de Ganhos - {ano}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Gerado em: {date.today().strftime('%d/%m/%Y')}", ln=True)
    
    pdf.ln(6)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    total_anual = 0.0

    # Itera sobre os meses em ordem
    for mes in sorted(ganhos_por_mes.keys()):
        ano_, mes_num = mes.split("-")
        mes_extenso = f"{nomes_meses[int(mes_num)-1]} de {ano_}"

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, mes_extenso, ln=True)

        # Cabeçalho da tabela
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(30, 8, "Data", fill=True)
        pdf.cell(50, 8, "Origem", fill=True)
        pdf.cell(30, 8, "Valor", fill=True)
        pdf.cell(150, 8, "Descrição", fill=True, ln=True)

        subtotal = 0.0
        pdf.set_font("Arial", "", 10)

        for _, data_mov, valor, origem, _, descricao in ganhos_por_mes[mes]:
            data_fmt = datetime.strptime(data_mov, "%Y-%m-%d").strftime("%d/%m/%Y")
            valor = float(valor)
            subtotal += valor
            total_anual += valor

            valor_str = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            pdf.cell(30, 8, data_fmt)
            pdf.cell(50, 8, origem[:30])
            pdf.set_text_color(0, 150, 0)
            pdf.cell(30, 8, valor_str)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(150, 8, descricao[:40], ln=True)

        # Subtotal do mês
        pdf.ln(4)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(80, 8, f"Subtotal de {mes_extenso}:")
        pdf.set_text_color(0, 150, 0)
        pdf.cell(30, 8, f"R$ {subtotal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(6)

    # Total anual
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, f"Total de Ganhos em {ano}:")
    pdf.set_text_color(0, 150, 0)
    pdf.cell(30, 10, f"R$ {total_anual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)

    pdf.output(caminho)


################################# RELATORIO DESPESAS ###############################################
def gerar_relatorio_despesas(ano_mes, caminho):
    #pegando os dados de despesas 
    movimentacoes = dados_relatorio_despesas()

    #FILTRA O MÊS
    movimentacoes = [
        mov for mov in movimentacoes
        if mov[1].startswith(ano_mes)
    ]

    if not movimentacoes:
        print("Nenhuma despesa encontrada para este mês.")
        return

    #agrupa as movimentações por origem para organizar o relatório por categorias
    mov_por_origem = defaultdict(list)
    for mov in movimentacoes:
        mov_por_origem[mov[3]].append(mov)

    #gerar o PDF do relatório
    pdf = FPDF()
    pdf.set_auto_page_break(True, 15)
    pdf.add_page()

    #formata o mês e ano para exibir no relatório
    ano, mes = ano_mes.split("-")
    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes_extenso = f"{nomes_meses[int(mes)-1]} / {ano}"

    # =========================
    # CABEÇALHO DO PDF
    # =========================
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Controle Financeiro", ln=True)

    pdf.set_font("Arial", "", 13)
    pdf.cell(0, 8, f"Relatório de Despesas - {mes_extenso}", ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Gerado em: {date.today().strftime('%d/%m/%Y')}", ln=True)

    pdf.ln(6)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # =========================
    # CABEÇALHO DA TABELA 
    # =========================
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 10)

    pdf.cell(50, 8, "Data", fill=True)
    pdf.cell(50, 8, "Valor", fill=True)
    pdf.cell(150, 8, "Descrição", fill=True, ln=True)

    total_geral = 0.0

    # =========================
    # DADOS 
    # =========================
    for origem, itens in mov_por_origem.items():
        pdf.ln(6)

        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, f"{origem}", ln=True)

        subtotal = 0.0
        pdf.set_font("Arial", "", 10)

        for mov in itens:
            _, data_mov, valor, _, _, descricao = mov

            #formata a data para exibir no relatório
            data_fmt = datetime.strptime(
                data_mov, "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            valor = float(valor)
            subtotal += valor
            total_geral += valor

            # formata o valor para exibir no relatório
            valor_str = (
                f"R$ {valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            pdf.set_text_color(0, 0, 0)
            pdf.cell(50, 8, data_fmt, align="L")
            pdf.set_text_color(200, 0, 0)
            pdf.cell(50, 8, valor_str, align="L")
            pdf.set_text_color(0, 0, 0)
            pdf.cell(150, 8, descricao or "", align="L", ln=True)

        # Subtotal
        pdf.ln(2)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(100, 8, f"Subtotal")

        pdf.set_text_color(200, 0, 0)
        pdf.cell(
            150,
            8,
            f"R$ {subtotal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            align="L",
            ln=True
        )

        y = pdf.get_y()
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, y, 200, y)
        pdf.ln(6)

    # =========================
    # TOTAL DO MÊS
    # =========================
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(100, 10, f"Total de Despesas em {mes_extenso}:")

    pdf.set_text_color(200, 0, 0)
    pdf.cell(
        150,
        10,
        f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        align="L",
        ln=True
    )

    # =========================
    # SALVAR E ABRIR
    # =========================
    pdf.output(caminho)



