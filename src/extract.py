import pandas as pd
import os

def extract_data(filial_path, vendas_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    df_filial = pd.read_excel(filial_path)
    df_vendas = pd.read_excel(vendas_path)

    filial_raw = os.path.join(output_dir, "filial_raw.xlsx")
    vendas_raw = os.path.join(output_dir, "vendas_raw.xlsx")

    df_filial.to_excel(filial_raw, index=False)
    df_vendas.to_excel(vendas_raw, index=False)

    return filial_raw, vendas_raw
