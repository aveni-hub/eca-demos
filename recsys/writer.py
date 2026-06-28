from tqdm import tqdm
import openai
import pandas as pd

from avenieca.api.model import *
from avenieca.api.eca import ECA
from config import *
import utils as util

load_dotenv()
data_path = os.getenv("DATA_PATH")
url = '%s/events_estore.csv' % data_path


def write_data():
    data = pd.read_csv(url)
    event = data['event'].values
    item = data['item'].values

    eca_server = os.getenv("ECA_SERVER")
    eca_secret = os.getenv("ECA_SECRET")
    openai.api_key = openai_key

    config = Config(uri=eca_server, username=username, password=password)
    eca = ECA(config=config)

    for i in tqdm(range(0, len(event))):
        event_ess = util.create_ess_and_sequence(eca, event[i], eca_secret, event_twin_config, openai, True)
        item_ess = util.create_ess_and_sequence(eca, item[i], eca_secret, item_twin_config, openai, True)

        aggregate_in_twins = [
            event_ess,
            item_ess,
        ]
        aggregate_insert = ESSInsert(
            module_id=aggregate_config.module_id,
            state=[],
            valence=0.0,
        )
        aggregate_insert = util.create_aggregate_from_ess(aggregate_in_twins, aggregate_insert)
        util.search_insert_ess_and_sequence(eca, aggregate_insert)


if __name__ == '__main__':
    write_data()
