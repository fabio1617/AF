# Interface (o que você vai ver na tela)
import streamlit as st
import pandas as pd
from engine import run_rules
import rules
from engine import calculate_metrics

st.title('Motor de Risco 🚀')

uploaded_file = st.file_uploader('📂 Faça upload de um arquivo CSV', type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv('data.csv')

data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')    

required_columns = ['transaction_id', 'user_id', 'amount', 'country', 'merchant', 'channel', 'timestamp', 'status', 'is_fraud']
                           
if not all(col in data.columns for col in required_columns):
    st.error('❌ O arquivo precisa conter as colunas: transaction_id, user_id, amount, country, merchant, channel, timestamp, status, is_fraud')
    st.stop()


st.sidebar.title('⚙️ Configuração de Regras')

usar_valor_alto = st.sidebar.checkbox('Valor Alto', value=True)
usar_pais_risco = st.sidebar.checkbox('País de Risco', value=True)
usar_frequencia = st.sidebar.checkbox('Alta Frequência', value=True)
usar_viagem = st.sidebar.checkbox('Viagem Impossível', value=True)

#Formato de Lista tuplas (nome, função, peso)
rules_dict = []

if usar_valor_alto:
    rules_list.append(('Valor Alto', rules.high_value, 8))

if usar_pais_risco:
    rules_list.append(('País de Risco', rules.risky_country, 12))

if usar_frequencia:
    rules_list.append(('Alta Frequência', rules.high_frequency, 10))

if usar_viagem:
    rules_list.append(('Viagem Impossível', rules.impossible_travel, 11))

results = run_rules(data, rules_list)

tp, fp, tn, fn = calculate_metrics(results)
 
df_resultados = pd.DataFrame(results).rename(columns={  
    'transaction_id': 'ID da Transação',
    'triggered_rules': 'Regras Ativadas',
    'maior_peso': 'Maior Peso',    'is_fraud': 'É Fraude'
})

st.write(df_resultados)

st.subheader('📊 Métricas')

col1, col2, col3, col4 = st.columns(4)

col1.metric("Fraudes Detectadas", tp)
col2.metric("Falsos Positivos", fp)
col3.metric("Negativos Corretos", tn)
col4.metric("Fraudes Perdidas", fn)