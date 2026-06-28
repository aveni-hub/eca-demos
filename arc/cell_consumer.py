import random
from avenieca.consumer import Consumer

from eca import *
from config import *

load_dotenv()
data_path = os.getenv("DATA_PATH")
idx = random.randint(1, 900)
cell_log = '%s/cell_%s.txt' % (data_path, idx)

if __name__ == '__main__':
    cell_config = cell_config.broker_config
    cell_writer = ECAIOWriter(
        log=cell_log,
        name="arc_cell")
    cell_consumer = Consumer(config=cell_config)
    print("listening...")
    cell_consumer.consume(cell_writer.write)
