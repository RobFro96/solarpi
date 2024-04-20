import datetime
import json
import logging
import os
import threading
import time
import typing

import coloredlogs
import serial

from config import config

QUERIES = [
    b"QPGS0" + bytes([0x3f, 0xda]),
    b"QPGS1" + bytes([0x2f, 0xfb]),
    b"QPGS2" + bytes([0x1f, 0x98]),
    b"QPGS3" + bytes([0x0f, 0xb9]),
    b"QPGS4" + bytes([0x7f, 0x5e]),
    b"QPGS5" + bytes([0x6f, 0x7f]),
    b"QPGS6" + bytes([0x5f, 0x1c]),
    b"QPGS7" + bytes([0x4f, 0x3d]),
    b"QPGS8" + bytes([0xbe, 0xd2]),
    b"QPGS9" + bytes([0xae, 0xf3])
]


class SerialThread(threading.Thread):
    def __init__(self, event: threading.Event) -> None:
        threading.Thread.__init__(self)
        self.event = event

    def run(self) -> None:
        self.ser = serial.Serial(config.serial_port, config.serial_baudrate,
                                 timeout=config.serial_timeout)

        self.download_data()
        while not self.event.wait(config.update_interval):
            self.download_data()

    def download_data(self) -> None:
        for device_id in config.devices:
            logging.info("Gerät %d anfragen", device_id)
            self.download_device_data(device_id)

    def download_device_data(self, device_id: int) -> None:
        self.ser.write(QUERIES[device_id] + b"\r")
        result = self.ser.read_until(b"\r")

        if not result:
            logging.warning("keine Antwort!")
            return

        result = self.prepare_results(device_id, result)
        logging.debug(result)
        self.store_results(result)

    def prepare_results(self, device_id: int, result: bytes):
        result = result[:-config.trim_result].decode("utf8")
        result = result.split(" ")

        logging.info("len=%d: %r", len(result), result)

        if len(result) != len(config.data_keys):
            logging.warning("Anzahl der Datensegmente stimmen nicht!")

        result_json = dict()
        result_json[config.data_key_timestr] = datetime.datetime.now().strftime("%H:%M:%S")

        time_num = int(datetime.datetime.now().strftime("%H")) + \
            int(datetime.datetime.now().strftime("%M")) / 60 + \
            int(datetime.datetime.now().strftime("%S")) / 3600

        result_json[config.data_key_time_num] = time_num
        result_json[config.data_key_device] = device_id

        for i, value in enumerate(result):
            key = config.data_keys[i][0]
            datatype = config.data_keys[i][1]
            value = self.convert_value(key, datatype, value)
            result_json[key] = value

        return json.dumps(result_json)

    def convert_value(self, key: str, datatype: str, value: str) -> typing.Union[str, int, float]:
        if datatype == "str":
            return value

        if datatype == "int":
            try:
                return int(value)
            except ValueError:
                logging.warning("Fehler beim Umwandeln in int des Feldes %s, Wert %s", key, value)
                return 0

        if datatype == "float":
            try:
                return float(value)
            except ValueError:
                logging.warning("Fehler beim Umwandeln in float des Feldes %s, Wert %s", key, value)
                return 0.0

        return value

    def store_results(self, result: str) -> None:
        filename = datetime.datetime.now().strftime(config.data_filename)
        filepath = os.path.join(config.data_folder, filename)

        try:
            with open(filepath, "a", encoding="utf8") as fp:
                fp.write(result + "\n")
        except:
            logging.exception("Fehler beim Abspeichern!")


if __name__ == "__main__":
    coloredlogs.install(fmt="%(asctime)s,%(msecs)03d %(levelname)-5s "
                        "[%(filename)s:%(lineno)d] %(message)s",
                        datefmt="%Y-%m-%d:%H:%M:%S",
                        level=logging.INFO)

    if not os.path.isdir(config.data_folder):
        os.makedirs(config.data_folder)

    SerialThread(threading.Event()).run()
