import logging
from logging import Logger
from typing import Final, Type, TypeVar

from serial import Serial
from tabulate import tabulate

CMD_PURGE: Final = 0x44
CMD_UPPER_DISPENSE: Final = 0x45
CMD_STATUS: Final = 0x46
CMD_ROM_VERSION: Final = 0x47
CMD_LOWER_DISPENSE: Final = 0x55
CMD_UPPER_AND_LOWER_DISPENSE: Final = 0x56
CMD_UPPER_TEST_DISPENSE: Final = 0x76
CMD_LOWER_TEST_DISPENSE: Final = 0x77

NO_ERROR: Final = 0x30
NORMAL_STOP: Final = 0x31

ACK_TIMEOUT: Final = 0xF1
RESPONSE_TIMEOUT: Final = 0xF2
UNKNOWN_ERROR: Final = 0xFF

ERROR_CODES = {
    0x01: 'Normal stop',
    0x02: 'Pickup error',
    0x03: 'JAM at CHK1,2 Sensor',
    0x04: 'Overflow bill',
    0x05: 'JAM at EXIT Sensor or EJT Sensor',
    0x06: 'JAM at DIV Sensor',
    0x07: 'Undefined command',
    0x08: 'Upper Bill- End',
    0x0A: 'Counting Error(between CHK3,4 Sensor and DIV Sensor) 3BH Note request error',
    0x0C: 'Counting Error(between DIV Sensor and EJT Sensor) 3DH Counting Error(between EJT Sensor and EXIT Sensor) 3FH Reject Tray is not recognized',
    0x10: 'Lower Bill-End',
    0x11: 'Motor Stop',
    0x12: 'JAM at Div Sensor',
    0x13: 'Timeout (From DIV Sensor to EJT Sensor)',
    0x14: 'Over Reject',
    0x15: 'Upper Cassette is not recognized',
    0x16: 'Lower Cassette is not recognized',
    0x17: 'Dispensing timeout',
    0x18: 'JAM at EJT Sensor',
    0x19: 'Diverter solenoid or SOL Sensor error',
    0x1A: 'SOL Sensor error',
    0x1C: 'JAM at CHK3,4 Sensor',
    0x1E: 'Purge error(Jam at Div Sensor)',
    ACK_TIMEOUT: 'ACK timed out',
    RESPONSE_TIMEOUT: 'Response timed out',
    UNKNOWN_ERROR: 'Unknown Error',
}


class CommandMessage:
    """
    Message protocol is dependent on Command and Response of message and
    has a little difference up to the function with specific format.

    BCC can be gotten through exclusive or (XOR) from the start of each message to ETX except BCC.
    """

    EOT: Final[int] = 0x04  # Start of Transmission.
    ID: Final[int] = 0x50  # Communications ID.
    STX: Final[int] = 0x02  # Start of Text.
    CMD: int  # Command.
    ...  # Command Parameter (Variable Length).
    ETX: Final[int] = 0x03  # End of Text.
    BCC: int  # Block Check Character.

    _response_size: int = 7  # SOH, ID, STX, RSP, ERROR, ETX, BCC

    def __init__(self, *_):
        self._compute_bcc()

    @classmethod
    def from_dict(cls, **kwargs: int):
        return cls(*kwargs.values())

    def _compute_bcc(self, *args: int):
        self.BCC = self.EOT
        for data in (self.ID, self.STX, self.CMD, *args, self.ETX):
            self.BCC = self.BCC ^ data

    def _bytes(self, *data: int):
        return ''.join(
            chr(d) for d in (self.EOT, self.ID, self.STX, self.CMD, *data, self.ETX, self.BCC,)
        ).encode('ascii')

    def bytes(self):
        return self._bytes()

    def response_size(self):
        return self._response_size


class ResponseMessage:
    """
    Message protocol is dependent on Command and Response of message and
    has a little difference up to the function with specific format.

    BCC can be gotten through exclusive or (XOR) from the start of each message to ETX except BCC.
    """

    SOH: Final[int] = 0x01  # Start of Header
    ID: Final[int] = 0x50  # Communications ID
    STX: Final[int] = 0x02  # Start of Text
    RSP: int  # Command
    ...  # Response Parameter (Variable Length)
    ERROR: int  # Error Status for Operation
    ...  # Response Parameter (Variable Length)
    ETX: Final[int] = 0x03  # End of Text
    BCC: int  # Block Check Character

    _origin: tuple[int, ...]

    def __init__(self, *response: int):
        self._origin = response
        self._compute_bcc()

    def _compute_bcc(self, *args: int):
        self.BCC = self.SOH
        for data in (self.ID, self.STX, self.RSP, *args, self.ETX):
            self.BCC = self.BCC ^ data

    def is_valid(self):
        return len(self._origin) > 0 and self.BCC == self._origin[-1]

    def as_dict(self):
        return {'error': self.ERROR - 0x30}

    def __repr__(self) -> str:
        return tabulate(
            ((k, v) for k, v in self.as_dict().items()),
            headers=('Name', 'Code'),
            colalign=('left', 'right'),
            tablefmt="pretty"
        )


class PurgeCommand(CommandMessage):
    """
    to purge the unit (to check the operation of the unit by purge of the unit
    and clear path by passing notes to reject tray)
    """
    CMD = CMD_PURGE


class PurgeResponse(ResponseMessage):
    RSP = CMD_PURGE
    ERROR: int  # Error Status for Operation

    def __init__(self, *response: int):
        (self.ERROR,) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.ERROR)


class UpperDispenseCommand(CommandMessage):
    """
    to dispense bills in the Upper Cassette
    (the requested number of notes to dispense is memorized and send the data to LCDM-2000)
    """
    CMD = CMD_UPPER_DISPENSE
    QTY_HIGH: int  # The number of 10`s of the bills to be dispensed from cassette. 0x30~0x36
    QTY_LOW: int  # The number of 1`s  of the bills to be dispensed from cassette. 0x30~0x39
    _response_size = 4 + 2 + 2 + 1 + 1 + 2 + 2  # ..., CHK, EXIT, ERROR, STATUS, REJECT, ...

    def __init__(self, *args):
        assert len(args) >= 2
        (self.QTY_HIGH, self.QTY_LOW) = args[:2]
        super().__init__(*args)

    @classmethod
    def from_dict(cls, qty=0, **_):
        return super().from_dict(
            QTY_HIGH=(qty // 10) + 0x30,
            QTY_LOW=(qty % 10) + 0x30,
        )

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.QTY_HIGH, self.QTY_LOW)

    def _bytes(self, *_):
        return super()._bytes(self.QTY_HIGH, self.QTY_LOW)


class UpperDispenseResponse(ResponseMessage):
    RSP = CMD_UPPER_DISPENSE
    CHK_HIGH: int = 0x30  # 10’s of the requested bills ( CHK1,2 Sensor ) + 0x30
    CHK_LOW: int = 0x30  # 1’s of the requested bills ( CHK1,2 Sensor ) + 0x30
    EXIT_HIGH: int = 0x30  # 10’s of the requested bills ( EXIT Sensor ) + 0x30
    EXIT_LOW: int = 0x30  # 1’s of the requested bills ( EXIT Sensor ) + 0x30
    ERROR: int  # Error Status for Operation
    STATUS: int = 0x30  # Status of upper cassette. 0x30: Enough Notes (Normal), 0x31: Status of Near end.
    REJECT_HIGH: int = 0x30  # 10’s of the rejected bills + 0x30
    REJECT_LOW: int = 0x30  # 1’s of the rejected bills + 0x30

    def __init__(self, *response: int):
        (
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        )

    def as_dict(self):
        return {
            'chk': (self.CHK_HIGH - 0x30 if self.CHK_HIGH > 0 else 0) + 10
                   + (self.CHK_LOW - 0x30 if self.CHK_LOW > 0 else 0),
            'exit': (self.EXIT_HIGH - 0x30 if self.EXIT_HIGH > 0 else 0) + 10
                    + (self.EXIT_LOW - 0x30 if self.EXIT_LOW > 0 else 0),
            'error': self.ERROR - 0x30,
            'status': self.STATUS - 0x30 if self.STATUS > 0 else 0,
            'reject': (self.REJECT_HIGH - 0x30 if self.REJECT_HIGH > 0 else 0) + 10
                      + (self.REJECT_LOW - 0x30 if self.REJECT_LOW > 0 else 0),
        }


class LowerDispenseCommand(CommandMessage):
    """
    to dispense bills in the Lower Cassette
    (the requested number of notes to dispense is memorized and send the data to LCDM-2000)
    """
    CMD = CMD_LOWER_DISPENSE
    QTY_HIGH: int  # The number of 10`s of the bills to be dispensed from cassette. 0x30~0x36
    QTY_LOW: int  # The number of 1`s  of the bills to be dispensed from cassette. 0x30~0x39
    _response_size = 4 + 2 + 2 + 1 + 1 + 2 + 2  # ..., CHK, EXIT, ERROR, STATUS, REJECT, ...

    def __init__(self, *args):
        assert len(args) >= 2
        (self.QTY_HIGH, self.QTY_LOW) = args[:2]
        super().__init__(*args)

    @classmethod
    def from_dict(cls, qty=0, **_):
        return super().from_dict(
            QTY_HIGH=(qty // 10) + 0x30,
            QTY_LOW=(qty % 10) + 0x30,
        )

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.QTY_HIGH, self.QTY_LOW)

    def _bytes(self, *_):
        return super()._bytes(self.QTY_HIGH, self.QTY_LOW)


class LowerDispenseResponse(ResponseMessage):
    RSP = CMD_LOWER_DISPENSE
    CHK_HIGH: int = 0x30  # 10’s of the requested bills ( CHK1,2 Sensor ) + 0x30
    CHK_LOW: int = 0x30  # 1’s of the requested bills ( CHK1,2 Sensor ) + 0x30
    EXIT_HIGH: int = 0x30  # 10’s of the requested bills ( EXIT Sensor ) + 0x30
    EXIT_LOW: int = 0x30  # 1’s of the requested bills ( EXIT Sensor ) + 0x30
    ERROR: int  # Error Status for Operation
    STATUS: int = 0x30  # Status of upper cassette. 0x30: Enough Notes (Normal), 0x31: Status of Near end.
    REJECT_HIGH: int = 0x30  # 10’s of the rejected bills + 0x30
    REJECT_LOW: int = 0x30  # 1’s of the rejected bills + 0x30

    def __init__(self, *response: int):
        (
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        )

    def as_dict(self):
        return {
            'chk': (self.CHK_HIGH - 0x30 if self.CHK_HIGH > 0 else 0) + 10
                   + (self.CHK_LOW - 0x30 if self.CHK_LOW > 0 else 0),
            'exit': (self.EXIT_HIGH - 0x30 if self.EXIT_HIGH > 0 else 0) + 10
                    + (self.EXIT_LOW - 0x30 if self.EXIT_LOW > 0 else 0),
            'error': self.ERROR - 0x30,
            'status': self.STATUS - 0x30 if self.STATUS > 0 else 0,
            'reject': (self.REJECT_HIGH - 0x30 if self.REJECT_HIGH > 0 else 0) + 10
                      + (self.REJECT_LOW - 0x30 if self.REJECT_LOW > 0 else 0),
        }


class UpperAndLowerDispenseCommand(CommandMessage):
    """
    to dispense bills in the Upper and Lower Cassettes
    (the requested number of notes to dispense is memorized and send the data to LCDM-2000)
    """
    CMD = CMD_LOWER_DISPENSE
    QTY_UPPER_HIGH: int  # The number of 10`s of the bills to be dispensed from upper cassette. 0x30~0x36
    QTY_UPPER_LOW: int  # The number of 1`s  of the bills to be dispensed from upper cassette. 0x30~0x39
    QTY_LOWER_HIGH: int  # The number of 10`s of the bills to be dispensed from lower cassette. 0x30~0x36
    QTY_LOWER_LOW: int  # The number of 1`s  of the bills to be dispensed from lower cassette. 0x30~0x39
    _response_size = 4 + 4 + 4 + 1 + 2 + 4 + 2  # ..., CHK, EXIT, ERROR, STATUS, REJECT, ...

    def __init__(self, *args):
        assert len(args) >= 4
        (self.QTY_UPPER_HIGH, self.QTY_UPPER_LOW, self.QTY_LOWER_HIGH, self.QTY_LOWER_LOW) = args[:4]
        super().__init__(*args)

    @classmethod
    def from_dict(cls, qty_upper=0, qty_lower=0, **_):
        return super().from_dict(
            QTY_UPPER_HIGH=(qty_upper // 10) + 0x30,
            QTY_UPPER_LOW=(qty_upper % 10) + 0x30,
            QTY_LOWER_HIGH=(qty_lower // 10) + 0x30,
            QTY_LOWER_LOW=(qty_lower % 10) + 0x30,
        )

    def _compute_bcc(self, *_):
        super()._compute_bcc(self.QTY_UPPER_HIGH, self.QTY_UPPER_LOW, self.QTY_LOWER_HIGH, self.QTY_LOWER_LOW)

    def _bytes(self, *_):
        return super()._bytes(self.QTY_UPPER_HIGH, self.QTY_UPPER_LOW, self.QTY_LOWER_HIGH, self.QTY_LOWER_LOW)


class UpperAndLowerDispenseResponse(ResponseMessage):
    RSP = CMD_UPPER_AND_LOWER_DISPENSE
    CHK_UPPER_HIGH: int = 0x30  # 10’s of the requested bills (upper) ( CHK3,4 Sensor ) + 0x30
    CHK_UPPER_LOW: int = 0x30  # 1’s of the requested bills (upper) ( CHK3,4 Sensor ) + 0x30
    CHK_LOWER_HIGH: int = 0x30  # 10’s of the requested bills (lower) ( CHK3,4 Sensor ) + 0x30
    CHK_LOWER_LOW: int = 0x30  # 1’s of the requested bills (lower) ( CHK3,4 Sensor ) + 0x30
    EXIT_UPPER_HIGH: int = 0x30  # 10’s of the requested bills  (upper) ( EXIT Sensor ) + 0x30
    EXIT_UPPER_LOW: int = 0x30  # 1’s of the requested bills  (upper) ( EXIT Sensor ) + 0x30
    EXIT_LOWER_HIGH: int = 0x30  # 10’s of the requested bills  (lower) ( EXIT Sensor ) + 0x30
    EXIT_LOWER_LOW: int = 0x30  # 1’s of the requested bills  (lower) ( EXIT Sensor ) + 0x30
    ERROR: int  # Error Status for Operation
    STATUS_UPPER: int = 0x30  # Status of upper cassette. 0x30: Enough Notes (Normal), 0x31: Status of Near end.
    STATUS_LOWER: int = 0x30  # Status of lower cassette. 0x30: Enough Notes (Normal), 0x31: Status of Near end.
    REJECT_UPPER_HIGH: int = 0x30  # 10’s of the rejected bills (upper) + 0x30
    REJECT_UPPER_LOW: int = 0x30  # 1’s of the rejected bills (upper) + 0x30
    REJECT_LOWER_HIGH: int = 0x30  # 10’s of the rejected bills (lower) + 0x30
    REJECT_LOWER_LOW: int = 0x30  # 1’s of the rejected bills (lower) + 0x30

    def __init__(self, *response: int):
        (
            self.CHK_UPPER_HIGH, self.CHK_UPPER_LOW, self.CHK_LOWER_HIGH, self.CHK_LOWER_LOW,
            self.EXIT_UPPER_HIGH, self.EXIT_UPPER_LOW, self.EXIT_LOWER_HIGH, self.EXIT_LOWER_LOW,
            self.ERROR, self.STATUS_UPPER, self.STATUS_LOWER,
            self.REJECT_UPPER_HIGH, self.REJECT_UPPER_LOW, self.REJECT_LOWER_HIGH, self.REJECT_LOWER_LOW,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.CHK_UPPER_HIGH, self.CHK_UPPER_LOW, self.CHK_LOWER_HIGH, self.CHK_LOWER_LOW,
            self.EXIT_UPPER_HIGH, self.EXIT_UPPER_LOW, self.EXIT_LOWER_HIGH, self.EXIT_LOWER_LOW,
            self.ERROR, self.STATUS_UPPER, self.STATUS_LOWER,
            self.REJECT_UPPER_HIGH, self.REJECT_UPPER_LOW, self.REJECT_LOWER_HIGH, self.REJECT_LOWER_LOW,
        )

    def as_dict(self):
        return {
            'chk_upper': (self.CHK_UPPER_HIGH - 0x30 if self.CHK_UPPER_HIGH > 0 else 0) + 10
                         + (self.CHK_UPPER_LOW - 0x30 if self.CHK_UPPER_LOW > 0 else 0),
            'chk_lower': (self.CHK_LOWER_HIGH - 0x30 if self.CHK_LOWER_HIGH > 0 else 0) + 10
                         + (self.CHK_LOWER_LOW - 0x30 if self.CHK_LOWER_LOW > 0 else 0),
            'error': self.ERROR - 0x30,
            'status_upper': self.STATUS_UPPER - 0x30 if self.STATUS_UPPER > 0 else 0,
            'status_lower': self.STATUS_LOWER - 0x30 if self.STATUS_LOWER > 0 else 0,
            'reject_upper': (self.REJECT_UPPER_HIGH - 0x30 if self.REJECT_UPPER_HIGH > 0 else 0) + 10
                            + (self.REJECT_UPPER_LOW - 0x30 if self.REJECT_UPPER_LOW > 0 else 0),
            'reject_lower': (self.REJECT_LOWER_HIGH - 0x30 if self.REJECT_LOWER_HIGH > 0 else 0) + 10
                            + (self.REJECT_LOWER_LOW - 0x30 if self.REJECT_LOWER_LOW > 0 else 0),
        }


class UpperTestDispenseCommand(CommandMessage):
    """
    to reject the one bills in the upper cassette to the reject tray
    """
    CMD = CMD_UPPER_TEST_DISPENSE
    _response_size = 4 + 2 + 2 + 1 + 1 + 2 + 2  # ..., CHK, EXIT, ERROR, STATUS, REJECT, ...


class UpperTestDispenseResponse(ResponseMessage):
    RSP = CMD_UPPER_TEST_DISPENSE
    CHK_HIGH: int = 0x30  # 10’s of the requested bills ( CHK1,2 Sensor ) + 0x30
    CHK_LOW: int = 0x30  # 1’s of the requested bills ( CHK1,2 Sensor ) + 0x30
    EXIT_HIGH: int = 0x30  # 10’s of the requested bills ( EXIT Sensor ) + 0x30
    EXIT_LOW: int = 0x30  # 1’s of the requested bills ( EXIT Sensor ) + 0x30
    ERROR: int  # Error Status for Operation
    STATUS: int = 0x30  # Status of upper cassette. 0x30: Enough Notes (Normal), 0x31: Status of Near end.
    REJECT_HIGH: int = 0x30  # 10’s of the rejected bills + 0x30
    REJECT_LOW: int = 0x30  # 1’s of the rejected bills + 0x30

    def __init__(self, *response: int):
        (
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        )

    def as_dict(self):
        return {
            'chk': (self.CHK_HIGH - 0x30 if self.CHK_HIGH > 0 else 0) + 10
                   + (self.CHK_LOW - 0x30 if self.CHK_LOW > 0 else 0),
            'exit': (self.EXIT_HIGH - 0x30 if self.EXIT_HIGH > 0 else 0) + 10
                    + (self.EXIT_LOW - 0x30 if self.EXIT_LOW > 0 else 0),
            'error': self.ERROR - 0x30,
            'status': self.STATUS - 0x30 if self.STATUS > 0 else 0,
            'reject': (self.REJECT_HIGH - 0x30 if self.REJECT_HIGH > 0 else 0) + 10
                      + (self.REJECT_LOW - 0x30 if self.REJECT_LOW > 0 else 0),
        }


class LowerTestDispenseCommand(CommandMessage):
    """
    to reject the one bills in the lower cassette to the reject tray
    """
    CMD = CMD_LOWER_TEST_DISPENSE
    _response_size = 4 + 2 + 2 + 1 + 1 + 2 + 2  # ..., CHK, EXIT, ERROR, STATUS, REJECT, ...


class LowerTestDispenseResponse(ResponseMessage):
    RSP = CMD_LOWER_TEST_DISPENSE
    CHK_HIGH: int = 0x30  # 10’s of the requested bills ( CHK3,4 Sensor ) + 0x30
    CHK_LOW: int = 0x30  # 1’s of the requested bills ( CHK3,4 Sensor ) + 0x30
    EXIT_HIGH: int = 0x30  # 10’s of the requested bills ( EXIT Sensor ) + 0x30
    EXIT_LOW: int = 0x30  # 1’s of the requested bills ( EXIT Sensor ) + 0x30
    ERROR: int  # Error Status for Operation
    STATUS: int = 0x30  # Status of lower cassette. 0x30: Enough Notes (Normal), 0x31: Status of Near end.
    REJECT_HIGH: int = 0x30  # 10’s of the rejected bills + 0x30
    REJECT_LOW: int = 0x30  # 1’s of the rejected bills + 0x30

    def __init__(self, *response: int):
        (
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.CHK_HIGH, self.CHK_LOW,
            self.EXIT_HIGH, self.EXIT_LOW,
            self.ERROR, self.STATUS,
            self.REJECT_HIGH, self.REJECT_LOW,
        )

    def as_dict(self):
        return {
            'chk': (self.CHK_HIGH - 0x30 if self.CHK_HIGH > 0 else 0) + 10
                   + (self.CHK_LOW - 0x30 if self.CHK_LOW > 0 else 0),
            'exit': (self.EXIT_HIGH - 0x30 if self.EXIT_HIGH > 0 else 0) + 10
                    + (self.EXIT_LOW - 0x30 if self.EXIT_LOW > 0 else 0),
            'error': self.ERROR - 0x30,
            'status': self.STATUS - 0x30 if self.STATUS > 0 else 0,
            'reject': (self.REJECT_HIGH - 0x30 if self.REJECT_HIGH > 0 else 0) + 10
                      + (self.REJECT_LOW - 0x30 if self.REJECT_LOW > 0 else 0),
        }


class StatusCommand(CommandMessage):
    """
    to call for the current status of the unit
    and to send RESPONSE of the result to detect troubles mechanism in the format of code
    """
    CMD = CMD_STATUS
    _response_size = 4 + 1 + 1 + 2 + 2  # ..., SKIP, ERROR, SENSOR, ...


"""
SENSOR 0
B0 : CHK SENSOR 1
B1 : CHK SENSOR 2
B2 : DIV SENSOR 1
B3 : DIV SENSOR 2
B4 : EJT SENSOR
B5 : EXIT SENSOR
B6 : NEAREND0 SENSOR
B7 : Always ‘1’

SENSOR 1
B0 : SOL SENSOR
B1 : CASSETTE0 SENSOR
B2 : CASSETTE1 SENSOR
B3 : CHK SENSOR 3
B4 : CHK SENSOR 4
B5 : NEAREND1 SENSOR
B6 : REJECT TRAY S/W
B7 : Not used
"""


class StatusResponse(ResponseMessage):
    RSP = CMD_STATUS
    SKIP: int = 0x30  # SKIP
    ERROR: int  # Error Status for Operation
    SENSOR0: int  # Sensor status
    SENSOR1: int  # Sensor status

    def __init__(self, *response: int):
        (
            self.SKIP, self.ERROR,
            self.SENSOR0, self.SENSOR1,
        ) = response[4:-2]
        super().__init__(*response)

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.SKIP, self.ERROR,
            self.SENSOR0, self.SENSOR1,
        )

    def as_dict(self):
        return {
            'skip': self.SKIP, 'error': self.ERROR,
            'sensor0': self.SENSOR0, 'sensor1': self.SENSOR1,
        }


class RomVersionCommand(CommandMessage):
    """
    to ask for ROM version
    """
    CMD = CMD_ROM_VERSION
    _response_size = 6 + 2 + 3 * 2


class RomVersionResponse(ResponseMessage):
    RSP = CMD_ROM_VERSION
    SKIP1: int = 0x54
    ROM1: int
    ROM2: int
    SKIP2: int = 0x54
    CHECK1: int
    CHECK2: int
    CHECK3: int
    CHECK4: int

    def __init__(self, *response: int):
        (
            self.SKIP1, self.ROM1, self.ROM2, self.SKIP2,
            self.CHECK1, self.CHECK2, self.CHECK3, self.CHECK4,
        ) = response[4:-2]
        super().__init__(*response)
        self.ERROR = NO_ERROR  # unspecified

    def _compute_bcc(self, *_):
        super()._compute_bcc(
            self.SKIP1, self.ROM1, self.ROM2, self.SKIP2,
            self.CHECK1, self.CHECK2, self.CHECK3, self.CHECK4,
        )

    def as_dict(self):
        return {
            'skip1': self.ROM1, 'rom1': self.ROM1, 'rom2': self.ROM2, 'skip2': self.ROM2,
            'check1': self.CHECK1, 'check2': self.CHECK2, 'check3': self.CHECK3, 'check4': self.CHECK4,
        }


class PuloonException(Exception):
    code: int = UNKNOWN_ERROR
    message: str = ERROR_CODES[UNKNOWN_ERROR]
    response: ResponseMessage = None

    def __init__(self, code: int, message: str = '', response: ResponseMessage = None, *args: object):
        self.code = code
        self.message = message or ERROR_CODES.get(code) or ERROR_CODES[UNKNOWN_ERROR]
        self.response = response
        super().__init__(self.code, self.message, self.response, *args)

    def __repr__(self) -> str:
        _repr = f'{self.__class__.__name__}: {hex(self.code)} - {self.message}'
        if self.response:
            _repr += f'\n{repr(self.response)}'
        return _repr


C = TypeVar('C', bound=CommandMessage)
R = TypeVar('R', bound=ResponseMessage)


class PuloonLCDM2000:
    ack: Final = 0x06
    nak: Final = 0x15
    eot: Final = 0x04

    ack_delay = (0.000, 0.050)
    ack_timeout = (0.500, 0.550)
    response_delay = (0.000, 60.000)

    port: Serial
    logger: Logger

    def __init__(self, port: Serial, logger: Logger = None):
        self.port = port
        self.logger = logger or logging.getLogger()

    def _run(self, cmd: CommandMessage, resp_class: Type[R]) -> R:
        for _ in range(3):
            self.logger.debug(f'CMD: {" ".join(hex(b) for b in cmd.bytes())}')
            self.port.write(cmd.bytes())
            self.port.timeout = self.ack_timeout[1]

            ack = self.port.read(1)
            self.logger.debug(f'ACK: {" ".join(hex(b) for b in ack)}')
            if len(ack) > 0 and self.ack == ack[0]:
                break
        else:
            raise PuloonException(ACK_TIMEOUT)

        for _ in range(3):
            self.port.timeout = self.response_delay[1]
            data = self.port.read(cmd.response_size())
            self.logger.debug(f'RSP: {" ".join(hex(b) for b in data)}')
            resp = resp_class(*data)
            if resp.is_valid():
                self.port.write(chr(self.ack).encode('ascii'))
                if resp.ERROR != NO_ERROR and resp.ERROR != NORMAL_STOP:
                    raise PuloonException(resp.ERROR - NO_ERROR, response=resp)
                break
            self.logger.debug(f'\n{repr(resp)}')
            self.port.write(chr(self.nak).encode('ascii'))
        else:
            raise PuloonException(RESPONSE_TIMEOUT)

        return resp

    def purge(self) -> PurgeResponse:
        """
        to purge the unit (to check the operation of the unit by purge of the unit
        and clear path by passing notes to reject tray)
        """
        return self._run(PurgeCommand.from_dict(), PurgeResponse)

    def status(self) -> StatusResponse:
        """
        to call for the current status of the unit
        and to send RESPONSE of the result to detect troubles mechanism in the format of code
        """
        return self._run(StatusCommand.from_dict(), StatusResponse)

    def rom_version(self) -> RomVersionResponse:
        """
        to ask for ROM version
        """
        return self._run(RomVersionCommand.from_dict(), RomVersionResponse)

    def upper_dispense(self, qty: int = 0) -> UpperDispenseResponse:
        """
        to dispense bills in the Upper Cassette
        (the requested number of notes to dispense is memorized and send the data to LCDM-2000)
        """
        assert 0 < qty <= 69, "Quantity should be at least 1 and maximum 69 in total"
        return self._run(UpperDispenseCommand.from_dict(qty), UpperDispenseResponse)

    def lower_dispense(self, qty: int = 0) -> LowerDispenseResponse:
        """
        to dispense bills in the Lower Cassette
        (the requested number of notes to dispense is memorized and send the data to LCDM-2000)
        """
        assert 0 < qty <= 69, "Quantity should be at least 1 and maximum 69 in total"
        return self._run(LowerDispenseCommand.from_dict(qty), LowerDispenseResponse)

    def upper_and_lower_dispense(self, qty_upper: int = 0, qty_lower: int = 0) -> UpperAndLowerDispenseResponse:
        """
        to dispense bills in the Upper and Lower Cassettes
        (the requested number of notes to dispense is memorized and send the data to LCDM-2000)
        """
        assert 0 < qty_upper <= 69, "Quantity upper should be at least 1 and maximum 69 in total"
        assert 0 < qty_lower <= 69, "Quantity lower should be at least 1 and maximum 69 in total"
        return self._run(UpperAndLowerDispenseCommand.from_dict(qty_upper, qty_lower), UpperAndLowerDispenseResponse)

    def upper_test_dispense(self) -> UpperTestDispenseResponse:
        """
        to reject the one bills in the upper cassette to the reject tray
        """
        return self._run(UpperTestDispenseCommand.from_dict(), UpperTestDispenseResponse)

    def lower_test_dispense(self) -> LowerTestDispenseResponse:
        """
        to reject the one bills in the lower cassette to the reject tray
        """
        return self._run(LowerTestDispenseCommand.from_dict(), LowerTestDispenseResponse)
