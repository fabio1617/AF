# Motor de Risco

Motor de regras que avalia transações e decide **aprovar** ou **negar** automaticamente, sem fila de revisão.

O projeto é um motor de regras de risco, **não um classificador de machine learning**. Quem define o comportamento são regras escritas por humanos, com peso e decisão explícitos. Cada regra está documentada por escrito antes de virar código.

> Projeto de estudo, em desenvolvimento. Usa apenas **dados sintéticos**.

---

## Como a decisão é tomada

1. Todas as regras ativas são avaliadas para cada transação.
2. As regras que dispararam são ordenadas por **peso** (de 1 a 12; maior número = maior prioridade).
3. A regra de maior peso decide: **aprovar** ou **negar**.
4. Em caso de empate de peso, **negar vence** (decisão conservadora).
5. Se nenhuma regra dispara, a transação é aprovada.

| Peso | Categoria |
|------|-----------|
| 1-7  | Reservado para expansão futura |
| 8-9  | Regras de limite (valor alto, perfil básico) |
| 10-11 | Regras de comportamento (velocidade, histórico) |
| 12   | Bloqueio absoluto e regras de produto |

## Regras implementadas

| Regra | Nome | Peso | Decisão |
|-------|------|------|---------|
| R01 | Valor alto (produto, cartão ou empresa restritos) | 8 | negar |
| R02 | País de risco | 12 | negar |
| R03 | Alta frequência (mais de 2 transações em 5 minutos) | 10 | negar |
| R04 | Viagem impossível (países diferentes em menos de 5 minutos) | 11 | negar |
| R05 | Cliente VIP dentro do limite | 9 | aprovar |
| R06 | Merchant bloqueado | 12 | negar |
| R07 | MCC restrito por produto | 12 | negar |
| R08 | Transação internacional não autorizada | 11 | negar |

A especificação completa de cada regra (objetivo, dados, condição, decisão, impacto esperado e mensagens) está em [`specs/especificacoes_regras.md`](specs/especificacoes_regras.md).

## Estrutura do projeto

```
├── app.py        # interface (Streamlit)
├── engine.py     # executa as regras, decide e calcula métricas
├── rules.py      # funções de cada regra
├── data.csv      # transações sintéticas para teste
├── listas/       # listas consultadas pelas regras (arquivos JSON)
├── specs/        # especificação escrita das regras
└── docs/adr/     # registros de decisão de arquitetura (ADRs)
```

As listas (países de risco, merchants bloqueados, MCCs restritos, autorizações internacionais, etc.) ficam em arquivos JSON separados do código. Para ajustar uma regra, edita-se a lista, sem mexer no código.

## Como rodar

Requisitos: Python 3, `streamlit` e `pandas`.

```bash
pip install streamlit pandas
streamlit run app.py
```

O app abre no navegador, em `http://localhost:8501`. Ele usa o `data.csv` por padrão, ou um CSV enviado pela tela, com as colunas:

```
transaction_id, user_id, amount, country, merchant, channel, timestamp,
status, is_fraud, mcc, product, is_vip, card_id, ta_id
```

Na barra lateral é possível ligar e desligar cada regra e acompanhar as métricas (fraudes detectadas, falsos positivos, negativos corretos e fraudes perdidas).

## Decisões de projeto (ADRs)

- [ADR-001: Escala de prioridade das regras](docs/adr/ADR-001-escala-de-prioridade.md)
- [ADR-002: Explicabilidade por transação](docs/adr/ADR-002-explicabilidade-futura.md)

## Decisões em aberto

- **R07:** a especificação usa produto restrito **OU** MCC restrito, mas o código usa **E**. A escolha muda as métricas e será registrada em um ADR.
- **Limite VIP:** o limite de R$ 3.000 deixa passar uma fraude do conjunto de teste.
- **Explicabilidade:** hoje o app mostra as regras que dispararam, mas não classifica cada transação como acerto ou erro do motor.

## Próximos passos

- Refatorar as regras em objetos independentes, para adicionar uma regra nova sem mexer nas existentes.
- Persistir o histórico de transações em banco de dados e calcular regras de velocidade em cache.
- Expor o motor como API.
- Trilha de auditoria e backtest de regras.
