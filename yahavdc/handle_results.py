"""
Module used to handle the results of a project.
"""
import json
import os
import base64
import zipfile

from .consts import *
from .utils import create_path_string
from .data_models import ReturnedProject


def save_results(returned_project: ReturnedProject, results_path: str):
    """
    Saves an entire project results' in the designated path.

    Args:
        returned_project (ReturnedProject): the results of the project.
        results_path (str): the path in which to store all the results.

    """
    save_results_file(returned_project.results, results_path)
    save_additional_results(returned_project.base64_zipped_additional_results,
                            results_path)


def find_results_free_path(path: str) -> str:
    """
    Searches for an available results' path.
    The purpose of this function is to handle cases when the results'
        path given by the user already exists.

    Args:
        path (str): the results' path given by the user.

    Returns:
        str: the available results' path.

    """
    base_path = path
    counter = 1
    while True:
        try:
            os.makedirs(base_path, mode=0o777)
        except FileExistsError:
            base_path = path + str(counter)
            counter += 1
        else:
            break
    return base_path


def save_results_file(results: dict, results_path: str):
    """
    Saves the results of the project in the designated path.

    Args:
        results (dict): the results of the project.
        results_path (str): the path in which to store the results.

    """
    results_file = create_path_string(results_path,
                                      RESULTS_FILE + JSON_EXTENSION,
                                      from_current_directory=False)
    with open(results_file, 'w') as file:
        json.dump(results, file)


def save_additional_results(z_additional_results: str, results_path: str):
    """
    Saves the additional results of the project in the designated path.

    Args:
        z_additional_results (str): the additional results as a zip file.
        results_path (str): the path in which to store the additional results.

    """
    z_additional_results = base64.b64decode(z_additional_results.encode('utf-8'))
    additional_results_path = create_path_string(results_path,
                                                 ADDITIONAL_RESULTS_DIRECTORY,
                                                 from_current_directory=False)
    os.makedirs(additional_results_path, mode=0o777)
    z_additional_results_path = create_path_string(results_path,
                                                   ZIPPED_ADDITIONAL_RESULTS,
                                                   from_current_directory=False)
    with open(z_additional_results_path, 'wb') as file:
        file.write(z_additional_results)
    with zipfile.ZipFile(z_additional_results_path) as zip_file:
        zip_file.extractall(additional_results_path)

    os.chmod(z_additional_results_path, mode=0o777)
    os.remove(z_additional_results_path)
