CREATE TABLE IF NOT EXISTS dim_filial (
    id_filial INTEGER PRIMARY KEY,
    nome_brick VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS fato_vendas (
    id_venda SERIAL PRIMARY KEY,
    id_filial INTEGER REFERENCES dim_filial(id_filial),
    ean VARCHAR(50),
    cod_prod_catarinense VARCHAR(50),
    si_concorrente_unidade NUMERIC,
    so_concorrente_unidade NUMERIC,
    so_preco_popular_unidade NUMERIC,
    data_carga TIMESTAMP DEFAULT NOW()
);
