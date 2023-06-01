import socket
from datetime import datetime

from avenieca.utils.signal import *


class UnitySocket:
    def __init__(self, host="127.0.0.1", port=25001):
        self.sock = None
        self.host = host
        self.port = port

    def connect(self):
        # Socket Tcp Connection.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP connection
        print("starting connection")
        try:
            sock.connect((self.host, self.port))  # To connect ot the given port.
            print("Connected")
            self.sock = sock
        except Exception as e:
            raise "error connecting to socket: {}".format(e)

    def send_data(self, steering_angle, throttle):
        data_01 = str(steering_angle)
        data_02 = str(throttle)
        data = data_01 + ',' + data_02
        self.sock.sendall(data.encode("utf-8"))

    def get_data(self, code=2048):
        arr1 = []
        arr2 = []
        arr3 = []
        try:
            data = "0,0"
            self.sock.sendall(data.encode("utf-8"))
            reply = self.sock.recv(code).decode("utf-8")  # To receive the data
            split_data = reply.split(',')
            arr1.append(split_data[0])
            arr2.append(split_data[1])
            arr3.append(split_data[2])
            steering_angle = float(split_data[0])
            velocity = float(split_data[1])
            throttle = float(split_data[2])
            steering_angle_list = np.array(arr1)
            velocity_list = np.array(arr2)
            throttle_list = np.array(arr3)
            return steering_angle, velocity, throttle
        except Exception as e:
            raise "error getting data: {}".format(e)

    def get_data_drive(self, code=2048):
        arr1 = []
        arr2 = []
        arr3 = []
        try:
            reply = self.sock.recv(code).decode("utf-8")  # To receive the data
            split_data = reply.split(',')
            arr1.append(split_data[0])
            arr2.append(split_data[1])
            arr3.append(split_data[2])
            steering_angle = float(split_data[0])
            velocity = float(split_data[1])
            throttle = float(split_data[2])
            steering_angle_list = np.array(arr1)
            velocity_list = np.array(arr2)
            throttle_list = np.array(arr3)
            return steering_angle, velocity, throttle
        except Exception as e:
            raise "error getting data: {}".format(e)


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

