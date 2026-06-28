import socket
from datetime import datetime

from avenieca.utils.signal import *


def read(path, mode):
    try:
        f = open(path, mode)
        data = f.read()
        f.close()
        return data
    except Exception as e:
        print("Error: {}".format(e))


def logger(name, mode, data=None):
    current_time = datetime.now()
    print("{}: {} signal {} {}".format(current_time, name, mode, data))


def write(path, mode, data):
    try:
        f = open(path, mode)
        f.write(str(data))
        f.close()
    except Exception as e:
        print("Error: {}".format(e))


class ECAIO:
    def __init__(self, log, name):
        self.name = name
        self.log = log


class ECAIOWriter(ECAIO):
    def __init__(self, log, name):
        super().__init__(log, name)
        self.log = log

    def write(self, data):
        get_state_as_list(data)
        logger(self.name, "received", data)
        data = data["state"][0]
        log = "{}\n".format(data)
        write(self.log, "a", log)


class ECAIOReader(ECAIO):
    def __init__(self, log, name):
        super().__init__(log, name)

    def read(self):
        data = read(self.log, "r")
        signal = {
            "valence": None,
            "score": None,
            "state": np.array([float(data)], dtype=np.float64),
        }
        current_time = datetime.now()
        print("{}: {} signal retrieved {}".format(current_time, self.name, signal))
        return signal
