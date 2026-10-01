#Onde ficam as regras de fraude

import pandas as pd

#🔴 Regra 1: Valor Alto
# Detecta transações com valor acima de 10.000
def high_value(transaction):  #Valor da transação
    return transaction['amount'] > 10000


# 🌍 Regra 2: País de Risco
# Detecta transações realizadas em países considerados de alto risco
def risky_country(transaction): #País da transação
    return transaction['country'] in ['NG', 'PK']

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
  