import os
import numpy as np
import pandas as pd

from ac_consumer import ac_log as air_conditioner_log
from purifier_consumer import purifier_log


def accuracy():
    url = os.path.join(os.getenv("DATA_PATH", "."), "iot_data.csv")

    data = pd.read_csv(url)

    with open(air_conditioner_log) as f:
        ac_log = [line.rstrip('\n') for line in f]
    ac_log_n = [float(ac_log[-1])]
    for x in ac_log[0:len(ac_log)-1]:
        ac_log_n.append(float(x))
    ac_log = ac_log_n

    with open(purifier_log) as f:
        pu_log = [line.rstrip('\n') for line in f]
    pu_log_n = [float(pu_log[-1])]
    for x in pu_log[0:len(pu_log)-1]:
        pu_log_n.append(float(x))
    pu_log = pu_log_n

    ac1 = np.array(data['Air Conditioner'].values).tolist()
    ac2 = ac_log

    pu1 = np.array(data['Purifier'].values).tolist()
    pu2 = pu_log

    ac_cnt = 0
    pu_cnt = 0
    total = len(ac1)

    assert len(pu1) == len(pu2)
    assert len(ac1) == len(ac2)

    print(pu2[0:5])
    print(pu1[0:5])

    for i in range(len(ac1)):
        if ac1[i] == ac2[i]:
            ac_cnt += 1
        if pu1[i] == pu2[i]:
            pu_cnt += 1

    pu_per = (pu_cnt / total) * 100
    ac_per = (ac_cnt / total) * 100

    print("Air conditioner accuracy: ", ac_per)
    print("Purifier: ", pu_per)


if __name__ == '__main__':
    accuracy()
    # rfl()
