import datetime
import importlib.util
import json
import logging
import os
import threading
import traceback

import coloredlogs
import flask
import werkzeug

import solarpi_datamanager
from config import config


class SolarPiServer(threading.Thread):
    def __init__(self, event: threading.Event) -> None:
        threading.Thread.__init__(self)
        self.event = event

        self.app = flask.Flask(__name__, static_url_path="", static_folder="public/")
        self.server = werkzeug.serving.make_server(
            host=config.server_host,
            port=config.server_port,
            app=self.app,
            threaded=False
        )
        self.app.add_url_rule("/", "index", self.__index)
        self.app.add_url_rule("/visu/<string:name>", view_func=self.__visu,
                              defaults={"date": "today"})
        self.app.add_url_rule("/visu/<string:name>/<string:date>", view_func=self.__visu)

    def __index(self) -> flask.Response:
        return flask.send_file("public/index.html")

    def __visu(self, name: str, date: str) -> flask.Response:
        visu_python_file = "visu_%s.py" % name
        if not os.path.isfile(visu_python_file):
            flask.abort(404)

        if date == "today":
            date = datetime.datetime.now().strftime("%y%m%d")

        data_file = os.path.join(config.data_folder, date + ".txt")
        if not os.path.isfile(data_file):
            flask.abort(404)

        logging.info("Rendere %s mit Daten %s", visu_python_file, data_file)

        try:
            dataset = solarpi_datamanager.get_dataset(date)

            # Import and run python file
            spec = importlib.util.spec_from_file_location("visu", visu_python_file)
            visu = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(visu)
            return visu.render(dataset)
        except:
            response = flask.make_response(traceback.format_exc(), 200)
            response.mimetype = "text/plain"
            return response

    def run(self) -> None:
        self.server.serve_forever()


if __name__ == "__main__":
    coloredlogs.install(fmt="%(asctime)s,%(msecs)03d %(levelname)-5s "
                        "[%(filename)s:%(lineno)d] %(message)s",
                        datefmt="%Y-%m-%d:%H:%M:%S",
                        level=logging.INFO)

    SolarPiServer(threading.Event()).run()
