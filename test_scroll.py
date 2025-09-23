import pandas as pd
from datetime import datetime

def test_table_structure():
    try:
        # URL do Google Sheets
        sheet_url = "https://docs.google.com/spreadsheets/d/19G1wYQUda-zjrtUMaKnksVhhnIujHr1UezcV5Z9IMAg/export?format=csv&gid=0"
        
        print("Carregando dados...")
        df = pd.read_csv(sheet_url)
        
        # Simular o processamento que o app faz
        df.columns = ['Nome Fantasia Filial', 'Nome Fantasia Agente', 'Prorrogado', 'Tipo Doc.', 'Número Doc.', 'AP', 'Retenção IR', 'Líquido', 'Saldo em Aberto', 'Complemento']
        
        # Converter datas
        df['Prorrogado'] = pd.to_datetime(df['Prorrogado'], dayfirst=True, errors='coerce')
        
        # Filtrar setembro 2025
        df_setembro = df[(df['Prorrogado'].dt.year == 2025) & (df['Prorrogado'].dt.month == 9)].copy()
        
        print(f"Registros de setembro 2025: {len(df_setembro)}")
        
        if len(df_setembro) > 0:
            # Simular o agrupamento diário como no app
            df_setembro = df_setembro.sort_values(['Prorrogado', 'Líquido'], ascending=[True, False])
            df_setembro['Data_fmt'] = df_setembro['Prorrogado'].dt.strftime('%d/%m/%Y')
            
            print("\nDatas únicas em setembro 2025:")
            for data_str in df_setembro['Data_fmt'].dropna().unique():
                count = len(df_setembro[df_setembro['Data_fmt'] == data_str])
                print(f"  {data_str}: {count} registros")
                
                # Verificar especificamente 25/09/2025
                if data_str == '25/09/2025':
                    print(f"    ✓ ENCONTRADO: {data_str} com {count} registros")
                    
                    # Mostrar como seria a linha na tabela
                    linha_data = f"Data: {data_str}"
                    print(f"    Texto da linha na tabela: '{linha_data}'")
                    
                    # Testar a regex do JavaScript
                    import re
                    match = re.search(r'Data:\s*(\d{1,2})\/(\d{1,2})\/(\d{4})', linha_data, re.IGNORECASE)
                    if match:
                        dia = int(match.group(1))
                        mes = int(match.group(2))
                        ano = int(match.group(3))
                        print(f"    Regex funcionou: dia={dia}, mes={mes}, ano={ano}")
                    else:
                        print(f"    ❌ Regex NÃO funcionou!")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_table_structure()