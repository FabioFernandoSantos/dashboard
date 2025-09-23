import pandas as pd
from datetime import datetime

def check_dates():
    try:
        # URL do Google Sheets
        sheet_url = "https://docs.google.com/spreadsheets/d/19G1wYQUda-zjrtUMaKnksVhhnIujHr1UezcV5Z9IMAg/export?format=csv&gid=0"
        
        print("Carregando dados...")
        df = pd.read_csv(sheet_url)
        print(f"Total de linhas carregadas: {len(df)}")
        
        # A coluna 'Unnamed: 2' parece conter as datas
        date_column = 'Unnamed: 2'
        
        print(f"\nAnalisando coluna de datas: {date_column}")
        
        # Verificar valores únicos na coluna de data (primeiros 20)
        date_values = df[date_column].dropna().unique()[:20]
        print(f"Primeiros valores de data: {date_values}")
        
        # Tentar converter para datetime
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column], dayfirst=True, errors='coerce')
        
        # Filtrar apenas linhas com datas válidas
        df_with_dates = df_copy.dropna(subset=[date_column])
        print(f"Linhas com datas válidas: {len(df_with_dates)}")
        
        if len(df_with_dates) > 0:
            # Verificar range de datas
            min_date = df_with_dates[date_column].min()
            max_date = df_with_dates[date_column].max()
            print(f"Data mínima: {min_date}")
            print(f"Data máxima: {max_date}")
            
            # Verificar datas de setembro 2025
            setembro_2025 = df_with_dates[
                (df_with_dates[date_column].dt.year == 2025) & 
                (df_with_dates[date_column].dt.month == 9)
            ]
            
            print(f"\nRegistros de setembro 2025: {len(setembro_2025)}")
            
            if len(setembro_2025) > 0:
                print("Datas únicas em setembro 2025:")
                datas_setembro = setembro_2025[date_column].dt.date.unique()
                for data in sorted(datas_setembro):
                    count = len(setembro_2025[setembro_2025[date_column].dt.date == data])
                    print(f"  {data.strftime('%d/%m/%Y')}: {count} registros")
                    
                # Verificar especificamente 25/09/2025
                data_25_09 = setembro_2025[setembro_2025[date_column].dt.date == pd.to_datetime('2025-09-25').date()]
                print(f"\nRegistros para 25/09/2025: {len(data_25_09)}")
                
                if len(data_25_09) > 0:
                    print("Detalhes dos registros de 25/09/2025:")
                    for idx, row in data_25_09.head(5).iterrows():
                        print(f"  Linha {idx}: {row.to_dict()}")
                else:
                    print("Não há registros para 25/09/2025")
                    
                    # Verificar a data mais próxima
                    target_date = pd.to_datetime('2025-09-25')
                    setembro_2025_sorted = setembro_2025.sort_values(date_column)
                    
                    # Encontrar datas antes e depois de 25/09
                    antes = setembro_2025_sorted[setembro_2025_sorted[date_column] < target_date]
                    depois = setembro_2025_sorted[setembro_2025_sorted[date_column] > target_date]
                    
                    if len(antes) > 0:
                        ultima_antes = antes[date_column].max()
                        print(f"Última data antes de 25/09: {ultima_antes.strftime('%d/%m/%Y')}")
                    
                    if len(depois) > 0:
                        primeira_depois = depois[date_column].min()
                        print(f"Primeira data depois de 25/09: {primeira_depois.strftime('%d/%m/%Y')}")
            else:
                print("Nenhum registro encontrado para setembro 2025")
                
                # Verificar que meses estão disponíveis em 2025
                dados_2025 = df_with_dates[df_with_dates[date_column].dt.year == 2025]
                if len(dados_2025) > 0:
                    print("\nMeses disponíveis em 2025:")
                    meses_2025 = dados_2025[date_column].dt.month.unique()
                    for mes in sorted(meses_2025):
                        count = len(dados_2025[dados_2025[date_column].dt.month == mes])
                        nome_mes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1]
                        print(f"  {nome_mes} ({mes}): {count} registros")
                else:
                    print("Nenhum registro encontrado para 2025")
        else:
            print("Nenhuma data válida encontrada")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_dates()