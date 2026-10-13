#Onde roda as regras nos dados

def run_rules(data, rules):
    results = []

    for _, row in data.iterrows():
        triggered = []
        transaction = row.to_dict()
        
        for rule_name, rule_func, peso in rules:
            try:
                if rule_func(transaction, data):
                    triggered.append((rule_name, peso))
            except TypeError:
                if rule_func(transaction):
                    triggered.append((rule_name, peso))                
        # Ordena por peso decrescente (maior peso = maior prioridade)
        triggered.sort(key=lambda x: x[1], reverse=True)

        # Decisão binária: se alguma regra disparou → negar
        # Regra de aprovação (R05 VIP) podem ser sobrescritas por peso maior
        decisao = 'negar' if triggered else 'aprovar'

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