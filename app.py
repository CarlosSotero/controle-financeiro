import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

ARQUIVO = "controle_gastos.xlsx"

def obter_mes_atual():
    return datetime.now().strftime('%Y-%m')

def inicializar_planilha():
    mes_atual = obter_mes_atual()
    if not os.path.exists(ARQUIVO):
        df = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Forma", "Cartão"])
        df.to_excel(ARQUIVO, index=False, sheet_name=mes_atual)
        return df
    try:
        return pd.read_excel(ARQUIVO, sheet_name=mes_atual)
    except Exception:
        df = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Forma", "Cartão"])
        with pd.ExcelWriter(ARQUIVO, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=mes_atual, index=False)
        return df

def salvar_df(df):
    mes_atual = obter_mes_atual()
    with pd.ExcelWriter(ARQUIVO, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=mes_atual, index=False)

def registrar_entrada(tipo_receita, valor):
    try:
        df = inicializar_planilha()
        nova_entrada = {
            "Data": datetime.now().strftime('%Y-%m-%d'),
            "Tipo": "Receita",
            "Categoria": tipo_receita,
            "Valor": valor,
            "Forma": "",
            "Cartão": ""
        }
        df = pd.concat([df, pd.DataFrame([nova_entrada])], ignore_index=True)
        salvar_df(df)
        return "✅ Receita registrada com sucesso!"
    except Exception as e:
        return f"Erro: {str(e)}"

def registrar_gasto(valor, forma, categoria, cartao):
    try:
        df = inicializar_planilha()
        novo_gasto = {
            "Data": datetime.now().strftime('%Y-%m-%d'),
            "Tipo": "Despesa",
            "Categoria": categoria,
            "Valor": valor,
            "Forma": forma,
            "Cartão": cartao if forma == "Crédito" else ""
        }
        df = pd.concat([df, pd.DataFrame([novo_gasto])], ignore_index=True)
        salvar_df(df)
        return "✅ Gasto registrado com sucesso!"
    except Exception as e:
        return f"Erro: {str(e)}"

def ver_extrato_e_saldo():
    try:
        df = inicializar_planilha()
        df = df.reset_index(drop=True)
        df.index.name = "ID"
        total_receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
        saldo = total_receitas - total_despesas
        status = (
            "🟢 Saldo Positivo" if saldo > 0 else
            "🟡 Saldo Zerado" if saldo == 0 else
            "🔴 Negativado"
        )

        # Gráfico por categoria
        despesas = df[df["Tipo"] == "Despesa"]
        fig1, ax1 = plt.subplots()
        despesas.groupby("Categoria")["Valor"].sum().sort_values().plot(kind="barh", ax=ax1)
        ax1.set_title("Gastos por Categoria")
        fig1.tight_layout()

        # Gráfico por forma
        fig2, ax2 = plt.subplots()
        despesas.groupby("Forma")["Valor"].sum().plot(kind="bar", ax=ax2)
        ax2.set_title("Gastos por Forma de Pagamento")
        fig2.tight_layout()

        return df, f"💰 Receitas: R$ {total_receitas:.2f}\n💸 Despesas: R$ {total_despesas:.2f}\n📊 Saldo: R$ {saldo:.2f}\n{status}", fig1, fig2

    except Exception as e:
        return pd.DataFrame(), f"Erro ao gerar extrato: {str(e)}", None, None

def excluir_transacao(index):
    try:
        df = inicializar_planilha()
        if 0 <= index < len(df):
            df = df.drop(index).reset_index(drop=True)
            salvar_df(df)
            return f"Transação de índice {index} excluída com sucesso!"
        else:
            return "Índice inválido."
    except Exception as e:
        return f"Erro ao excluir: {str(e)}"

def excluir_todas_transacoes():
    try:
        df_vazio = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Forma", "Cartão"])
        salvar_df(df_vazio)
        return "✅ Todas as transações do mês foram apagadas!"
    except Exception as e:
        return f"Erro ao excluir todas: {str(e)}"

# Interface com Gradio
with gr.Blocks(title="Controle de Gastos Mensais") as app:
    gr.Markdown("# 💸 Controle de Gastos Mensais")

    with gr.Tab("Registrar Entrada"):
        tipo_entrada = gr.Dropdown(["Salário", "Outros"], label="Tipo de Receita", value="Salário")
        valor_entrada = gr.Number(label="Valor (R$)", value=0)
        botao_entrada = gr.Button("Registrar Receita")
        saida_entrada = gr.Textbox(label="Mensagem")

        botao_entrada.click(fn=registrar_entrada, inputs=[tipo_entrada, valor_entrada], outputs=saida_entrada)

    with gr.Tab("Registrar Gasto"):
        valor_gasto = gr.Number(label="Valor (R$)", value=0)
        forma_pagamento = gr.Dropdown(["Pix", "Crédito"], label="Forma de Pagamento", value="Pix")
        categoria_gasto = gr.Dropdown(["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", "Outros"], label="Categoria", value="Alimentação")
        cartao_usado = gr.Textbox(label="Cartão (se Crédito)", placeholder="Ex: Nubank")
        botao_gasto = gr.Button("Registrar Gasto")
        saida_gasto = gr.Textbox(label="Mensagem")

        botao_gasto.click(fn=registrar_gasto, inputs=[valor_gasto, forma_pagamento, categoria_gasto, cartao_usado], outputs=saida_gasto)

    with gr.Tab("Extrato e Saldo"):
        botao_extrato = gr.Button("Ver Extrato Atual")
        extrato = gr.Dataframe(label="Extrato do Mês")
        resumo_saldo = gr.Textbox(label="Resumo Financeiro")
        graf1 = gr.Plot()
        graf2 = gr.Plot()

        botao_extrato.click(fn=ver_extrato_e_saldo, inputs=[], outputs=[extrato, resumo_saldo, graf1, graf2])

    with gr.Tab("Excluir Lançamento"):
        idx_excluir = gr.Number(label="Digite o índice da transação para excluir", value=0)
        botao_excluir = gr.Button("Excluir Transação")
        saida_excluir = gr.Textbox(label="Mensagem")

        botao_excluir.click(fn=excluir_transacao, inputs=[idx_excluir], outputs=saida_excluir)

        botao_excluir_tudo = gr.Button("Excluir Todas as Transações do Mês")
        saida_excluir_tudo = gr.Textbox(label="Mensagem")

        botao_excluir_tudo.click(fn=excluir_todas_transacoes, inputs=[], outputs=saida_excluir_tudo)

app.launch()
