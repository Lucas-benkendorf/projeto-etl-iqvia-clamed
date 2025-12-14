import pandas as pd
import os

def transform_data(filial_raw_path, vendas_raw_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    df_filial = pd.read_excel(filial_raw_path)
    df_filial.columns = ["nome_brick", "id_filial"]

    df_filial = (
        df_filial
        .drop_duplicates(subset=["id_filial"])
        [["id_filial", "nome_brick"]]
    )

    dim_path = os.path.join(output_dir, "dim_filial_transformed.xlsx")
    df_filial.to_excel(dim_path, index=False)

    df_vendas = pd.read_excel(vendas_raw_path)

    df_vendas = df_vendas.rename(columns={
        "BRICK": "nome_brick",
        "EAN": "ean",
        "Cod Prod Catarinense": "cod_prod_catarinense",
        "Tipo Informacao SI Bandeira CONCORRENTE Unidade": "si_concorrente_unidade",
        "Tipo Informacao SO Bandeira CONCORRENTE Unidade": "so_concorrente_unidade",
        "Tipo Informacao SO Bandeira PRECO POPULAR Unidade": "so_preco_popular_unidade"
    })

    df_vendas = df_vendas.merge(df_filial, on="nome_brick", how="left")

    df_fato = df_vendas[
        [
            "id_filial",
            "ean",
            "cod_prod_catarinense",
            "si_concorrente_unidade",
            "so_concorrente_unidade",
            "so_preco_popular_unidade"
        ]
    ].copy()

    for col in [
        "si_concorrente_unidade",
        "so_concorrente_unidade",
        "so_preco_popular_unidade"
    ]:
        df_fato[col] = pd.to_numeric(df_fato[col], errors="coerce")

    fato_path = os.path.join(output_dir, "fato_vendas_transformed.xlsx")
    df_fato.to_excel(fato_path, index=False)

    return dim_path, fato_path
