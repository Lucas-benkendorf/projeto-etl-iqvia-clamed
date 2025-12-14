from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from src.analyze import analyze_data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

filial_input = os.path.join(DATA_DIR, "filial-brick_sample.xlsx")
vendas_input = os.path.join(DATA_DIR, "MS_12_2022_sample.xlsx")

filial_raw, vendas_raw = extract_data(
    filial_input, vendas_input, RAW_DIR
)

dim_path, fato_path = transform_data(
    filial_raw, vendas_raw, PROCESSED_DIR
)

load_data(dim_path, fato_path)
analyze_data(PLOTS_DIR)
