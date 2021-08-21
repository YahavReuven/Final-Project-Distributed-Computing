
import os
import shutil
import json
import base64

from utils import create_path_string
import consts

# TODO: change
def merge_results(project_id: str) -> dict:
    results_path = create_path_string(consts.PROJECTS_DIRECTORY,
                                      project_id,
                                      consts.PROJECT_STORAGE_RESULTS)

    results = dict()

    directories = (os.listdir(results_path)).sort()

    for directory in directories:
        result_path = create_path_string(results_path, directory, 'results', consts.RESULT_FILE)
        with open(result_path, 'r') as file:
            results.update(json.load(file))
            os.remove(results_path)

    return results



def zip_additional_results(project_id) -> str:

    base_results_path = create_path_string(consts.PROJECTS_DIRECTORY,
                                      project_id,
                                      consts.PROJECT_STORAGE_RESULTS)

    returned_results_path = create_path_string(base_results_path, consts.TEMP_PROJECT_ADDITIONAL_RESULTS_DIRECTORY)

    directories = sorted(os.listdir(base_results_path))

    os.makedirs(returned_results_path)

    for directory in directories:
        result_path = create_path_string(base_results_path, directory, 'results', consts.RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY)
        shutil.move(result_path, returned_results_path)
        # TODO: maybe check if empty
        os.rmdir(result_path)

    zipped_results_path = shutil.make_archive(create_path_string(base_results_path, consts.RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY),
                        'zip', returned_results_path)

    with open(zipped_results_path, 'rb') as file:
        zipped_results = file.read()

    zipped_results = base64.b64encode(zipped_results).decode('utf-8')

    return zipped_results



