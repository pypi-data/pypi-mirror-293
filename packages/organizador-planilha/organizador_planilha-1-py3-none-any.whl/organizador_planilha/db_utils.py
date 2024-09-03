import pandas as pd
from sqlalchemy import create_engine
from openpyxl import Workbook

def sanitize_column_names(df):
    df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '-', regex=True)
    return df

def sanitize_data(df):
    df = df.astype(str).replace({'[^A-Za-z0-9_ ]+': '-'}, regex=True)
    return df

def organizar_planilha(input_path, output_path, coluna_ordenar):
    try:
        if input_path.endswith('.csv'):
            df = pd.read_csv(input_path)
        elif input_path.endswith('.xlsx'):
            df = pd.read_excel(input_path)
        else:
            raise ValueError("Formato de arquivo não suportado. Use .csv ou .xlsx.")

        df_organizada = df.sort_values(by=coluna_ordenar)

        if output_path.endswith('.csv'):
            df_organizada.to_csv(output_path, index=False)
        elif output_path.endswith('.xlsx'):
            df_organizada.to_excel(output_path, index=False)
        else:
            raise ValueError("Formato de arquivo de saída não suportado. Use .csv ou .xlsx.")

        print(f"Planilha organizada salva em: {output_path}")

    except Exception as e:
        print(f"Ocorreu um erro ao organizar a planilha: {e}")

def buscar_planilha(query, banco, servidor, senha, usuario, nome_planilha):
    try:
        engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{servidor}/{banco}')
        with engine.connect() as connection:
            print("Conexão bem-sucedida!")
            df = pd.read_sql(query, connection)
            print("Dados consultados com sucesso!")

            df = sanitize_column_names(df)
            print("Nomes das colunas sanitizados:", df.columns)

            df = sanitize_data(df)
            print("Dados sanitizados")

            excel_file = f"{nome_planilha}.xlsx"

            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, index=False, sheet_name=f'{nome_planilha}_Data')

            print(f"Planilha '{excel_file}' atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados ou atualizar planilha: {e}")
