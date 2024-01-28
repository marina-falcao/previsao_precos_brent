import streamlit as st
import pandas as pd
from datetime import datetime


def ler_arquivo(file_path):
  df = pd.read_parquet(file_path)
  df.info()
  #print(df)
  return df
    
# Function to handle the prediction process
def predict_oil_price(predicted_df, date_input):
    #formatted_date = pd.to_datetime(prediction_date).strftime('%Y-%m-%d')
    #model_input = pd.DataFrame({'ds': [formatted_date], 'unique_id': ['Brent']})
    print(date_input)

    try: 
        #date_filter = datetime.strptime(date_input, '%Y/%m/%d')
        predict_df =  predicted_df[predicted_df['ds'].dt.date == date_input]
        return predict_df['AutoARIMA-hi-90'].iloc[0]
    except Exception as e:
        print(f"Error during model prediction: {e}")
        return None





predicted_df = ler_arquivo('meu_modelo.parquet')

#st.title("Oil Price Prediction")
date_input = st.date_input("Select a Date for Prediction:")

# Button to make prediction
if st.button("Predict"):
    prediction = predict_oil_price(predicted_df, date_input)
    if prediction is not None:
        st.write(f"Predicted Oil Price for {date_input}: ${round(float(prediction), 2)}")
    else:
        st.write("Prediction not available for the selected date.")



