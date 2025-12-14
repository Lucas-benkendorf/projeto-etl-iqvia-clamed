# Projeto ETL e Análise de Vendas

Este projeto implementa um processo de **ETL (Extração, Transformação e Carga)** seguido de uma **análise exploratória de dados**, utilizando Python e PostgreSQL.
O objetivo é organizar dados de vendas, carregar em um banco relacional e gerar gráficos para apoio à análise.

---

## Estrutura do Projeto

```
projeto-etl-iqvia-clamed/
├── data/
│ ├── raw/
│ │ ├── filial-brick_sample.xlsx
│ │ └── MS_12_2022_sample.xlsx
│ └── processed/
│ ├── dim_filial_transformed.xlsx
│ └── fato_vendas_transformed.xlsx
├── plots/
│ ├── 01_top_10_filiais_preco_popular.png
│ ├── 02_comparacao_concorrente_preco_popular.png
│ ├── 03_distribuicao_preco_popular.png
│ └── 04_top_10_produtos_ean.png
├── sql/
│ └── create_tables.sql
├── src/
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│ ├── analyze.py
│ └── main.py
├── requirements.txt
└── README.md
```

---

## Descrição das Etapas

### Extração (`extract.py`)
- Lê os arquivos Excel de origem
- Salva os dados na camada **raw**, sem transformações
- Preserva os dados originais para rastreabilidade

### Transformação (`transform.py`)
- Cria a dimensão **filial**
- Cria a tabela fato de vendas
- Renomeia colunas, remove duplicidades e ajusta tipos
- Salva os dados tratados na pasta **processed**

### Carga (`load.py`)
- Conecta ao PostgreSQL
- Insere dados na tabela `dim_filial` evitando duplicidade
- Insere os dados de vendas na tabela `fato_vendas`

### Análise (`analyze.py`)
- Consulta os dados carregados no banco
- Gera gráficos de apoio à análise:
  - Top 10 filiais por vendas
  - Comparação entre concorrente e preço popular
  - Distribuição de vendas de preço popular
  - Top 10 produtos (EAN)
- Salva os gráficos na pasta `plots`

### Orquestração (`main.py`)
- Controla a execução do pipeline completo
- Executa as etapas na seguinte ordem:
  1. Extração
  2. Transformação
  3. Carga
  4. Análise

---

## Requisitos

- Python 3.10 ou superior
- PostgreSQL em execução

Instalação das dependências:
```bash
pip install -r requirements.txt
```

### Banco de Dados

Crie um banco no PostgreSQL (exemplo: `etl_vendas`).

Execute o script `sql/create_tables.sql`.

Configure as variáveis de ambiente, se necessário:

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

## Como Executar

Coloque os arquivos Excel na pasta `data/raw`.

No diretório raiz do projeto, execute:

```bash
python main.py
```

Ao final da execução:

- Os dados estarão carregados no banco
- Os arquivos transformados estarão em `data/processed`
- Os gráficos estarão disponíveis em `plots`