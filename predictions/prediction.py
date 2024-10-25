import pandas as pd
import joblib

model = joblib.load('predictions/model.pkl')
scaler = joblib.load('predictions/scaler.pkl')


def predict_new_data(send_date_str):
    input_df = pd.DataFrame([send_date_str], columns=['SendDate'])
    input_df['SendDate'] = pd.to_datetime(input_df['SendDate'])
    input_df['Hour'] = input_df['SendDate'].dt.hour
    input_df['Day'] = input_df['SendDate'].dt.day
    input_df['Month'] = input_df['SendDate'].dt.month
    input_scaled = scaler.transform(input_df[['Hour', 'Day', 'Month']])
    prediction = model.predict(input_scaled)
    return prediction
