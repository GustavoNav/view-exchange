import os
import pandas as pd


base_path = os.path.dirname(os.path.abspath(__file__))
historic_file_path = os.path.join(base_path, '..', 'historic.parquet')
general_financials_file_path = os.path.join(base_path, '..', 'general_financials.parquet')
real_time_file_path = os.path.join(base_path,'..', 'real_time.parquet')

df_historic = pd.read_parquet(historic_file_path)
df_general_financials = pd.read_parquet(general_financials_file_path)
df_real_time = pd.read_parquet(real_time_file_path)


type_mapping = {
    'open': float,
    'high': float,
    'low': float,
    'close': float,
    'volume': float,
    'dividends': float,
    'stock_splits': float
}

# Aplicar a conversão para as colunas especificadas
df_historic = df_historic.astype(type_mapping)

df_historic['date_information'] = pd.to_datetime(df_historic['date_information'])
