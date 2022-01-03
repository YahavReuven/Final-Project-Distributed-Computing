import json
import os
import base64
import zipfile

from utils import create_path_string
import consts
from data_models import ReturnedProject


def save_results(returned_project: ReturnedProject, results_path):
    save_results_file(returned_project.results, results_path)
    save_additional_results(returned_project.base64_zipped_additional_results, results_path)


def save_results_file(results: dict, results_path):
    results_file = create_path_string(results_path, consts.RESULTS_FILE + consts.JSON_EXTENSION)

    os.makedirs(results_path, mode=0o777)

    with open(results_file, 'w') as file:
        json.dump(results, file)


def save_additional_results(z_additional_results, results_path):
    z_additional_results = base64.b64decode(z_additional_results.encode('utf-8'))

    additional_results_path = create_path_string(results_path, consts.ADDITIONAL_RESULTS_DIRECTORY,
                                                 from_current_directory=False)

    os.makedirs(additional_results_path, mode=0o777)

    z_additional_results_path = create_path_string(results_path, consts.ZIPPED_ADDITIONAL_RESULTS,
                                                   from_current_directory=False)
    with open(z_additional_results_path, 'wb') as file:
        file.write(z_additional_results)

    with zipfile.ZipFile(z_additional_results_path) as zip_file:
        zip_file.extractall(additional_results_path)

    os.remove(z_additional_results_path)
