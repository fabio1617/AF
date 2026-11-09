#Onde ficam as regras de fraude

import pandas as pd 
import json
import os

#🔴 Regra 1: Valor Alto
# Detecta transações com valor acima de 5.000
def high_value(transaction):  #Valor da transação
    return transaction['amount'] > 5000

# Detecta transações realizadas em países considerados de alto risco
# Lista de países carregada de listas/paises_risco.json
def risky_country(transaction):
    caminho = os.path.join(os.path.dirname(__file__), 'listas', 'paises_risco.json')
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    codigos = [p['codigo'] for p in dados['paises']]
    return transaction['country'] in codigos

# ⚡ Regra 3: Alta Frequência
# Detecta quando um usuário realiza mais de 2 transações em um intervalo de 5 minutos
# Pode indicar uso indevido ou cartão comprometido
def high_frequency(transaction, data):

    # Filtra transações do mesmo usuário
    user_data = data[data['user_id'] == transaction['user_id']]

    # Janela de 5 minutos antes da transação atual
    window = user_data[
        (user_data['timestamp'] >= transaction['timestamp'] - pd.Timedelta(minutes=5)) &
        (user_data['timestamp'] <= transaction['timestamp'])                
    ]

    return len(window) > 2

# 🌍 Regra 4: Viagem Impossível
# Detecta mudança de país em um curto intervalo de tempo
# Pode indicar uso simultâneo do cartão em locais diferentes
def impossible_travel(transaction, data):

    user_data = data[data['user_id'] == transaction['user_id']]

    #pega transações anteriores
    previous = user_data[
        user_data['timestamp'] < transaction['timestamp']
    ].sort_values(by='timestamp', ascending=False)

    if previous.empty:
        return False
    
    last_transaction = previous.iloc[0]

    #se mudou de pais em menos de 5 minutos → suspeito
    time_diff = transaction['timestamp'] - last_transaction['timestamp']

    if transaction['country'] != last_transaction['country'] and time_diff <= pd.Timedelta(minutes=5):
        return True
    
    return False

# 🏪 Regra 6: Merchant Bloqueado
# Detecta transações em estabelecimentos identificados como fraudulentos
# Lista de merchants carregada de listas/merchants_bloqueados.json
def blocked_merchant(transaction):
    caminho = os.path.join(os.path.dirname(__file__), 'listas', 'merchants_bloqueados.json')
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    merchants = [m['nome'] for m in dados['merchamts']]
    return transaction['merchant'] in merchants


# 🚫 Regra 7: MCC Restrito por produto
# Detecta transações com MCC não permitido para o produto do cartão
#Listas carregadas de listas/mcc_restritos.json e listas/produtos_restritos.json
def restricted_mcc(transaction):
    caminho_mcc = os.path.join(os.path.dirname(__file__), 'listas', 'mcc_restritos.json')
    caminho_produtos = os.path.join(os.path.dirname(__file__), 'listas', 'produtos_restritos.json')

    with open( caminho_mss, 'r', encoding= 'utf-8') as f:
        dados_mcc = json.load(f)

    with open(caminho_produtos, 'r', encoding='utf-8') as f:
        dados_produtos = json.load(f)

    mcc_restritos = [m['codigo'] for m in dados_mcc['mcc']]
    produtos_restritos = [p['nome'] for p in dados_produtos['produtos']]

    mcc_bloqueado = transaction.get('mcc') in mccs_restritos
    produto_bloqueado = transaction.get ('product') in produtos_restritos

    return mcc_bloqueado and produto_bloqueado 
