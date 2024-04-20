import logging
import time

import coloredlogs


def main() -> None:
    coloredlogs.install(fmt="%(asctime)s,%(msecs)03d %(levelname)-5s "
                        "[%(filename)s:%(lineno)d] %(message)s",
                        datefmt="%Y-%m-%d:%H:%M:%S",
                        level=logging.INFO)

    while True:
        logging.info("Hallo Welt!")
        time.sleep(5)


if __name__ == "__main__":
    main()
