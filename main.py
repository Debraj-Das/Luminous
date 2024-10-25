from fastapi import FastAPI
import schedule
from datetime import datetime, timedelta
import random
from predictions.prediction import predict_new_data

app = FastAPI()


predict_solar_power = [900, 1326, 1138, 973, 1563, 1163, 1562, 1528, 1443, 881,
                       1147, 1012, 1609, 852, 649, 644, 656, 667, 805, 769, 941, 1038, 927, 742]

predict_consumption = [0.47, 0.46, 0.43, 0.43, 0.48, 0.51, 0.46, 0.43, 0.55, 0.44,
                       0.46, 0.48, 0.47, 0.46, 0.46, 0.48, 0.43, 0.45, 0.48, 0.48, 0.5, 0.5, 0.41, 0.42]
predict_price = [5.93, 6.89, 7.06, 8.22, 9.87, 8.5, 6.52, 7.8, 5.0, 6.78, 5.61,
                 6.28, 4.78, 7.21, 4.5, 6.07, 7.32, 5.08, 8.41, 6.65, 8.64, 4.54, 6.59, 5.15]

actual_solar_power = [x + random.randint(-20, 20) for x in predict_solar_power]

actual_consumption = [round(x + random.uniform(-0.1, 0.1), 2)
                      for x in predict_consumption]

actual_price = [round(x + random.uniform(-0.5, 0.5), 2) for x in predict_price]

saving = [round((actual_solar_power[i]*0.01 - actual_consumption[i])
                * actual_price[i], 2) for i in range(len(predict_solar_power))]


total_saving = 0
for i in range(len(saving)//2):
    total_saving += saving[i]

notification = [{
    'id': 1,
    'message': 'Tomorrow, Can you use less electricity between 10:00 AM to 10:00 PM?',
    'viewed': False,
},]


def hourly_prediction():
    current_time = (datetime.now() + timedelta(hours=12)
                    ).strftime('%Y-%m-%d %H:%M')
    predicted_values = predict_new_data(current_time)

    _predict_solar_power = predicted_values[0][0]
    _predict_consumption = predicted_values[0][1]
    _predict_price = predicted_values[0][2]

    _actual_solar_power = _predict_solar_power + random.randint(-20, 20)
    _actual_consumption = _predict_consumption + random.uniform(-0.1, 0.1)
    _actual_price = _predict_price + random.uniform(-0.5, 0.5)

    predict_solar_power.append(_predict_solar_power)
    predict_solar_power.pop(0)
    predict_consumption.append(_predict_consumption)
    predict_consumption.pop(0)
    predict_price.append(_predict_price)
    predict_price.pop(0)

    actual_solar_power.append(_actual_solar_power)
    actual_solar_power.pop(0)
    actual_consumption.append(_actual_consumption)
    actual_consumption.pop(0)
    actual_price.append(_actual_price)
    actual_price.pop(0)

    saving.append(
        round((_actual_solar_power*0.01 - _actual_consumption)*_actual_price, 2))
    saving.pop(0)

    global total_saving
    total_saving += round((actual_solar_power[11]*0.01 -
                           actual_consumption[11])*actual_price[11], 2)


if __name__ == "__main__":
    schedule.every().hour.at(":00").do(hourly_prediction)


@app.get("/")
def read_root():
    res = {}
    res['predict_solar_power'] = predict_solar_power
    res['predict_consumption'] = predict_consumption
    res['predict_price'] = predict_price
    res['actual_solar_power'] = actual_solar_power[:12]
    res['actual_consumption'] = actual_consumption[:12]
    res['actual_price'] = actual_price[:12]
    res['saving'] = saving[:12]
    res['total_saving'] = total_saving
    res['notification'] = notification

    return res

@app.post("/update")
def update(notification_id: int):
    for i in notification:
        if i['id'] == notification_id:
            i['viewed'] = True
    return notification
    