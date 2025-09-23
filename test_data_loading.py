import pandas as pd
from datetime import datetime

# URL da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/19G1wYQUda-zjrtUMaKnksVhhnIujHr1UezcV5Z9IMAg/export?format=csv&gid=0"

def test_carregar_dados():
    """Testa o carregamento de dados com tratamento de erro robusto."""
    try:
        print("Tentando carregar dados...")
        
        # Leitura robusta do CSV com tratamento de linhas inconsistentes
        df = pd.read_csv(
            sheet_url,
            skiprows=3,           # Ignora as 3 primeiras linhas
            on_bad_lines='skip',  # Pula linhas com problemas
            engine='python',      # Usa o engine Python para melhor tratamento de erros
            encoding='utf-8',     # Especifica encoding
            sep=','               # Especifica separador
        )
        
        # Verificar se o DataFrame foi carregado corretamente
        if df.empty:
            print("Aviso: DataFrame está vazio após o carregamento")
            return False
        
        print(f"Dados carregados com sucesso: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"Colunas disponíveis: {list(df.columns)}")

        # Filtrar dados: remover linhas a partir de "Total Geral" (inclusive)
        if not df.empty and len(df.columns) > 0:
            primeira_coluna = df.columns[0]
            df[primeira_coluna] = df[primeira_coluna].astype(str)
            
            # Encontrar a primeira ocorrência de "Total Geral" (case insensitive)
            total_geral_mask = df[primeira_coluna].str.contains('Total Geral', case=False, na=False)
            total_geral_indices = df[total_geral_mask].index.tolist()
            
            if total_geral_indices:
                # Pegar o primeiro índice onde aparece "Total Geral"
                primeiro_total_geral = total_geral_indices[0]
                linhas_removidas = len(df) - primeiro_total_geral
                # Filtrar o DataFrame para manter apenas as linhas antes de "Total Geral"
                df = df.iloc[:primeiro_total_geral].copy()
                print(f"Filtrado: removidas {linhas_removidas} linhas a partir de 'Total Geral'")
                print(f"Dados após filtro: {len(df)} linhas")

        # Mostrar primeiras 5 linhas
        print("\nPrimeiras 5 linhas:")
        print(df.head())
        
        return True

    except pd.errors.ParserError as e:
        print(f"Erro de parsing CSV: {e}")
        print("Tentando carregar com configurações alternativas...")
        
        # Tentativa alternativa com configurações mais flexíveis
        try:
            df = pd.read_csv(
                sheet_url,
                on_bad_lines='skip',
                engine='python',
                encoding='utf-8',
                sep=',',
                quotechar='"',
                skipinitialspace=True
            )
            print(f"Carregamento alternativo bem-sucedido: {len(df)} linhas")
            return True
        except Exception as e2:
            print(f"Falha no carregamento alternativo: {e2}")
            return False
            
    except Exception as e:
        print(f"Erro geral ao carregar dados: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_carregar_dados()
    if success:
        print("\n✅ Teste de carregamento de dados: SUCESSO")
    else:
        print("\n❌ Teste de carregamento de dados: FALHA")