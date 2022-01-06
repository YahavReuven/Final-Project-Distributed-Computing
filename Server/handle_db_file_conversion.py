from datetime import datetime, timedelta
import copy

import consts


def datetime_to_str(datetime_: datetime) -> str:
    return datetime_.strftime(consts.DATETIME_FORMAT)


def device_to_device_db(device: dict) -> dict:
    """
    Converts the dict representation of a Device object to its representation
    in the backup database.

    Args:
        device (dict): the dict representation of a Device.
            The function mutates the argument and sets it to be the device's database
            representation.

    Returns:
        dict: the device's database representation.

    """
    device_db = copy.deepcopy(device)
    projects_ids = [project['project_id'] for project in device['projects']]
    device_db.pop('projects')
    device_db['projects_ids'] = projects_ids
    return device_db


def encode_json_recursively(obj):
    if isinstance(obj, datetime):
        return datetime_to_str(obj)
    elif isinstance(obj, timedelta):
        return str(obj)

    if isinstance(obj, dict) or isinstance(obj, list):
        if isinstance(obj, dict):
            temp = obj
            if obj.get('device_id', None):
                return device_to_device_db(obj)
        else:
            temp = {i: val for i, val in enumerate(obj)}
        for i, val in temp.items():
            obj[i] = encode_json_recursively(val)

    return obj


def str_to_date_time(str_datetime: str) -> datetime:
    return datetime.strptime(str_datetime, consts.DATETIME_FORMAT)
