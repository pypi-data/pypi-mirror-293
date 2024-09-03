import pandas as pd

def organizar_planilha(input_path, output_path, coluna_ordenar):
    """
    Organiza uma planilha por uma coluna específica e salva o resultado em um novo arquivo.

    :param input_path: Caminho para a planilha de entrada (formato .csv ou .xlsx)
    :param output_path: Caminho para salvar a planilha organizada
    :param coluna_ordenar: Nome da coluna pela qual a planilha deve ser organizada
    """
    try:
        # Detecta o tipo do arquivo (csv ou xlsx) e carrega a planilha
        if input_path.endswith('.csv'):
            df = pd.read_csv(input_path)
        elif input_path.endswith('.xlsx'):
            df = pd.read_excel(input_path)
        else:
            raise ValueError("Formato de arquivo não suportado. Use .csv ou .xlsx.")

        # Organiza a planilha pela coluna especificada
        df_organizada = df.sort_values(by=coluna_ordenar)

        # Salva a planilha organizada no formato especificado
        if output_path.endswith('.csv'):
            df_organizada.to_csv(output_path, index=False)
        elif output_path.endswith('.xlsx'):
            df_organizada.to_excel(output_path, index=False)
        else:
            raise ValueError("Formato de arquivo de saída não suportado. Use .csv ou .xlsx.")

        print(f"Planilha organizada salva em: {output_path}")

    except Exception as e:
        print(f"Ocorreu um erro ao organizar a planilha: {e}")
