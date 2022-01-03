import os
import shutil
import json
import base64

from utils import create_path_string
import consts


# TODO: change
def merge_results(project_id: str) -> dict:
    results_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                      consts.PROJECT_STORAGE_RESULTS)

    results = {}

    directories = sorted(os.listdir(results_path))

    for directory in directories:
        result_file = create_path_string(results_path, directory,
                                         consts.RETURNED_TASK_RESULTS_DIRECTORY,
                                         consts.RESULTS_FILE, from_current_directory=False)
        with open(result_file, 'r') as file:
            results.update(json.load(file))

        os.remove(result_file)

    results_json_file = create_path_string(results_path, consts.RESULTS_FILE,
                                           from_current_directory=False)
    with open(results_json_file, 'w') as file:
        os.chmod(results_json_file, mode=0o777)
        json.dump(results, file)

    return results


def zip_additional_results(project_id) -> str:
    base_results_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                           consts.PROJECT_STORAGE_RESULTS)

    temp_results_path = create_path_string(base_results_path,
                                           consts.TEMP_PROJECT_ADDITIONAL_RESULTS_DIRECTORY,
                                           from_current_directory=False)

    os.makedirs(temp_results_path, mode=0o777)

    tasks_storage = sorted(os.listdir(base_results_path))

    for task_directory in tasks_storage:
        # TODO: not sure why this line is here
        if task_directory.isdigit():
            result_path = create_path_string(base_results_path, task_directory,
                                             consts.RETURNED_TASK_RESULTS_DIRECTORY,
                                             consts.RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY,
                                             from_current_directory=False)

            if not os.path.isdir(result_path):
                continue

            additional_results = sorted(os.listdir(result_path))
            for file in additional_results:
                file_path = create_path_string(result_path, file, from_current_directory=False)
                shutil.move(file_path, temp_results_path)
            # TODO: maybe check if empty
            os.rmdir(result_path)

    zipped_results_without_extension = create_path_string(base_results_path,
                                                          consts.RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY,
                                                          from_current_directory=False)
    zipped_results_path = shutil.make_archive(zipped_results_without_extension, 'zip', temp_results_path)

    with open(zipped_results_path, 'rb') as file:
        zipped_results = file.read()

    zipped_results = base64.b64encode(zipped_results).decode('utf-8')

    return zipped_results
