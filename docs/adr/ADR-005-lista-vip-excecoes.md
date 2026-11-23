# ADR-005: Lista VIP como exceção configurável

**Data:** 2026-11-23
**Status:** Proposto

## Contexto
Alguns clientes precisam de permissões diferentes das regras padrão. Por
exemplo, o cartão corporativo usado pelo RH: o dinheiro é da empresa, mas
o uso inclui eventos de funcionários, almoços com clientes, transações de
alto valor e horários fora do habitual, tudo combinado com a diretoria.
Transações assim eram negadas pelas regras. Os clientes também costumam
pedir mudanças nos limites, e cada pedido de exceção não deveria virar uma
regra nova.

## Opções consideradas
1. Criar uma regra nova para cada pedido de exceção.
2. Uma lista de exceção por cliente, cartão ou TA, com limite e prazo
   próprios, usada pela regra de aprovação (VIP).
3. Cada regra de limite consultar a sua própria lista de exceções.

## Decisão
Adotar uma lista de exceção (lista VIP) por cliente, cartão ou TA. Cada
entrada pode ter um limite de valor próprio e um prazo, definido ou
indeterminado. A lista pode ser alterada manualmente, conforme o pedido do
cliente.

A lista VIP não anula as regras de política do produto. Um usuário de
benefício flexível, por exemplo, continua sem conseguir sacar o saldo,
porque o MCC não é permitido, mesmo estando na lista.

## Motivo
- Evita criar uma regra nova a cada pedido de exceção.
- A exceção é um dado que se altera na lista, sem mudar o código.
- Reaproveita pesos e ações do ADR-004. A regra VIP tem peso 9, então
  vence a regra de valor alto (8) e perde para as regras de comportamento
  e de política (10 a 12). Assim o MCC restrito continua valendo.

A opção 1 não escala com muitos pedidos. A opção 3 espalha as exceções por
várias listas, e fica difícil saber o que cada cliente pode fazer.

## Consequências
- A lista precisa de revisão periódica. Uma conta VIP invadida passa pelo
  motor até o limite definido para ela.
- A inclusão na lista não libera o que foi negado por regras de peso maior.
  Para liberar um cliente, é preciso saber qual regra negou a transação
  (ADR-003).
- Hoje a regra VIP (R05) usa só a coluna `is_vip` e um limite fixo de
  R$ 3.000. Limite e prazo por cliente ainda não estão implementados.
- A lista de autorizados internacionais (R08) já segue esse formato, com
  `data_expiracao` e `limite_valor`, e serve de modelo.