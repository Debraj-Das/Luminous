from fastapi import FastAPI
import schedule
from datetime import datetime, timedelta
import random
from predictions.prediction import predict_new_data
from fastapi.middleware.cors import CORSMiddleware
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ist = pytz.timezone('Asia/Kolkata')

predict_solar_power = []
predict_consumption = []
predict_price = []

actual_solar_power = [
    x + random.randint(-100, 100) for x in predict_solar_power]

actual_consumption = [round(x + random.uniform(-0.1, 0.1), 2)
                      for x in predict_consumption]

actual_price = [round(x + random.uniform(-1, 1), 2) for x in predict_price]

saving = [round((actual_solar_power[i]*0.01 - actual_consumption[i])
                * actual_price[i], 2) for i in range(len(predict_solar_power))]


total_saving = 0
for i in range(len(saving)//2):
    total_saving += saving[i]

current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
previous_time = (datetime.now(ist) - timedelta(hours=20)
                 ).strftime('%Y-%m-%d %H:%M:%S')

notification = [{
    'id': 1,
    'message': 'Tomorrow, Can you use less electricity between 10:00 AM to 10:00 PM?',
    'viewed': False,
    'time': f'{current_time}',
}, {
    'id': 2,
    'message': 'You have saved $10.00 today!',
    'viewed': False,
    'time': f'{current_time}',
}, {
    'id': 3,
    'message': 'You can use high electricity device today!',
    'viewed': True,
    'time': f'{previous_time}',
}]


def hourly_prediction():
    current_time = (datetime.now(ist) + timedelta(hours=12)
                    ).strftime('%Y-%m-%d %H:%M')
    predicted_values = predict_new_data(current_time)

    _predict_solar_power = predicted_values[0][0]
    _predict_consumption = predicted_values[0][1]
    _predict_price = predicted_values[0][2]

    _actual_solar_power = _predict_solar_power + random.randint(-20, 20)
    _actual_consumption = _predict_consumption + random.uniform(-0.1, 0.1)
    _actual_price = _predict_price + random.uniform(-1, 1)

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


# intialize the data

for i in range(-11, 13):
    t = (datetime.now(ist) + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M')
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
