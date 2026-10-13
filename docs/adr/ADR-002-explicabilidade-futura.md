# ADR-002: Explicabilidade por transação

**Data:** 2026-10-06
**Status:** Pendente — previsto para o Mês 6

## Contexto
O motor atual registra métricas agregadas (tp, fp, tn, fn) mas não 
identifica qual transação específica foi um falso positivo ou falso negativo.

## Decisão pendente
Adicionar o campo `resultado` no `results.append` do `engine.py`:

results.append({
    ...
    'decisao': decisao,
    'is_fraud': row['is_fraud'],
    'resultado': # tp, fp, tn ou fn — a calcular
})

## Motivo do adiamento
Depende da refatoração do engine prevista no Mês 6 
junto com logs e trilha de auditoria.