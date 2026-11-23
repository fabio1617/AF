# ADR-004: Regras com ação e decisão pela regra de maior peso

**Data:** 2026-11-16
**Status:** Aceito

## Contexto
Até a regra de cliente VIP (R05), todas as regras só negavam, então o motor
negava sempre que alguma regra disparava. A R05 aprova, e o motor precisou
saber o que fazer quando uma regra de aprovação e uma de bloqueio disparam
juntas na mesma transação.

## Opções consideradas
1. Liberação fora das regras: uma lista separada, consultada antes, que
   aprova direto.
2. Cada regra tem uma ação (negar ou aprovar), e a de maior peso decide.
3. Regra de aprovação sempre vence as demais.

## Decisão
Cada regra carrega uma ação: `negar` ou `aprovar`. Entre as regras que
dispararam, a de maior peso decide. Em empate de peso, negar vence
(conforme o ADR-001). Se nenhuma regra dispara, a transação é aprovada.

## Motivo
- Reaproveita a escala de pesos do ADR-001, sem criar um mecanismo novo.
- A regra VIP funciona como qualquer outra, sem tratamento especial no código.
- Uma conta VIP invadida não passa por cima de bloqueios fortes (país de
  risco, merchant bloqueado, MCC restrito).

A opção 1 criaria um segundo caminho de decisão para manter. A opção 3
deixaria uma conta VIP invadida passar por tudo.

## Consequências
- Toda regra nova precisa de peso e ação (no `app.py`, uma tupla com
  nome, função, peso e ação).
- Regras de aprovação precisam ter peso menor que as de bloqueio que não
  podem ser vencidas. Um peso errado em uma regra de aprovação libera
  transações que deveriam ser negadas.
- A tela mostra todas as regras que dispararam, inclusive as que perderam.
  Isso ajuda a explicar por que uma transação foi negada.