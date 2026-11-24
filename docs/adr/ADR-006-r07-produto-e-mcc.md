# ADR-006: R07 exige produto restrito E MCC restrito

**Data:** 2026-11-23
**Status:** Aceito

## Contexto
A especificação da R07 dizia que a transação seria negada se o produto
estivesse na lista de produtos restritos OU o MCC estivesse na lista de
MCCs restritos. O código implementava E. A divergência foi notada ao
comparar a spec com as métricas do conjunto de teste, e era preciso
decidir qual das duas versões vale.

## Opções consideradas
1. OU: negar se o produto for restrito ou se o MCC for restrito.
2. E: negar só quando o produto for restrito e o MCC também for restrito.
3. Uma lista de MCCs permitidos para cada produto.

## Decisão
Usar E. A R07 nega a transação quando o produto está na lista de
produtos restritos e o MCC está na lista de MCCs restritos. A
especificação foi corrigida para refletir isso.

## Motivo
- O objetivo da R07 é manter o cartão dentro da finalidade do produto, e
  não bloquear o produto inteiro.
- Com OU, todo uso de um cartão de benefício seria negado, até em
  estabelecimentos comuns. Qualquer saque ou aposta também seria negado
  em produtos que não têm restrição, como a Conta Digital.
- O E combina com o nome da regra ("MCC restrito por produto") e com o
  ADR-005: o usuário de benefício flexível não saca o saldo porque o MCC
  não é permitido.
- As métricas do `data.csv` não decidiram a escolha. Os dados são
  sintéticos, e a decisão vem da finalidade da regra.

A opção 3 é mais precisa, mas dá mais trabalho de manutenção e fica fora
do escopo do Mês 1.

## Consequências
- Produto restrito com um MCC comum não dispara a R07. Se esse uso
  precisar de controle, tem que ser tratado por outra regra.
- No `data.csv`, as transações 11 e 23 (combustível em posto, com cartão de
  combustível) foram reclassificadas como não fraude, porque são o uso
  previsto do produto.
- Se os MCCs permitidos variarem muito por produto, a opção 3 pode virar
  uma evolução futura.