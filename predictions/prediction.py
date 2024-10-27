import pandas as pd
import joblib
import random

model = joblib.load('predictions/model.pkl')
scaler = joblib.load('predictions/scaler.pkl')


def predict_new_data(send_date_str):
    # Convert the user input to datetime and extract features
    input_df = pd.DataFrame([send_date_str], columns=['SendDate'])
    input_df['SendDate'] = pd.to_datetime(input_df['SendDate'])
    input_df['Hour'] = input_df['SendDate'].dt.hour
    input_df['Day'] = input_df['SendDate'].dt.day
    input_df['Month'] = input_df['SendDate'].dt.month

    # Determine if it's daytime or nighttime
    input_df['is_daytime'] = input_df['Hour'].apply(
        lambda x: 1 if 6 <= x < 17 else 0)

    # Preprocess the input
    input_scaled = scaler.transform(
        input_df[['Hour', 'Day', 'Month', 'is_daytime']])

    # Predict using the trained model
    prediction = model.predict(input_scaled)
    if input_df['is_daytime'].iloc[0] == 0:
        prediction[0][0] = random.uniform(0, 150)

    return prediction
