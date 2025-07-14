# controle-financeiro
# 📊 Aplicação de Controle Financeiro Pessoal

Este projeto é uma aplicação web desenvolvida com **Gradio** para registro e acompanhamento de **gastos mensais**, com opção de entrada via **Pix** ou **Crédito**.

A aplicação foi criada como reforço da matéria de *Deploy* no curso de **Cientista de Dados da DNC**, e está disponível gratuitamente via **Hugging Face Spaces**.

---

## 🚀 Funcionalidades

- Registro de **gastos** com:
  - Valor
  - Tipo de gasto: `Pix` ou `Crédito`
  - Categoria (alimentação, transporte, etc.)
  - Cartão (caso seja no crédito)
- Registro de **receitas** (salário ou extras)
- Cálculo automático de:
  - Total gasto no mês
  - Saldo disponível
  - Aviso se saldo está positivo, zerado ou negativo
- Visualização de extrato com **índice** das transações
- Exclusão de transações específicas ou de todo o mês
- **Gráficos interativos** de:
  - Gastos por **categoria**
  - Gastos por **tipo** (Pix / Crédito)
- Armazenamento automático em **planilha Excel**:
  - Cada mês tem sua própria aba
  - Os dados são persistentes mesmo após fechar o app

---

## 📎 Tecnologias Utilizadas

- Python 3.10+
- Gradio
- Pandas
- Matplotlib
- Openpyxl

---
