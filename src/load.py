from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd
import os

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", "admin"),
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", "5432"),
    database=os.environ.get("DB_NAME", "etl_vendas")
)

def load_data(dim_path, fato_path):
    engine = create_engine(DATABASE_URL)

    df_dim = pd.read_excel(dim_path)
    insert_sql = text("""
        INSERT INTO dim_filial (id_filial, nome_brick)
        VALUES (:id_filial, :nome_brick)
        ON CONFLICT (id_filial) DO NOTHING
    """)

    with engine.begin() as conn:
        for _, row in df_dim.iterrows():
            conn.execute(insert_sql, row.to_dict())

    df_fato = pd.read_excel(fato_path)
    df_fato.to_sql("fato_vendas", engine, if_exists="append", index=False)
