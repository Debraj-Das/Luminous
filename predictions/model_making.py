import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import root_mean_squared_error

df = pd.read_csv("Energy_data.csv")

df['SendDate'] = pd.to_datetime(df['SendDate'])
df['Hour'] = df['SendDate'].dt.hour
df['Day'] = df['SendDate'].dt.day
df['Month'] = df['SendDate'].dt.month


X = df[['Hour', 'Day', 'Month']]  
y = df[['Solar Power (kW)', 'consumptionValue (kW)', 'price']]

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

model = RandomForestRegressor()
model.fit(X_train_scaled, y_train)

val_preds = model.predict(X_val_scaled)

# Calculate RMSE for validation set
rmse_values = {
    'Solar Power (kW)': np.sqrt(root_mean_squared_error(y_val['Solar Power (kW)'], val_preds[:, 0])),
    'Consumption Value (kW)': np.sqrt(root_mean_squared_error(y_val['consumptionValue (kW)'], val_preds[:, 1])),
    'Price': np.sqrt(root_mean_squared_error(y_val['price'], val_preds[:, 2]))
}

print(f"Validation RMSE Values: {rmse_values}")

# Test the model
test_preds = model.predict(X_test_scaled)
# Calculate RMSE for test set
test_rmse_values = {
    'Solar Power (kW)': np.sqrt(root_mean_squared_error(y_test['Solar Power (kW)'], test_preds[:, 0])),
    'Consumption Value (kW)': np.sqrt(root_mean_squared_error(y_test['consumptionValue (kW)'], test_preds[:, 1])),
    'Price': np.sqrt(root_mean_squared_error(y_test['price'], test_preds[:, 2]))
}

print(f"Test RMSE Values: {test_rmse_values}")

import joblib
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')