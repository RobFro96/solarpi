import io

import flask
import matplotlib.pyplot as plt


def render(dataset: dict) -> flask.Response:
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(dataset[0]["zeit_num"], dataset[0]["v_batterie"], label="Batteriespannung (V)")
    axis.plot(dataset[0]["zeit_num"], dataset[0]["prozent_batterie"], label="Batterie (%)")
    axis.plot(dataset[0]["zeit_num"], dataset[0]["i_batterie_laden"], label="Laden (A)")
    axis.plot(dataset[0]["zeit_num"], dataset[0]["i_batterie_entladen"], label="Entladen (A)")

    axis.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    axis.set_xlabel("Zeit")

    output = io.BytesIO()
    fig.savefig(output, format="svg", bbox_inches="tight")
    return flask.Response(output.getvalue(), mimetype="image/svg+xml")
