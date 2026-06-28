from tqdm import tqdm
import openai
import pandas as pd

from avenieca.api.model import *
from avenieca.api.eca import ECA
from config import *
import utils as util

load_dotenv()
data_path = os.getenv("DATA_PATH")
url = '%s/gwp_data.csv' % data_path


def write_data():
    data = pd.read_csv(url)
    date = data['date'].values
    quarter = data['quarter'].values
    department = data['department'].values
    day = data['day'].values
    team = data['team'].values
    smv = data['smv'].values
    wip = data['wip'].values
    incentive = data['targeted_productivity'].values
    now = data['no_of_workers'].values
    actual_prod = data['actual_productivity'].values
    eca_server = os.getenv("ECA_SERVER")
    eca_secret = os.getenv("ECA_SECRET")
    openai.api_key = openai_key

    config = Config(uri=eca_server, username=username, password=password)
    eca = ECA(config=config)

    for i in tqdm(range(0, len(date))):
        date_ess = util.create_ess_and_sequence(eca, date[i], eca_secret, date_twin_config, openai, True)
        quarter_ess = util.create_ess_and_sequence(eca, quarter[i], eca_secret, quarter_twin_config, openai, True)
        department_ess = util.create_ess_and_sequence(eca, department[i], eca_secret, department_twin_config, openai,
                                                      True)
        day_ess = util.create_ess_and_sequence(eca, day[i], eca_secret, day_twin_config, openai, True)
        team_ess = util.create_ess_and_sequence(eca, [float(team[i])], eca_secret, team_twin_config)
        smv_ess = util.create_ess_and_sequence(eca, [float(smv[i])], eca_secret, smv_twin_config)
        wip_ess = util.create_ess_and_sequence(eca, [float(wip[i])], eca_secret, wip_twin_config)
        incentive_ess = util.create_ess_and_sequence(eca, [float(incentive[i])], eca_secret, incentive_twin_config)
        now_ess = util.create_ess_and_sequence(eca, [float(now[i])], eca_secret, now_twin_config)
        gwp_aggregate_in_twins = [
            date_ess,
            quarter_ess,
            department_ess,
            day_ess,
            team_ess,
            smv_ess,
            wip_ess,
            now_ess,
            incentive_ess
        ]
        gwp_aggregate_insert = ESSInsert(
            module_id=aggregate_config.module_id,
            state=[],
            valence=0.0,
        )
        gwp_aggregate_insert = util.create_aggregate_from_ess(gwp_aggregate_in_twins, gwp_aggregate_insert)
        gwp_aggregate = util.search_insert_ess_and_sequence(eca, gwp_aggregate_insert)
        actual_prod_ess = util.create_ess_and_sequence(eca, [float(actual_prod[i])], eca_secret,
                                                       actual_prod_twin_config)

        gwp_record_in_twins = [
            gwp_aggregate,
            actual_prod_ess
        ]
        gwp_record_insert = ESSInsert(
            module_id=gwp_record_config.module_id,
            state=[],
            valence=0.0
        )
        gwp_record_insert = util.create_aggregate_from_ess(gwp_record_in_twins, gwp_record_insert)
        util.search_insert_ess_and_sequence(eca, gwp_record_insert)


if __name__ == '__main__':
    write_data()
