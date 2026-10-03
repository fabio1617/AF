# Especificações de Regras — Risk Simulator

## Índice de Regras

- [ ] R01: high_value - Alto Valor
- [ ] R02: risky_country - País de Risco
- [ ] R03: high_frequency - Alta Frequência
- [ ] R04: impossible_travel - Viagem Impossível
- [ ] R05: vip_client - Aprovação para cliente VIP
- [ ] R06: blocked_merchant - Estabelecimento bloqueado
- [ ] R07: restricted_mcc - MCC restrito por produto
- [ ] R08: unauthorized_international - Transação Internacional Não Autorizada

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
- **Peso:** 12 
- **Objetivo:** Identificar transações de paises que representam risco em suas operações.
- **Dados:** Id_Transação, Pais
- **Condição:** A regra dispara quando o país da transação estiver 
na lista contida em listas/paises_risco.json
- **Decisão:** Negar - Peso 12 — sobrepõe todas as demais regras.
- **Impacto esperado:** Reprovar toda e qualquer transação que for realizada 
nesses países que representam risco de lavagem de dinheiro. 
Nota de calibração: o peso 12 bloqueia 100% das transações nesses países, 
inclusive para clientes VIP. Revisão recomendada se o apetite de risco da 
empresa mudar ou se houver expansão para algum desses mercados.
- **Código de motivo:** R02_Pais_Risco
- **Mensagem ao analista:** A transação de R$ 00,00 foi recusada porque não é permitido realizar transações do Pais de origem.  
- **Mensagem ao cliente:** Transação Negada

---

### R03: high_frequency - Alta Frequencia
- **Peso:** 10
- **Objetivo:** Identitificar transações realizadas com um curto espaço de tempo, para evitar fraudes de teste de cartão.
- **Dados:** user_id, timestamp
- **Condição:**A regra dispara quando o mesmo usuário realizar mais de 2 transações em um intervalo de 5 minutos.
- **Decisão:** Negar - pode ser sobreposta por regras de peso 11 e 12.
- **Impacto esperado:** Reprovar transações quando identificada alta frequência pelo mesmo usuário em um intervalo de 5 minutos. 
Risco: usuários legítimos com múltiplas compras rápidas podem ser barrados. 
Tratamento: contestação via atendimento para revisão manual.
- **Código de motivo:** R03_Alta_Frequencia
- **Mensagem ao analista:** A transação foi bloqueada porque identificamos alta frquencia em uma curto espaço de tempo.
- **Mensagem ao cliente:** Transação Negada

---

### R04: impossible_travel - Viagem Impossível
- **Peso:** 11
- **Objetivo:** Detectar quando o mesmo usuário realiza transações em países diferentes em um intervalo de tempo fisicamente impossível de viajar.
- **Dados:** ID user, Produto, Pais.
- **Condição:** A regra dispara quando o mesmo usuário realizar transações 
em países diferentes em um intervalo menor que 5 minutos.
- **Decisão:** Negar - Pode ser sobreposta por regras de peso 12.
- **Impacto esperado:** Reprovar transações onde o mesmo usuário 
aparece em países diferentes em tempo fisicamente impossível 
de viajar. Risco: usuário com VPN ou proxy pode disparar 
a regra sem ser fraude. Tratamento: contestação via atendimento.
- **Código de motivo:** R04_VIAGEM_IMPOSSIVEL
- **Mensagem ao analista:** Transação bloqueada porque o usuário 
{user_id} realizou transações em {país_anterior} e {país_atual} 
com intervalo de {tempo} minutos.
- **Mensagem ao cliente:** Transação Negada


---

### R05: Aprovação para cliente VIP
- **Peso:** 9
- **Objetivo:** evitar que clientes confiáveis e conhecidos sejam barrados por regras de limite em compras do dia a dia.
- **Dados:** ID do cliente, lista VIP, limite VIP do cliente, valor da transação.
- **Condição:** o cliente está na lista VIP E o valor da transação é menor ou igual ao limite VIP do cliente (padrão: R$ 3.000,00). Acima do limite, a regra não dispara e a transação segue para as demais regras.
- **Decisão:** aprovar. Pode ser sobreposta por regras de peso 12.
- **Impacto esperado:** menos atrito para bons clientes. Risco: se uma conta VIP for invadida, o fraudador passa por esta regra até o limite do cliente. Tratamento: revisão periódica da lista VIP e limites conservadores.
- **Código de motivo:** R05_CLIENTE_VIP
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
- **Código de motivo:** R06_MERCHANT_BLOQUEADO
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
- **Código de motivo:** R07_MCC_RESTRITO
- **Mensagem ao analista:** "Transação com MCC {mcc} não permitida para o produto {produto}."
- **Mensagem ao cliente:** "Transação negada."


---

### R08: unauthorized_international - Transação Internacional Não Autorizada
- **Peso:** 11
- **Objetivo:** Bloquear transações internacionais de usuários que não possuem autorização para operar fora do país de origem.
- **Dados:** user_id, card_id, country, valor, lista de autorizados em listas/autorizados_internacional.json.
- **Condição:** A regra dispara quando o país da transação for diferente de BR E o user_id OU card_id não estiver na lista de autorizados, OU estiver na lista mas a data de expiração já passou, OU o valor da transação ultrapassar o limite autorizado.
- **Decisão:** Negar - Pode ser sobreposta por regras de peso 12.
- **Impacto esperado:** Reprovar transações internacionais de usuários sem autorização ou com autorização expirada ou acima do limite. Risco: usuário em viagem legítima sem autorização prévia será barrado. Tratamento: desbloqueio via atendimento com definição de limite e prazo de validade.
- **Código de motivo:** R08_INTERNACIONAL_NAO_AUTORIZADO
- **Mensagem ao analista:** "Transação bloqueada. Usuário {user_id} / cartão {card_id} sem autorização internacional válida. País: {country}. Motivo: {sem_autorizacao | expirado | limite_excedido}."
- **Mensagem ao cliente:** "Transação não autorizada. Entre em contato com o atendimento para liberar transações internacionais."