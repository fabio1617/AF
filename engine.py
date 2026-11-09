#Onde roda as regras nos dados

def run_rules(data, rules):
    results = []

    for _, row in data.iterrows():
        triggered = []
        transaction = row.to_dict()
        
        for rule_name, rule_func, peso, acao in rules:
            try:
                if rule_func(transaction, data):
                    triggered.append((rule_name, peso, acao))
            except TypeError:
                if rule_func(transaction):
                    triggered.append((rule_name, peso, acao))                
        # Ordena por peso decrescente (maior peso = maior prioridade)
        triggered.sort(key=lambda x: x[1], reverse=True)

        # A regra de maior peso decide. Em empate de peso, negar vence.
        if triggered:
            maior_peso = triggered[0][1]
            acoes_do_maior_peso = [r[2] for r in triggered if r[1] == maior_peso]
            decisao = 'negar' if 'negar' in acoes_do_maior_peso else 'aprovar'
        else:
            decisao = 'aprovar'

        results.append({
            'transaction_id': row['transaction_id'],
            'triggered_rules': [r[0] for r in triggered],
            'maior_peso': triggered[0][1] if triggered else None,
            'decisao': decisao,
            'is_fraud': row['is_fraud']
        })

    return results

def calculate_metrics(results):
    tp = fp = tn = fn = 0

    for r in results:
        predicted = r['decisao'] == 'negar'
        actual = r['is_fraud'] == 1

        if predicted and actual:
            tp +=1
        elif predicted and not actual:
            fp +=1
        elif not predicted and not actual:
            tn +=1
        elif not predicted and actual:
            fn +=1

    return tp, fp, tn, fn                          