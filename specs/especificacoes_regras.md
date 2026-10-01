# Especificações de Regras — Risk Simulator

## Índice de Regras

- [ ] high_value
- [ ] risky_country
- [ ] high_frequency
- [ ] impossible_travel
- [ ] R05: Aprovação para cliente VIP
- [ ] R06: Estabelecimento bloqueado
- [ ] R07: MCC restrito por produto

---

## Escala de Prioridade

| Peso | Categoria |
|------|-----------|
| 1-7  | Reservado para expansão futura |
| 8-9  | Regras de limite (valor alto, perfil básico) |
| 10-11 | Regras de comportamento (velocidade, histórico) |
| 12   | Bloqueio absoluto + Regras de produto |

### Regras de empate
- Quando duas regras disparam com o mesmo peso → **negar vence**
- Decisão é binária: **aprovar** ou **negar**
- Não há fila de revisão — o motor decide sozinho

---

## Regras Implementadas

## R01: high_value - Alto Valor 
- **Peso:** 8
- **Objetivo:** Evitar que transações de alto valor ser realizado em um determinado produto ou cartão ou empresa.
- **Dados:** Id da transação, produto, valor, id card, TA
- **Condição:** A regra dispara quando identifica transações igual ou maior que R$5.000,00 E o produto OU cartão OU TA esta na lista restrita.
- **Decisão:** Negar - pode ser sobreposta por regras de peso superior (9 a 12)
- **Impacto esperado:** Impedir que usuários, TA e cliente que usam um determinado produtos não consigam realizar transações de alto valor.
- **Código de motivo:** R01_ALTO_VALOR
- **Mensagem ao analista:** A transação de R$xxxx foi reprovado porque o Id card (xxx), ou  TA (xxx) não pode transacionar valor alto.
- **Mensagem ao cliente:** Transação Negada

---

### R02: risky_country - Pais de Risco
- **Peso:** 9
- **Objetivo:**
- **Dados:**
- **Condição:**
- **Decisão:**
- **Impacto esperado:**
- **Código de motivo:**
- **Mensagem ao analista:**
- **Mensagem ao cliente:**

---

### R03: high_frequency - Alta Frequencia
- **Peso:** 10
- **Objetivo:**
- **Dados:**
- **Condição:**
- **Decisão:**
- **Impacto esperado:**
- **Código de motivo:**
- **Mensagem ao analista:**
- **Mensagem ao cliente:**

---

### R04: impossible_travel - Proibido transações internacionais
- **Peso:** 11
- **Objetivo:**
- **Dados:**
- **Condição:**
- **Decisão:**
- **Impacto esperado:**
- **Código de motivo:**
- **Mensagem ao analista:**
- **Mensagem ao cliente:**

---

## Regras Especificadas (aguardando implementação)

### R05: Aprovação para cliente VIP
- **Peso:** 9
- **Objetivo:** evitar que clientes confiáveis e conhecidos sejam barrados por regras de limite em compras do dia a dia.
- **Dados:** ID do cliente, lista VIP, limite VIP do cliente, valor da transação.
- **Condição:** o cliente está na lista VIP E o valor da transação é menor ou igual ao limite VIP do cliente (padrão: R$ 3.000,00). Acima do limite, a regra não dispara e a transação segue para as demais regras.
- **Decisão:** aprovar. Pode ser sobreposta por regras de peso 12.
- **Impacto esperado:** menos atrito para bons clientes. Risco: se uma conta VIP for invadida, o fraudador passa por esta regra até o limite do cliente. Tratamento: revisão periódica da lista VIP e limites conservadores.
- **Código de motivo:** R01_CLIENTE_VIP
- **Mensagem ao analista:** "Cliente {id_cliente} está na lista VIP e o valor R$ {valor} está dentro do limite de R$ {limite_vip}."
- **Mensagem ao cliente:** "Transação aprovada."

---

### R06: Estabelecimento bloqueado
- **Peso:** 12
- **Objetivo:** proteger os clientes de perdas financeiras em estabelecimentos que um analista de risco já identificou como fraudulentos.
- **Dados:** ID do merchant da transação, lista de merchants bloqueados.
- **Condição:** o ID do merchant da transação está na lista de merchants bloqueados.
- **Decisão:** negar. Peso 12 — sobrepõe todas as demais regras.
- **Impacto esperado:** impede perdas em estabelecimentos conhecidos por fraude. Risco: merchant legítimo na lista por erro. Tratamento: revisão periódica e remoção mediante contestação.
- **Código de motivo:** R02_MERCHANT_BLOQUEADO
- **Mensagem ao analista:** "Merchant {id_merchant} está na lista de merchants bloqueados."
- **Mensagem ao cliente:** "Transação não autorizada."

---

### R07: MCC restrito por produto
- **Peso:** 12
- **Objetivo:** garantir que cartões de benefício e despesas sejam usados apenas para a finalidade definida pela empresa cliente.
- **Dados:** MCC da transação, produto do cartão, lista de MCCs restritos, lista de produtos com restrição.
- **Condição:** o produto da transação está na lista de produtos restritos OU o MCC está na lista de MCCs restritos. Produtos restritos: Benefícios flexíveis, Combustível e frotas, Despesas corporativas, Premiação. MCCs restritos: 6010 (saque manual), 6011 (saque em caixa eletrônico), 7995 (apostas).
- **Decisão:** negar. Peso 12 — sobrepõe todas as demais regras.
- **Impacto esperado:** mantém o uso do cartão dentro da política do produto. Risco: cartão cadastrado no produto errado teria saques legítimos negados. Tratamento: conferir cadastro do produto quando houver contestação.
- **Código de motivo:** R03_MCC_RESTRITO
- **Mensagem ao analista:** "Transação com MCC {mcc} não permitida para o produto {produto}."
- **Mensagem ao cliente:** "Transação negada."