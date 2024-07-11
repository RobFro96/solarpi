import argparse
import io
import json
import os
import traceback

DEVICES = [0, 1, 2]
FIELDS = ["p_ac_ausgang", "p_ac_ausgang_gesamt", "i_batterie_laden",
          "i_laden_gesamt", "i_pv_eingang", "i_batterie_entladen"]
FOLDER = "auswertung"
FORMAT = "%.3f"
SEP = "\t"
NEWLINE = "\n"


def main() -> None:
    parser = argparse.ArgumentParser(prog="SolarPi Auswerteprogramm")
    parser.add_argument("monat", help="Monat, welcher ausgewertet werden soll im Format YYMM")
    args = parser.parse_args()
    monat = args.monat

    if len(monat) != 4:
        print("Fehler: Der angegebene Monat hat nicht 4 Zeichen. Format YYMM verwenden!")
        return

    if not os.path.isdir(FOLDER):
        os.mkdir(FOLDER)
        print("Info: Ordner %s/ erstellt." % FOLDER)

    filename = os.path.join(FOLDER, monat + ".tsv")
    auswerte_file = open(filename, "w", encoding="utf8")
    summe = [0] * len(FIELDS) * len(DEVICES)
    count = 0

    header = ["Tag"]
    for device in DEVICES:
        for field in FIELDS:
            header.append(field + str(device))
    auswerte_file.write(SEP.join(header) + NEWLINE)

    for tag in range(1, 32):
        day_filename = os.path.join("data", "%s%02d.txt" % (monat, tag))
        print("Lese Datei %s" % day_filename)
        tageswerte = tag_auswerten(day_filename)
        if tageswerte is None:
            continue

        count += 1
        for i, wert in enumerate(tageswerte):
            summe[i] += wert

        schreibe_zeile(auswerte_file, str(tag), tageswerte)

    if count > 0:
        mittelwerte = [v / count for v in summe]
        schreibe_zeile(auswerte_file, "Mittelwert", mittelwerte)

    auswerte_file.close()


def tag_auswerten(day_filename: str) -> list[float]:
    werte = [0.] * len(FIELDS) * len(DEVICES)
    counts = [0.] * len(DEVICES)

    try:
        with open(day_filename, "r", encoding="utf8") as fp:
            for line in fp:
                obj = json.loads(line)
                device_id = obj["geraet"]
                counts[DEVICES.index(device_id)] += 1
                for field in FIELDS:
                    werte[len(FIELDS) * DEVICES.index(device_id) +
                          FIELDS.index(field)] += obj[field]
    except:
        print("Fehler bei Datei %s:" % day_filename)
        traceback.print_exc()
        return None

    # sicherstellen dass nie durch 0 geteilt wird
    counts = [1 if c == 0 else c for c in counts]

    # teilen aller werte durch die Anzahl
    for d, _ in enumerate(DEVICES):
        for i, _ in enumerate(FIELDS):
            werte[len(FIELDS) * d + i] /= counts[d]

    return werte


def schreibe_zeile(auswerte_file: io.TextIOWrapper, tag: str, tageswerte: list[float]):
    zeile = [tag]
    zeile += [FORMAT % v for v in tageswerte]
    auswerte_file.write(SEP.join(zeile) + NEWLINE)


if __name__ == "__main__":
    main()
