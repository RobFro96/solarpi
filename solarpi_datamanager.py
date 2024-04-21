import json
import os

from config import config


def get_dataset(date: str) -> dict:
    data_file = os.path.join(config.data_folder, date + ".txt")

    # Generate empty dataset
    dataset = dict()
    for device_id in config.devices:
        dataset[device_id] = dict()
        dataset[device_id][config.data_key_timestr] = list()
        dataset[device_id][config.data_key_time_num] = list()
        for key, _ in config.data_keys:
            dataset[device_id][key] = list()

    # Read file
    with open(data_file, "r", encoding="utf8") as fp:
        for line in fp:
            obj = json.loads(line)

            device_id = obj[config.data_key_device]
            dataset[device_id][config.data_key_timestr].append(obj[config.data_key_timestr])
            dataset[device_id][
                config.data_key_time_num].append(
                obj[config.data_key_time_num])
            for key, _ in config.data_keys:
                dataset[device_id][key].append(obj[key])

    return dataset
