#Onde roda as regras nos dados

def run_rules(data, rules):
    results = []

    for _, row in data.iterrows():
        triggered = []

        transaction = row.to_dict()

        for rule_name, rule_func in rules.items():
            try:
                if rule_func(transaction, data):
                    triggered.append(rule_name)
            except TypeError:
                if rule_func(transaction):
                    triggered.append(rule_name)                

        results.append({
            'transaction_id': row['transaction_id'],
            'triggered_rules': triggered,
            'is_fraud': row['is_fraud']
        })

    return results

def calculate_metrics(results):
    tp = fp = tn = fn = 0

    for r in results:
        predicted = len(r['triggered_rules']) > 0
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