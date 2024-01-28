# Previsão de preços do petróleo Brent

Criação de um modelo de ML que faça a previsão do preço do petróleo Brent diariamente, além de um dashboard interativo para apresentar insights relevantes sobre a variação do preço do petróleo, como situações geopolíticas, crises econômicas, demanda global por energia, etc. 

A aplicação em Streamlit fornece a previsão do preço do petróleo em data escolhida pelo usuário, considerando aproximadamente 60 dias da data atual. 

# Tecnologias
* Análise: Jupyter Notebook / Python / Pandas
* Pipeline: Python
* Dashboard: Power BI
* MVP: Streamlit

# Getting started

1. Baixar o repositório do projeto - download ZIP. Descompactar o arquivo ZIP. Isso cria a pasta **previsao_precos_brent_main**.
   
2. Abrir a pasta **previsao_precos_brent_main**.

3. Criar virtual environment no diretório escolhido:

   `python -m venv meu_env`
   
4. Ativar o virtual environment:

   `.\meu_env\Scripts\activate`

5. Instalar os requisitos necessários para o projeto:

   `pip install -r requirements.txt`

6. Rodar o arquivo pipeline.py:

   `python .\pipeline.py`

7. Rodar o arquivo streamlit.py:

   `streamlit run streamlit.py`

8. A aplicação estará no endereço:

   {IP da máquina}:8501

9. Para atualizar os dados, executar novamente os itens 6 e 7. 
