import streamlit as st
import sqlite3
import pandas as pd

# conectar ao banco de dados sqlite
conn = sqlite3.connect('../data/quotes.db')

# carregar os dados da tabela do banco de dados
df = pd.read_sql_query('SELECT * FROM mercado_livre_itens', con=conn)

# fechar a conexao do banco de dados
conn.close()

# alterar largura da pagina do streamlit
st.set_page_config(layout="wide")

# TITULO
#with st.columns(3)[1]:
st.title('Mercado Livre - Tênis de Corrida')

# subtitulo
st.subheader('Principais KPIs')

col1, col2, col3 = st.columns(3)

# KPI1: numero total de itens
total_itens = df.shape[0]
col1.metric(label='Número total de itens', value=total_itens)

# KPI2: numero de marcas unicas
marcas = df['brand'].nunique()
col2.metric(label='Número de marcas únicas', value=marcas)

# KPI3: preco atual medio
preco_atual_medio = df['preco_atual'].mean()
col3.metric(label='Preço atual médio', value=round(preco_atual_medio, 2))

# Marcas mais encontradas ate a pagina 10
st.subheader('Marcas mais encontradas até a página 10')
col1, col2 = st.columns([2, 1])
top_10_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_brands)
col2.write(top_10_brands)


# Preco medio por marca
st.subheader('Preço médio por marca')
col1, col2 = st.columns([2, 1])
df_non_zero = df[df['preco_atual'] > 0]
preco_medio_por_marca = df_non_zero.groupby('brand')['preco_atual'].mean().sort_values(ascending=False)
col1.bar_chart(preco_medio_por_marca)
col2.write(preco_medio_por_marca)

# satisfacao por marca
st.subheader('Satisfação por marca')
col1, col2 = st.columns([2, 1])

df_non_zero = df[df['rating'] > 0]
satisfacao_por_marca = df_non_zero.groupby('brand')['rating'].mean().sort_values(ascending=False)

col1.bar_chart(satisfacao_por_marca)
col2.write(satisfacao_por_marca)

salomon = df[df['brand'] == 'SALOMON']
st.write(salomon)