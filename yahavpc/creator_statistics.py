from data_models import ProjectStatisticsServer
import consts
from utils import create_path_string

import json

def save_statistics(results_path: str,statistics: str):
    path = create_path_string(results_path, consts.STATISTICS_FILE + consts.JSON_EXTENSION,
                               from_current_directory=False)

    stats_dict = json.loads(statistics)
    with open(path, "w") as file:
        json.dump(stats_dict, file)