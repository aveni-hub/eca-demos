from avenieca.consumer import Consumer
from eca import *
from config import *

load_dotenv()
data_path = os.getenv("DATA_PATH")
purifier_log = '%s/logs/purifier.txt' % data_path

if __name__ == '__main__':
    purifier_config = purifier_twin_config.broker_config
    purifier_writer = ECAIOWriter(
        log=purifier_log,
        name="purifier")
    purifier_consumer = Consumer(config=purifier_config)
    print("listening...")
    purifier_consumer.consume(purifier_writer.write)