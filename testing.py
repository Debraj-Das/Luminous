from predictions.prediction import predict_new_data
from datetime import datetime, timedelta
import random

# current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
# future_time = (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d %H:%M')

# predicted_values = predict_new_data(current_time)
# future_values = predict_new_data(future_time)

# print(current_time)
# print(predicted_values[0][0], predicted_values[0][1], predicted_values[0][2])

# print(future_time)
# print(future_values[0][0], future_values[0][1], future_values[0][2])


predict_solar_power = []

predict_consumption = []
predict_price = []

actual_solar_power = []
actual_consumption = []
actual_price = []

saving = []
total_saving = 0

for i in range(-11, 13):
    t = (datetime.now() + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M')
    predicted_values = predict_new_data(t)

    _predict_solar_power = float(round(predicted_values[0][0], 2))
    _predict_consumption = float(round(predicted_values[0][1], 2))
    _predict_price = float(round(predicted_values[0][2], 2))

    _actual_solar_power = round(
        _predict_solar_power + random.randint(-20, 20), 2)
    _actual_consumption = round(
        _predict_consumption + random.uniform(-0.1, 0.1), 2)
    _actual_price = round(_predict_price + random.uniform(-1, 1), 2)

    predict_solar_power.append(_predict_solar_power)
    predict_consumption.append(_predict_consumption)
    predict_price.append(_predict_price)

    actual_solar_power.append(_actual_solar_power)
    actual_consumption.append(_actual_consumption)
    actual_price.append(_actual_price)

    saving.append(
        round((_actual_solar_power*0.01 - _actual_consumption)*_actual_price, 2))
    saving.pop(0)

    total_saving += round((_actual_solar_power*0.01 -
                           _actual_consumption)*_actual_price, 2)


print(len(predict_solar_power))
print(predict_consumption)
print(predict_price)
print(actual_solar_power)
print(actual_consumption)
print(actual_price)
print(saving)
print(total_saving)
