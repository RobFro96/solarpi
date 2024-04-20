import serial

DATA0 = b"(1 55355535553555 L 00 238.1 49.98 238.1 49.98 0357 0165 007 50.3 001 081 053.2 002 00596 00293 003 10100010 1 3 060 120 20 01 000__\r"
DATA1 = b"(1 55355535553555 L 00 238.6 50.00 238.6 50.00 0238 0131 005 50.4 001 082 053.3 002 00594 00291 003 10100010 1 3 080 120 20 01 000__\r"
DATA2 = b"(0 00000000000000 P 00 000.0 00.00 000.0 00.00 0000 0000 000 00.0 000 000 000.0 002 00619 00303 003 00000000 0 0 010 110 02 00 000__\r"


def main():
    port = serial.Serial("COM3", 2400, timeout=1)
    while True:
        line = port.read_until(b"\r")
        if line.startswith(b"QPGS0"):
            port.write(DATA0)
        elif line.startswith(b"QPGS1"):
            port.write(DATA1)
        elif line.startswith(b"QPGS2"):
            port.write(DATA2)


if __name__ == "__main__":
    main()
