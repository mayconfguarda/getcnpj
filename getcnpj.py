import os
import requests
import pandas as pd
from datetime import datetime
from json.decoder import JSONDecodeError
from requests.exceptions import RequestException
import time

def consultar_api_cnpj(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                return dados
            elif response.status_code == 429:  # Too Many Requests
                print(f"API retornou 'Too many requests'. Aguardando até obter status 200...")
            else:
                print(f"Erro ao consultar CNPJ {cnpj}. Status Code: {response.status_code}")
            # Aguarda um curto período de tempo antes de tentar novamente
            time.sleep(1)
        except RequestException as e:
            print(f"Erro ao consultar CNPJ {cnpj}: {e}")
            # Aguarda um curto período de tempo antes de tentar novamente
            time.sleep(1)
        except JSONDecodeError:
            print(f"Erro ao decodificar JSON para CNPJ {cnpj}")
            # Aguarda um curto período de tempo antes de tentar novamente
            time.sleep(1)

def criar_excel(dados, output_file='dados_empresas.xlsx'):
    if not os.path.exists(output_file):
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
        while dados_empresa is None:
            dados_empresa = consultar_api_cnpj(cnpj)

        criar_excel(dados_empresa, arquivo_saida)
        time.sleep(0.5)

def main():
    arquivo_cnpjs = 'cnpjs.txt'
    data_atual = datetime.now().strftime("%Y%m%d%H%M%S")
    arquivo_saida = f'dados_empresas_{data_atual}.xlsx'
    processar_cnpjs_arquivo(arquivo_cnpjs, arquivo_saida)
    print(f'Arquivo final: {arquivo_saida}')

if __name__ == "__main__":
    main()
