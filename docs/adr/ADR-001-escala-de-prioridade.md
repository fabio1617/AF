# ADR-001: Escala de Prioridade das Regras

**Data:** 2026-10-03  
**Status:** Aceito

## Contexto
O motor precisa resolver conflitos quando mais de uma regra dispara 
na mesma transação. Sem uma ordem definida, o resultado é imprevisível.

## Opções consideradas
1. Descrever prioridade por nome ("tem prioridade sobre R02 e R03")
2. Escala numérica onde menor número = maior prioridade
3. Escala numérica onde maior número = maior prioridade

## Decisão
Escala de 1 a 12 onde **maior número = maior prioridade**.

| Peso | Categoria |
|------|-----------|
| 1-7  | Reservado para expansão futura |
| 8-9  | Regras de limite |
| 10-11 | Regras de comportamento |
| 12   | Bloqueio absoluto + Regras de produto |

## Motivo
A opção 1 se torna inviável com mais de 10 regras — impossível 
lembrar qual sobrepõe qual. A escala crescente (opção 3) foi 
escolhida sobre a decrescente porque é mais intuitivo: quanto 
maior o risco, maior o número.

## Regra de empate
Quando duas regras disparam com o mesmo peso, **negar vence**. 
Decisão conservadora por padrão — mais fácil negar e tratar 
contestação do que aprovar uma fraude.

## Consequências
- Adicionar uma regra nova exige definir seu peso antes de implementar
- Regras de peso 12 bloqueiam inclusive clientes VIP
- A faixa 1-7 está reservada para expansão sem quebrar a escala atual

