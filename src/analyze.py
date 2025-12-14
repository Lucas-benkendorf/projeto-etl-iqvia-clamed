import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", "admin"),
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", "5432"),
    database=os.environ.get("DB_NAME", "etl_vendas")
)

def analyze_data(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    engine = create_engine(DATABASE_URL)

    # 1. Top 10 Filiais – Preço Popular
    df_filial = pd.read_sql("""
        SELECT 
            df.nome_brick,
            SUM(fv.so_preco_popular_unidade) AS total_preco_popular
        FROM fato_vendas fv
        JOIN dim_filial df ON fv.id_filial = df.id_filial
        GROUP BY df.nome_brick
        ORDER BY total_preco_popular DESC
        LIMIT 10
    """, engine)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df_filial,
        x="total_preco_popular",
        y="nome_brick"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_top_10_filiais_preco_popular.png"))
    plt.close()

    # 2. Concorrente x Preço Popular
    df_comp = pd.read_sql("""
        SELECT
            SUM(so_concorrente_unidade) AS concorrente,
            SUM(so_preco_popular_unidade) AS preco_popular
        FROM fato_vendas
    """, engine)

    df_comp = df_comp.melt(
        var_name="tipo",
        value_name="total_unidades"
    )

    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=df_comp,
        x="tipo",
        y="total_unidades"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_comparacao_concorrente_preco_popular.png"))
    plt.close()

    # 3. Distribuição de Preço Popular
    df_dist = pd.read_sql("""
        SELECT so_preco_popular_unidade
        FROM fato_vendas
        WHERE so_preco_popular_unidade IS NOT NULL
    """, engine)

    plt.figure(figsize=(10, 6))
    sns.histplot(
        df_dist["so_preco_popular_unidade"],
        bins=30,
        kde=True
    )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_distribuicao_preco_popular.png"))
    plt.close()

    # 4. Top 10 Produtos (EAN)
    df_prod = pd.read_sql("""
        SELECT
            ean,
            SUM(so_preco_popular_unidade) AS total_preco_popular
        FROM fato_vendas
        GROUP BY ean
        ORDER BY total_preco_popular DESC
        LIMIT 10
    """, engine)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df_prod,
        x="total_preco_popular",
        y="ean"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "04_top_10_produtos_ean.png"))
    plt.close()

    return output_dir
