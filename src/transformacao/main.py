import pandas as pd
import sqlite3
from datetime import datetime

# caminho para os dados
path = '../data/data.jsonl'

# leitura dos dados
df = pd.read_json(path, lines=True)

# setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# cricao de colunas para fontes dos dados e data de coleta
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'
df['_data_coleta'] = datetime.today()

# alterando os tipos das colunas e retirando valores vazios
df['rating'] = df['rating'].fillna(0).astype(float) 
df['reais_antigo'] = df['reais_antigo'].fillna(0).astype(float)
df['centavos_antigo'] = df['centavos_antigo'].fillna(0).astype(float)
df['reais_atual'] = df['reais_atual'].fillna(0).astype(float)
df['centavos_atual'] = df['centavos_atual'].fillna(0).astype(float)

# retirar os parenteses da coluna rating_amount
#df['ratings_amount'] = df['ratings_amount'].str.replace('(', '')
#df['ratings_amount'] = df['ratings_amount'].str.replace(')', '')
df['ratings_amount'] = df['ratings_amount'].str.replace('[\(\)]', '', regex=True)
df['ratings_amount'] = df['ratings_amount'].fillna(0).astype(int)

# tratar os precos como floats e calcular os valores totais
df['preco_antigo'] = df['reais_antigo'] + df['centavos_antigo']/100
df['preco_atual'] = df['reais_atual'] + df['centavos_atual']/100

# remover colunas descnecessarias
df.drop(['reais_antigo', 'centavos_antigo', 'reais_atual', 'centavos_atual'], axis=1)

# conectar banco de dados
conn = sqlite3.connect('../data/quotes.db')

# salvar df no banco de dados
df.to_sql('mercado_livre_itens', con= conn, if_exists='replace', index=False)

# fechar conexao com banco de dados
conn.close()


print(df)
print(df.info())
#print(df)