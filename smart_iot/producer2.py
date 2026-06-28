import os
import time

import pandas as pd
from avenieca import Signal
from avenieca.producers import Event
from avenieca.api.model import *
from avenieca.api.eca import ECA

from eca import *
from config import *
import utils as util


def publish_data():
    # aqi_broker_config = aqi_twin_config.broker_config
    # aqi_event = Event(config=aqi_broker_config)
    #
    # temperature_broker_config = temperature_twin_config.broker_config
    # temperature_event = Event(config=temperature_broker_config)
    #
    # occupancy_broker_config = occupancy_twin_config.broker_config
    # occupancy_event = Event(config=occupancy_broker_config)
    #
    # ac_broker_config = ac_twin_config.broker_config
    # ac_event = Event(config=ac_broker_config)
    #
    # purifier_broker_config = purifier_twin_config.broker_config
    # purifier_event = Event(config=purifier_broker_config)

    url = os.path.join(os.getenv("DATA_PATH", "."), "iot_data.csv")

    data = pd.read_csv(url)
    aqi_data = data['Air Quality Index'].values
    temp_data = data['Temperature'].values
    occupancy_data = data['Occupancy'].values
    ac_data = data['Air Conditioner'].values
    purifier_data = data['Purifier'].values

    eca_server = os.getenv("ECA_SERVER")

    config = Config(uri=eca_server, username=username, password=password)
    eca = ECA(config)

    for i in range(0, len(aqi_data)):
        print("")
        print("")
        current_time = datetime.now()

        aqi_signal = Signal(
            state=[float(aqi_data[i])]
        )
        util.create_ess_and_sequence(eca, [float(aqi_data[i])], "", aqi_twin_config, None, False)
        print("{}: {} value: {}".format(current_time, "Air Quality Index", aqi_data[i]))

        temp_signal = Signal(
            state=[float(temp_data[i])]
        )
        util.create_ess_and_sequence(eca, [float(temp_data[i])], "", temperature_twin_config, None, False)
        print("{}: {} value: {}".format(current_time, "Temperature", temp_data[i]))

        ac_signal = Signal(
            state=[float(ac_data[i])]
        )
        util.create_ess_and_sequence(eca, [float(ac_data[i])], "", ac_twin_config, None, False)
        print("{}: {} value: {}".format(current_time, "Air Conditioner", ac_data[i]))

        purifier_signal = Signal(
            state=[float(purifier_data[i])]
        )
        util.create_ess_and_sequence(eca, [float(purifier_data[i])], "", purifier_twin_config, None, False)

        # future = ac_event.publish(ac_signal)
        # _ = future.get(timeout=60)
        #
        # future = aqi_event.publish(aqi_signal)
        # _ = future.get(timeout=60)
        #
        # future = purifier_event.publish(purifier_signal)
        # _ = future.get(timeout=60)
        #
        # future = temperature_event.publish(temp_signal)
        # _ = future.get(timeout=60)

        time.sleep(20)


if __name__ == '__main__':
    publish_data()
