# README para o script de consulta de CNPJ

Este script Python consulta a API da ReceitaWS para obter informações sobre empresas a partir de seus CNPJs e salva os dados em um arquivo Excel.

## Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas Python: `os`, `requests`, `pandas`, `datetime`, `json` , `openpyxl`

Iniciei um ambiente virtual do Python

```bash
python3 -m venv venv
source venv/bin/activate
```

Você pode instalar as bibliotecas necessárias com o seguinte comando:

```bash
pip install requests pandas open openpyxl
```

Para executar o script, siga os seguintes passos:

1. Clone o repositório do script para o seu computador.
2. Abra um terminal na pasta do repositório.
3. Crie um arquivo de texto chamado `cnpjs.txt` na pasta do repositório e adicione os CNPJs que você deseja consultar, um por linha.
4. Execute o seguinte comando no terminal:

```bash
python consulta_cnpj.py
```

5. O script irá consultar a API da ReceitaWS para cada CNPJ no arquivo `cnpjs.txt` e salvar os dados em um arquivo Excel chamado `dados_empresas.xlsx`.
6. O arquivo `dados_empresas.xlsx` será criado na pasta do repositório.

Se você quiser alterar o nome do arquivo de entrada ou saída, basta editar as variáveis `arquivo_cnpjs` e `arquivo_saida` no arquivo `consulta_cnpj.py`.

Lembre-se de que a API da ReceitaWS tem um limite de consultas por dia. Se você atingir esse limite, precisará esperar até o dia seguinte para continuar consultando.
