**Data:** 2026-11-16
**Status:** Aceito

## Contexto

O motor AF foi idealizado para automatizar a tomada de decisão de transações, considerando especialmente cenários de alto volume e empresas que não possuem uma estrutura operacional robusta para análise manual em tempo integral.

A proposta é reduzir a dependência de intervenção humana no fluxo inicial de autorização, permitindo que as transações sejam avaliadas por regras automatizadas e recebam uma decisão objetiva.

O projeto considera que diferentes empresas e produtos possuem características operacionais e perfis de risco distintos. Portanto, as políticas de autorização e restrição precisam considerar o segmento e a finalidade do produto utilizado.

## Opções consideradas
1. Três estados (aprovar, revisar, negar), com fila para um analista decidir.
2. Dois estados (aprovar ou negar), com contestação feita pelo cliente depois.
3. Dois estados com confirmação do cliente por mensagem antes de negar.

## Decisão

Adotar uma decisão binária: **aprovar ou negar**.

O motor não terá uma fila de revisão manual como parte do fluxo inicial. A decisão será tomada automaticamente com base nas regras configuradas, seus respectivos pesos e ações.

A contestação de uma transação negada será tratada como um processo externo ao fluxo inicial de decisão do motor.

A inclusão de um cliente em uma lista VIP não deverá representar uma aprovação automática de todas as suas transações.

Antes de conceder qualquer liberação ou autorização, será necessário identificar qual regra provocou a negativa e analisar o motivo da reprovação.

As regras deverão permitir configurações compatíveis com as características e políticas de cada cliente, produto ou segmento, evitando que restrições específicas de uma operação sejam aplicadas indiscriminadamente a todas as demais.

## Consequências

- O motor terá uma resposta rápida, sem depender da disponibilidade de um analista.
- Poderá ocorrer um volume maior de negativas, inclusive de transações legítimas, aumentando o risco de atrito com os clientes.
- A contestação deverá considerar a regra responsável pela negativa e o motivo identificado antes de qualquer decisão de liberação.
- A inclusão na lista VIP não garantirá aprovação quando outras regras de maior prioridade forem acionadas.
- As regras e seus critérios de prioridade deverão ser calibrados para reduzir falsos positivos sem comprometer a segurança.
- As políticas de risco poderão variar conforme o segmento, produto ou cliente, respeitando as particularidades de cada operação.

## Evoluções futuras

- Desenvolver mecanismos de comunicação com o cliente para apresentar, de maneira adequada, o motivo de uma transação negada. Atualmente, a identificação da regra responsável está disponível na visão interna do sistema.
- Implementar um fluxo de contestação de transações negadas.
- Avaliar autorizações específicas por cliente, cartão, estabelecimento ou tipo de transação, considerando o motivo da negativa.
- Permitir a configuração de políticas e restrições específicas por segmento e produto, incluindo regras de MCC, estabelecimentos e categorias de transação.
- Evoluir a gestão de regras para permitir que usuários autorizados configurem parâmetros e condições sem precisar alterar diretamente o código-fonte.
- Implementar notificações para que o cliente confirme operações suspeitas, como uma possível alternativa para o tratamento de transações negadas.