from avenieca.consumer import Consumer
from eca import *
from config import *

load_dotenv()
data_path = os.getenv("DATA_PATH")
ac_log = '%s/logs/ac.txt' % data_path

if __name__ == '__main__':
    ac_config = ac_twin_config.broker_config
    ac_writer = ECAIOWriter(
        log=ac_log,
        name="air_conditioner")
    ac_consumer = Consumer(config=ac_config)
    print("listening...")
    ac_consumer.consume(ac_writer.write)
