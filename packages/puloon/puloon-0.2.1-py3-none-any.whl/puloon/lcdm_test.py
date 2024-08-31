import logging

from serial import Serial

from puloon.lcdm2000 import PuloonLCDM2000

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('lcdm2000')
logger.setLevel(logging.DEBUG)


def main():
    with Serial('COM2', baudrate=9600, timeout=1) as serial:
        puloon = PuloonLCDM2000(serial, logger=logger)
        print(puloon.purge())
        # print(puloon.status())
        # print(puloon.rom_version())
        # print(puloon.upper_dispense(qty1=1, qty2=3))
        # print(puloon.lower_dispense(qty1=2, qty2=5))
        # print(puloon.upper_and_lower_dispense(qty1=0, qty2=7, qty3=1, qty4=9))
        # print(puloon.upper_test_dispense())
        # print(puloon.lower_test_dispense())


if __name__ == '__main__':
    main()
