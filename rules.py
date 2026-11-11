#Onde ficam as regras de fraude

import pandas as pd 
import json
import os

#🔴 Regra 1: Valor Alto
# Detecta transações iguais ou acima de R$ 5.000 quando o produto, o cartão ou
# a empresa (TA) estiver nas listas de restrição
# Listas: alto_valor_produtos.json, cartoes_restritos.json, empresas_restritas.json
def high_value(transaction):
    # Abaixo do limite, a regra nem precisa olhar as listas
    if transaction['amount'] < 5000:
        return False

    pasta = os.path.join(os.path.dirname(__file__), 'listas')

    with open(os.path.join(pasta, 'alto_valor_produtos.json'), 'r', encoding='utf-8') as f:
        produtos = [p['nome'] for p in json.load(f)['produtos']]

    with open(os.path.join(pasta, 'cartoes_restritos.json'), 'r', encoding='utf-8') as f:
        cartoes = [c['id'] for c in json.load(f)['cartoes']]

    with open(os.path.join(pasta, 'empresas_restritas.json'), 'r', encoding='utf-8') as f:
        empresas = [e['id'] for e in json.load(f)['empresas']]

    produto_restrito = transaction.get('product') in produtos
    cartao_restrito = str(transaction.get('card_id')) in cartoes
    empresa_restrita = str(transaction.get('ta_id')) in empresas
                                              
    return produto_restrito or cartao_restrito or empresa_restrita

# 🌍 Regra 2: País de Risco 
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
    merchants = [m['nome'] for m in dados['merchants']]
    return transaction['merchant'] in merchants


# 🚫 Regra 7: MCC Restrito por produto
# Detecta transações com MCC não permitido para o produto do cartão
#Listas carregadas de listas/mcc_restritos.json e listas/produtos_restritos.json
def restricted_mcc(transaction):
    caminho_mcc = os.path.join(os.path.dirname(__file__), 'listas', 'mcc_restritos.json')
    caminho_produtos = os.path.join(os.path.dirname(__file__), 'listas', 'produtos_restritos.json')

    with open(caminho_mcc, 'r', encoding='utf-8') as f:
        dados_mcc = json.load(f)

    with open(caminho_produtos, 'r', encoding='utf-8') as f:
        dados_produtos = json.load(f)

    mccs_restritos = [m['codigo'] for m in dados_mcc['mcc']]
    produtos_restritos = [p['nome'] for p in dados_produtos['produtos']]

    mcc_bloqueado = transaction.get('mcc') in mccs_restritos
    produto_bloqueado = transaction.get('product') in produtos_restritos

    return mcc_bloqueado and produto_bloqueado 

# ⭐ Regra 5: Cliente VIP
# Aprova transações de clientes VIP dentro do limite VIP (padrão R$ 3.000)
# Usa a coluna is_vip do CSV
def vip_client(transaction):
    return transaction.get('is_vip', 0) == 1 and transaction['amount'] <= 3000


# 🌐 Regra 8: Transação Internacional Não Autorizada
# Detecta transações fora do BR sem autorização válida (sem cadastro, expirada ou acima do limite)
# Lista carregada de listas/autorizados_internacional.json
def unauthorized_international(transaction):
    #Transação nacioanl não é avaliada por esta regra
    if transaction['country'] == 'BR':
        return False

    caminho = os.path.join(os.path.dirname(__file__), 'listas', 'autorizados_internacional.json')
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    for item in dados['autorizados']:
        # A autorização pode ser por user_id ou por card_id
        if item['tipo'] == 'user_id':
            valor_transacao = str(transaction['user_id'])
        else:
            valor_transacao = str(transaction.get('card_id'))
        if item['identificador'] == valor_transacao:
            expirou = transaction['timestamp'] > pd.to_datetime(item['data_expiracao'])
            acima_limite = transaction['amount'] > item['limite_valor']
            return expirou or acima_limite

    # Não achou na lista: sem autorização
    return True        
