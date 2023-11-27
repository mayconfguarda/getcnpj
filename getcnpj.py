import os
import requests
import pandas as pd
from datetime import datetime
from json.decoder import JSONDecodeError
from requests.exceptions import RequestException

def consultar_api_cnpj(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        return dados
    except RequestException as e:
        print(f"Erro ao consultar CNPJ {cnpj}: {e}")
        return None
    except JSONDecodeError:
        print(f"Erro ao decodificar JSON para CNPJ {cnpj}")
        return None

def criar_excel(dados, output_file='dados_empresas.xlsx'):
    if not os.path.exists(output_file):
        # Se o arquivo não existe, crie um novo com os dados
        df = pd.DataFrame(columns=['CNPJ', 'Nome', 'Email'])

        if dados:
            nova_linha = {
                'CNPJ': dados.get('cnpj', ''),
                'Nome': dados.get('nome', ''),
                'Email': dados.get('email', ''),
            }
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)

        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f'Dados salvos em {output_file}')
    else:
        # Se o arquivo já existe, carregue-o, adicione uma nova linha e salve-o novamente
        df_existente = pd.read_excel(output_file, engine='openpyxl')

        if dados:
            nova_linha = {
                'CNPJ': dados.get('cnpj', ''),
                'Nome': dados.get('nome', ''),
                'Email': dados.get('email', ''),
            }
            df_atualizado = pd.concat([df_existente, pd.DataFrame([nova_linha])], ignore_index=True)
            df_atualizado.to_excel(output_file, index=False, engine='openpyxl')
            print(f'Dados adicionados ao arquivo {output_file}')
        else:
            print(f'Dados não encontrados. Pulando...')

def processar_cnpjs_arquivo(arquivo, arquivo_saida):
    with open(arquivo, 'r') as file:
        cnpjs = [line.strip() for line in file]

    for cnpj in cnpjs:
        dados_empresa = consultar_api_cnpj(cnpj)
        criar_excel(dados_empresa, arquivo_saida)

def main():
    arquivo_cnpjs = 'cnpjs.txt'  # Substitua pelo nome do seu arquivo de CNPJs
    data_atual = datetime.now().strftime("%Y%m%d%H%M%S")
    arquivo_saida = f'dados_empresas_{data_atual}.xlsx'
    processar_cnpjs_arquivo(arquivo_cnpjs, arquivo_saida)
    print(f'Arquivo final: {arquivo_saida}')

if __name__ == "__main__":
    main()
