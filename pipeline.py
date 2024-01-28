#import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
import requests
from bs4 import BeautifulSoup


url='http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'

class DataExtractor:
      def extracao(self, url, table_index=0):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'grd_DXMainTable'})
        df = pd.read_html(str(table), skiprows=0)[0]
        df.columns = df.iloc[0]
        df = df.drop(0)
        return df

      def salva_parquet(self, df, file_name):
        df.columns = df.columns.map(str)
        df.to_parquet(file_name, index=False)


class DataReader:
      def ler_arquivo(self, file_path):
        df = pd.read_parquet(file_path)
        return df

class DataTransformer:
        def transformacao(self, df):
          df['Data'] = pd.to_datetime(df['Data'], format="%d/%m/%Y")
          df.sort_values(by='Data', ascending=True, inplace=True)
          df['Preço - petróleo bruto - Brent (FOB)'] = df['Preço - petróleo bruto - Brent (FOB)'].astype(float).round(2)
          df['Preço - petróleo bruto - Brent (FOB)'] = df['Preço - petróleo bruto - Brent (FOB)']/100
          df.rename(columns={'Data': 'ds', 'Preço - petróleo bruto - Brent (FOB)': 'y'}, inplace=True)
          #df = df.set_index('ds')  #obs: ver se o modelo consegue trabalhar com a data no index. No notebook de análise não estava no index.
          #df.drop(["Unnamed: 2"], inplace=True, axis=1)
          df.dropna(inplace=True)
          df["unique_id"] = 'Brent'
          return df

class TimeSeriesForecasting:
    def __init__(self):
        self.treino = None
        self.valid = None
        self.h = None
        self.model = None
        self.forecast_df = None

    def treino_valid_split(self, df, data_inicio):
        self.treino = df.loc[df['ds'] < data_inicio]
        self.valid = df.loc[df['ds'] >= data_inicio]
        self.h = self.valid.index.nunique()

    def treina_modelo(self, season_length):
        self.model = StatsForecast(models=[AutoARIMA(season_length=30)], freq='D', n_jobs=-1)
        self.model.fit(self.treino)
        return self.model

    def previsao_futura(self, periods):
        last_date = self.treino['ds'].max()

        future_dates = pd.date_range(start=last_date, periods=periods + 1, inclusive='right', freq='D')
        future_df = pd.DataFrame({'ds': future_dates, 'unique_id': 'Brent'})

        self.future_forecast = self.model.predict(periods, level=[90])
        self.future_forecast = self.future_forecast.reset_index().merge(future_df, on=['ds', 'unique_id'], how='left')
        #print(future_forecast.head(12))
        return self.future_forecast

    def salva_previsao(self, df,  nome_arquivo):
        df.columns = df.columns.map(str)
        df.to_parquet(nome_arquivo, index=False)        
        #joblib.dump(self.model, nome_arquivo)

    def orquestracao(self, df,data_inicio, periods):
        self.treino_valid_split(df, data_inicio)
        self.treina_modelo(season_length=30)
        df_previsao = self.previsao_futura(periods)
        self.salva_previsao(df_previsao, 'meu_modelo.parquet')
        return df_previsao
        #self.salva_modelo(nome_arquivo)
    
    def busca_valores(self, data_input):
        predict_df =  self.future_forecast[self.future_forecast['ds'] == data_input]
        return predict_df
          

class DataPipeline:
    def __init__(self):
        self.extractor = DataExtractor()
        self.reader = DataReader()
        self.transformer = DataTransformer()
        self.forecaster = TimeSeriesForecasting()
        #self.forecaster.orquestracao(df, nome_arquivo, data_inicio, periods, season_length)


    def run_pipeline(self, parquet_file, data_inicio, periods):
        # Extraction
        df = self.extractor.extracao(url)
        self.extractor.salva_parquet(df, parquet_file)
        print('salva_parquet')

        # Reading
        df = self.reader.ler_arquivo(parquet_file)
        print('ler_arquivo')

        # Transformation
        df = self.transformer.transformacao(df)
        print('transformacao')

        # Forecasting and Model Saving
        self.forecaster.orquestracao(df, data_inicio, periods)
        print('orquestracao')

    # Function to handle the prediction process
    def predict_oil_price(self, prediction_date):
        #formatted_date = pd.to_datetime(prediction_date).strftime('%Y-%m-%d')
        #model_input = pd.DataFrame({'ds': [formatted_date], 'unique_id': ['Brent']})
        print('predict_oil_price')

        try: 
            df=self.forecaster.busca_valores(prediction_date)
            print(df)
        except Exception as e:
            print(f"Error during model prediction: {e}")
            return None
        
dt_pipe =DataPipeline()
dt_pipe.run_pipeline("df_transf.parquet", '2023-12-05', 60)