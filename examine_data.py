import pandas as pd

# URL da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/19G1wYQUda-zjrtUMaKnksVhhnIujHr1UezcV5Z9IMAg/export?format=csv&gid=0"

def examine_data():
    """Examina os dados para identificar onde aparece 'Total Geral'."""
    try:
        print("Carregando dados...")
        
        # Carregando dados com skiprows=3 como está atualmente
        df = pd.read_csv(
            sheet_url,
            skiprows=3,
            on_bad_lines='skip',
            engine='python',
            encoding='utf-8',
            sep=','
        )
        
        print(f"Total de linhas carregadas: {len(df)}")
        print(f"Colunas: {list(df.columns)}")
        
        # Procurar por "Total Geral" na primeira coluna (assumindo que é a coluna A)
        primeira_coluna = df.columns[0]
        print(f"\nProcurando 'Total Geral' na coluna: {primeira_coluna}")
        
        # Converter para string para busca
        df[primeira_coluna] = df[primeira_coluna].astype(str)
        
        # Encontrar linhas que contêm "Total Geral"
        total_geral_mask = df[primeira_coluna].str.contains('Total Geral', case=False, na=False)
        total_geral_indices = df[total_geral_mask].index.tolist()
        
        if total_geral_indices:
            print(f"\n'Total Geral' encontrado nas linhas (índices): {total_geral_indices}")
            
            for idx in total_geral_indices:
                print(f"\nLinha {idx}:")
                print(df.iloc[idx].to_dict())
                
                # Mostrar algumas linhas ao redor
                print(f"\nContexto (linhas {max(0, idx-2)} a {min(len(df)-1, idx+5)}):")
                context_start = max(0, idx-2)
                context_end = min(len(df), idx+6)
                
                for i in range(context_start, context_end):
                    marker = " >>> " if i == idx else "     "
                    print(f"{marker}Linha {i}: {df.iloc[i][primeira_coluna]}")
        else:
            print("\n'Total Geral' não encontrado na primeira coluna.")
            
            # Vamos verificar as últimas 20 linhas para ver o que tem
            print(f"\nÚltimas 20 linhas da primeira coluna:")
            for i in range(max(0, len(df)-20), len(df)):
                print(f"Linha {i}: {df.iloc[i][primeira_coluna]}")
        
        return df, total_geral_indices
        
    except Exception as e:
        print(f"Erro ao examinar dados: {e}")
        return None, []

if __name__ == "__main__":
    examine_data()