import time

import pandas as pd
from avenieca import Signal
from avenieca.producers import Event

from eca import *
from config import *


def publish_data():
    aqi_broker_config = aqi_twin_config.broker_config
    aqi_event = Event(config=aqi_broker_config)

    temperature_broker_config = temperature_twin_config.broker_config
    temperature_event = Event(config=temperature_broker_config)

    occupancy_broker_config = occupancy_twin_config.broker_config
    occupancy_event = Event(config=occupancy_broker_config)

    ac_broker_config = ac_twin_config.broker_config
    ac_event = Event(config=ac_broker_config)

    purifier_broker_config = purifier_twin_config.broker_config
    purifier_event = Event(config=purifier_broker_config)

    url = '/Users/ogbanugot/Workspace/eca_demos/smart_iot/iot_data.csv'

    data = pd.read_csv(url)
    aqi_data = data['Air Quality Index'].values
    temp_data = data[' Temperature'].values
    occupancy_data = data[' Occupancy'].values
    ac_data = data[' Air Conditioner'].values
    purifier_data = data[' Purifier'].values

    for i in range(0, len(aqi_data)):
        print("sending signal ", i)
        aqi_signal = Signal(
            state=[float(aqi_data[i])]
        )

        temp_signal = Signal(
            state=[float(temp_data[i])]
        )

        occupancy_signal = Signal(
            state=[float(occupancy_data[i])]
        )
        ac_signal = Signal(
            state=[float(ac_data[i])]
        )
        purifier_signal = Signal(
            state=[float(purifier_data[i])]
        )

        future = ac_event.publish(ac_signal)
        _ = future.get(timeout=60)
        logger("ac", "sent")

        future = aqi_event.publish(aqi_signal)
        _ = future.get(timeout=60)
        logger("aqi", "sent")

        future = occupancy_event.publish(occupancy_signal)
        _ = future.get(timeout=60)
        logger("occupancy", "sent")

        future = purifier_event.publish(purifier_signal)
        _ = future.get(timeout=60)
        logger("purifier", "sent")

        future = temperature_event.publish(temp_signal)
        _ = future.get(timeout=60)
        logger("temperature", "sent")

        time.sleep(1)


if __name__ == '__main__':
    publish_data()
