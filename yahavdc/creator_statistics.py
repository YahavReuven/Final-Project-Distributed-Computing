"""
Module used for statistics handling.
"""
import json

import consts
from utils import create_path_string


def save_statistics(results_path: str, statistics: str):
    """
    Saves the statistics of a project.

    Args:
        results_path (str): the path in which to sae the statistics.
        statistics (str): the statistics as passed from the server.

    """
    path = create_path_string(results_path,
                              consts.STATISTICS_FILE + consts.JSON_EXTENSION,
                              from_current_directory=False)

    stats_dict = json.loads(statistics)
    with open(path, "w") as file:
        json.dump(stats_dict, file)
