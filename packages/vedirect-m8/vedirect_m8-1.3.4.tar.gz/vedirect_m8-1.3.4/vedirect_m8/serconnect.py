# -*- coding: utf-8 -*-
"""
Connect to serial port.

Contain method to scan all available ports.

 .. see also: Vedirect, VedirectController
 Raise:
  - SerialConfException,
  - OpenSerialVeException
  - SerialVeException
"""
import logging
import os
from typing import Optional, Union
from serial import Serial, SerialException
import serial.tools.list_ports as serial_list_ports
from ve_utils.usys import USys
from vedirect_m8.serutils import SerialUtils as Ut
from vedirect_m8.exceptions import SerialConfException
from vedirect_m8.exceptions import OpenSerialVeException
from vedirect_m8.exceptions import SerialVeException

__author__ = "Eli Serra"
__copyright__ = "Copyright 2020, Eli Serra"
__license__ = "MIT"

logging.basicConfig()
logger = logging.getLogger("vedirect")


class SerialConnection:
    """
        Serial connection tool. Set up connection to serial port.

        Able to scan serial ports available on system.

        If you are working with VeDirect protocol,
        remember the configuration :
            - Baud rate : 19200
            - Data bits : 8
            - Parity: None
            - Stop bits: 1
            - Flow Control None
    """
    def __init__(self,
                 serial_port: Optional[str] = None,
                 baud: int = 19200,
                 timeout: Union[int, float] = 0,
                 source_name: str = 'void'
                 ):
        """
        Constructor of SerialConnection class.

        :Example:
            >>> sc = SerialConnection(serial_port = "/dev/ttyUSB1")
            >>> sc.connect()
            >>> True # if connection opened on serial port "/dev/tyyUSB1"
        :param self: Refer to the object instance itself,
        :param serial_port: The serial port to connect,
        :param baud: Baud rate such as 9600 or 115200 etc.
        :param timeout: Set a read timeout value in seconds,
        :param source_name: This is used in logger
         to identify the source of call.
        :return: Nothing
        """
        self._source_name = 'void'
        self._serial_port = None
        self._baud = 19200
        self._timeout = 0
        self.ser = None
        self._init_settings(serial_port=serial_port,
                            baud=baud,
                            timeout=timeout,
                            source_name=source_name)

    def get_serial_port(self) -> Optional[str]:
        """Return serial_port value from instance."""
        return self._serial_port

    def set_serial_port(self, serial_port: Optional[str]) -> bool:
        """
        Set serial_port value.

        :Example :
            >>> self.set_serial_port(serial_port="/tmp/vmodem0")
            >>> True
        :param serial_port: The serial port to set.
        :return: True if is valid serial_port
        """
        if SerialConnection.is_serial_port(serial_port):
            self._serial_port = serial_port
            return True
        return False

    def set_baud(self, baud: Optional[int]) -> bool:
        """
        Set baud value.

        :Example :
            >>> self.set_baud(baud=19200)
            >>> True
        :param baud: The baud to set.
        :return: True if is valid baud
        """
        if SerialConnection.is_baud(baud):
            self._baud = baud
            return True
        return False

    def get_timeout(self) -> Union[int, float]:
        """Return timeout value from instance."""
        return self._timeout

    def set_timeout(self, timeout: Optional[Union[int, float]]) -> bool:
        """
        Set timeout value.

        :Example :
            >>> self.set_timeout(timeout=0)
            >>> True
        :param timeout: The timeout to set.
        :return: True if is valid timeout
        """
        if SerialConnection.is_timeout(timeout):
            self._timeout = timeout
            return True
        return False

    def set_source_name(self, source_name: Optional[str]) -> bool:
        """
        Set source_name value.

        This is used in logger to identify the source of call.
        When multiple serial connections are defined.
        :Example :
            >>> self.set_source_name(source_name='BMV700')
            >>> True
        :param source_name: The source_name to set.
        :return: True if is valid source_name
        """
        if Ut.is_str(source_name, mini=2):
            self._source_name = source_name
            return True
        return False

    def is_ready(self) -> bool:
        """
        Test if the object is ready.

        :return:
            True if configuration settings are valid
            and if the serial connection is opened.
        """
        return self.is_settings() and self.is_serial_ready()

    def is_serial(self) -> bool:
        """
        Test if is serial connection is Serial Instance.

        :return:
            True if self._ser is an instance of Serial.
        """
        return isinstance(self.ser, Serial)

    def is_serial_ready(self) -> bool:
        """
        Test if is serial connection is ready.

        :return:
            True if self._ser is an instance of Serial
            and if the serial connection is opened.
        """
        return self.is_serial() and self.ser.isOpen()

    def is_settings(self) -> bool:
        """
        Test if class instance has valid configuration settings.

        :return: True if is valid configuration settings.
        """
        return SerialConnection.is_serial_conf(serial_port=self._serial_port,
                                               baud=self._baud,
                                               timeout=self._timeout)

    def _init_settings(self,
                       serial_port: Optional[str] = None,
                       baud: int = 19200,
                       timeout: Optional[Union[int, float]] = 0,
                       source_name: str = 'void'
                       ) -> bool:
        """
        Initialise configuration settings.

        :Example :
            >>> self._init_settings(
            >>>     serial_port="/tmp/vmodem0",
            >>>     baud=19200,
            >>>     timeout=0,
            >>>     source_name="BMV700"
            >>> )
            >>> True
        :param serial_port: The serial port
        :param baud: The serial baud rate
        :param timeout: The serial timeout
        :param source_name: The source_name.
        :return: True if configuration settings are valid.
        """
        self.set_serial_port(serial_port)
        self.set_baud(baud)
        self.set_timeout(timeout)
        self.set_source_name(source_name)
        return self.is_settings()

    def _set_serial_conf(self,
                         serial_port: Optional[str] = "default",
                         baud: Optional[int] = None,
                         timeout: Optional[Union[int, float]] = -1,
                         write_timeout: Optional[Union[int, float]] = -1,
                         exclusive: bool = False
                         ) -> Optional[dict]:
        """
        Set serial configuration settings to open serial connection.

        :Example :
            >>> self._set_serial_conf(
            >>>     serial_port="/tmp/vmodem0",
            >>>     baud=19200,
            >>>     timeout=0,
            >>>     write_timeout=0,
            >>>     exclusive=True
            >>> )
            >>> True
        :param serial_port: The serial port
        :param baud: The serial baud rate
        :param timeout: The serial timeout
        :param write_timeout: The serial write timeout
        :param exclusive: Set exclusive access mode (POSIX only).
            A port cannot be opened in exclusive access mode
            if it is already open in exclusive access mode.
        :return:
            a dictionary with the configuration to open a serial connection.
            Or None if a parameter is invalid.
        """
        if (serial_port != "default"
                and not SerialConnection.is_serial_port(serial_port))\
                or (baud is not None
                    and not SerialConnection.is_baud(baud))\
                or (timeout != -1
                    and not SerialConnection.is_timeout(timeout))\
                or (write_timeout != -1
                    and not SerialConnection.is_timeout(write_timeout)):
            result = None
        else:
            self.set_serial_port(serial_port)
            self.set_baud(baud)
            self.set_timeout(timeout)

            result = {
                'port': self._serial_port,
                'baudrate': self._baud,
                'timeout': self._timeout
            }
            if SerialConnection.is_timeout(write_timeout):
                result.update({'write_timeout': write_timeout})
            if Ut.str_to_bool(exclusive) is True:
                result.update({'exclusive': True})
        return result

    def close(self) -> bool:
        """Close serial connection"""
        result = False
        if self.is_serial():
            self.ser.close()
            result = True
        return result
    
    def close_end(self) -> bool:
        """Close and destruct serial connection"""
        result = False
        if self.is_serial():
            self.ser.close()
            self.ser.__del__()
            result = True
        return result

    def connect(self,
                serial_port: Optional[str] = "default",
                baud: Optional[int] = None,
                timeout: Optional[Union[int, float]] = -1,
                write_timeout: Optional[Union[int, float]] = -1,
                exclusive: bool = False
                ) -> bool:
        """
        Start serial connection from parameters.

        :Example :
            >>> self.connect(
            >>>     serial_port="/tmp/vmodem0",
            >>>     baud=19200,
            >>>     timeout=0,
            >>>     write_timeout=0,
            >>>     exclusive=True
            >>> )
            >>> True

        :param serial_port: The serial port
        :param baud: The serial baud rate
        :param timeout: The serial timeout
        :param write_timeout: The serial write timeout
        :param exclusive: Set exclusive access mode (POSIX only).
            A port cannot be opened in exclusive access mode
            if it is already open in exclusive access mode.
        :return: True if success to open a serial connection.
        Raise:
         - SerialConfException:
           Will be raised when parameter
           are out of range or invalid,
           e.g. serial_port, baud rate, data bits
         - SerialVeException:
           In case the device can not be found or can not be configured.
         - OpenSerialVeException:
           Will be raised when the device is configured
           but port is not opened.
        """
        serial_conf = self._set_serial_conf(
            serial_port=serial_port,
            baud=baud,
            timeout=timeout,
            write_timeout=write_timeout,
            exclusive=exclusive
        )
        logger.debug(
            '[SerialConnection::connect::%s] '
            'settings : %s',
            self._source_name, serial_conf
        )
        if SerialConnection.is_serial_conf_data(serial_conf):
            try:
                self.ser = Serial(**serial_conf)
                if self.ser.isOpen():
                    logger.info(
                        '[SerialConnection::connect::%s] '
                        'New Serial connection established. '
                        'args : %s.',
                        self._source_name, serial_conf
                    )
                    result = True
                else:
                    raise OpenSerialVeException(
                        f'[SerialConnection::connect::{self._source_name}] '
                        'Unable to open serial connection. args: '
                        f'{serial_conf}'
                    )

            except SerialException as ex:
                raise SerialVeException(
                    f'[SerialConnection::connect::{self._source_name}] '
                    'Exception when attempting to open serial connection. '
                    f' args: {serial_conf} - ex : {ex}'
                ) from SerialException
            except ValueError as ex:
                raise SerialConfException(
                    f'[SerialConnection::connect::{self._source_name}] '
                    'Parameter are out of range, e.g. baud rate, data bits. '
                    f' args: {serial_conf} - ex : {ex}'
                ) from ValueError

        else:
            raise SerialConfException(
                f'[SerialConnection::connect::{self._source_name}] '
                'Unable to open serial connection. '
                f'Invalid configuration : {serial_conf}'
            )

        return result

    def get_serial_ports_list(self) -> list:
        """
        Get all available ports on the machine.

        First get available virtual serial ports on /tmp/ directory.
        Then use serial.tools.list_ports.comports()
        to get available serial ports.

        :Example :
            >>> self.get_serial_ports_list()
            >>> ['/tmp/vmodem0', '/tmp/vmodem1', '/dev/ttyUSB1']
        :return: List of serial ports and virtual serial ports available.
        """
        result = []
        try:
            # scan unix virtual serial ports ports
            result = self.get_unix_virtual_serial_ports_list()
            ports = serial_list_ports.comports()
            for port, desc, hwid in sorted(ports):
                if hwid != 'n/a':
                    result.append(port)
                    logger.debug(
                        "Serial port found : "
                        "%s: %s [%s]",
                        port, desc, hwid
                    )
        except Exception as ex:
            logger.error(
                '[SerialConnection::get_serial_ports_list::%s] '
                'Unable to list serial ports. '
                'exception : %s',
                self._source_name, ex
            )
        return result

    def get_unix_virtual_serial_ports_list(self) -> list:
        """
        Get all available virtual ports from /tmp/ directory.

        The port name must respect the syntax :
            - ttyUSB[0-999]
            - ttyACM[0-999]
            - vmodem[0-999]

        :Example :
            >>> self.get_unix_virtual_serial_ports_list()
            >>> ['/tmp/vmodem0', '/tmp/vmodem1']

        :return: List of virtual serial ports available.
        """
        result = []
        try:
            if USys.is_op_sys_type('unix'):
                for path in SerialConnection._get_virtual_ports_paths():
                    tmp = SerialConnection._scan_path(path)
                    if Ut.is_list(tmp, not_null=True):
                        result = result + tmp
        except Exception as ex:
            logger.error(
                '[SerialConnection::get_unix_virtual_serial_ports_list::%s] '
                'Unable to list serial ports. '
                'exception : %s',
                self._source_name, ex
            )
        return result

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of order
        :rtype: Dict
        """

        return {
            'source_name': self._source_name,
            'serial_port': self._serial_port,
            'baud': self._baud,
            'timeout': self._timeout
        }

    @staticmethod
    def _scan_path(path: str) -> list:
        """Scan path and get serial ports from it."""
        result = None
        if path != "/dev" and os.path.exists(path):
            # get list files from path
            result = []
            for entry in os.scandir(path):
                if not os.path.isdir(entry.path) \
                        and Ut.is_serial_port_name_pattern(entry.name):
                    if os.path.exists(entry.path):
                        result.append(entry.path)
        return result

    @staticmethod
    def get_default_serial_conf(conf: Optional[dict]) -> dict:
        """Get serial configuration data with default values."""
        result = {
            "serial_port": None,
            "baud": 19200,
            "timeout": 0
        }
        if Ut.is_dict(conf, not_null=True):
            serial_conf = Ut.get_items_from_dict(
                data=conf,
                list_keys=["serial_port", "baud", "timeout"]
            )
            if Ut.is_dict(serial_conf, not_null=True):
                result.update(serial_conf)
        return result

    @staticmethod
    def is_serial_conf(serial_port: Optional[str],
                       baud: int,
                       timeout: Union[int, float]) -> bool:
        """
        Test if valid serial configuration settings.

        :Example :
            >>> SerialConnection.is_serial_conf(
            >>>     serial_port="/tmp/vmodem0",
            >>>     baud=19200,
            >>>     timeout=0
            >>> )
            >>> True
        :param serial_port: The serial port,
        :param baud: The baudrate.
        :param timeout: The timeout.
        :return: True if configuration settings are valid
        """
        return SerialConnection.is_serial_port(serial_port) \
            and SerialConnection.is_baud(baud) \
            and SerialConnection.is_timeout(timeout)

    @staticmethod
    def is_serial_conf_data(conf: Optional[dict]) -> bool:
        """
        Test if valid serial configuration settings.

        :Example :
            >>> SerialConnection.is_serial_conf(
            >>>     serial_port="/tmp/vmodem0",
            >>>     baud=19200,
            >>>     timeout=0
            >>> )
            >>> True
        :param conf: The Configuration data
        :return: True if configuration settings are valid
        """
        return Ut.is_dict(conf)\
            and SerialConnection.is_serial_port(
                conf.get('serial_port')) \
            and SerialConnection.is_baud(
                conf.get('baudrate')) \
            and SerialConnection.is_timeout(
                conf.get('timeout'))

    @staticmethod
    def _get_virtual_ports_paths() -> list:
        """
        Return valid virtual serial ports paths.

        :return: list of valid virtual serial ports paths
        """
        return [os.path.expanduser('~')]

    @staticmethod
    def get_virtual_home_serial_port(port: str) -> Optional[str]:
        """
        Return the virtual serial port path from user home directory.

        :Example :
            >>> SerialConnection.get_virtual_home_serial_port(
            >>>     port="vmodem0"
            >>> )
            >>> "/home/${USER}/vmodem0"
        :param port: The port name to join at user home directory.
        :return: the virtual serial port path from user home directory.
                 Or None if port is invalid virtual port name.
        """
        path = None
        if Ut.is_virtual_serial_port_pattern(port):
            path = os.path.join(os.path.expanduser('~'), port)
        return path

    @staticmethod
    def _is_virtual_serial_port(serial_port: str) -> bool:
        """
        Test if is valid virtual serial port.

        First split the serial port in path and port name.
        Then test if serial port is a string, if path and port name are valid.
        :Example :
            >>> SerialConnection._is_virtual_serial_port(
            >>>     serial_port="/tmp/vmodem0"
            >>> )
            >>> True
            >>> SerialConnection._is_virtual_serial_port(
            >>>     serial_port="/run/vmodem0"
            >>> )
            >>> False
        :param serial_port: The serial port to test.
        :return: True if the virtual serial port is valid.
        """
        name, path = SerialConnection._split_serial_port(serial_port)
        return Ut.is_str(serial_port)\
            and path in SerialConnection._get_virtual_ports_paths()\
            and Ut.is_virtual_serial_port_pattern(name)

    @staticmethod
    def _split_serial_port(serial_port: str) -> tuple:
        """
        Return serial port split in name and path.

        :Example :
            >>> SerialConnection._split_serial_port(
            >>>     serial_port="/tmp/vmodem0"
            >>> )
            >>> ('vmodem0', '/tmp')
        :param serial_port: The serial port to split.
        :return: Tuple of name and path.
        """
        name, path = None, None
        if Ut.is_str(serial_port):
            path, name = os.path.split(serial_port)
        return name, path

    @staticmethod
    def is_serial_port_exists(serial_port: str) -> bool:
        """
        Test serial_port path exists.

        :Example :
            >>> SerialConnection.is_serial_port_exists(
            >>>     serial_port="/tmp/vmodem0"
            >>> )
            >>> True
        :param serial_port: The serial port to test.
        :return: True if the serial port path exists and is a string instance.
        """
        return Ut.is_str(serial_port) and os.path.exists(serial_port)

    @staticmethod
    def is_baud(baud: int) -> bool:
        """
        Test if is valid baud rate.

        :Example :
            >>> SerialConnection.is_baud(baud=1200)
            >>> True
        :param baud: The baudrate value to test.
        :return:
            True if the baudrate value is valid
            and is an integer instance.
        """
        return Ut.is_int(baud)\
            and baud in [
               110, 300, 600, 1200,
               2400, 4800, 9600, 14400,
               19200, 38400, 57600, 115200,
               128000, 256000
           ]

    @staticmethod
    def is_timeout(timeout: Optional[Union[int, float]]) -> bool:
        """
        Test if is valid serial read timeout.

        Possible values for the parameter timeout
        which controls the behavior of read():
         - timeout = None:
            wait forever / until requested number of bytes are received.
         - timeout = 0:
            non-blocking mode, return immediately in any case,
            returning zero or more, up to the requested number of bytes
         - timeout = x:
            set timeout to x seconds (float allowed)
            returns immediately when the requested
            number of bytes are available,
            otherwise wait until the timeout expires
            and return all bytes that were received until then.

        :Example :
            >>> SerialConnection.is_timeout(timeout=0)
            >>> True
        :param timeout: The timeout value to test.
        :return: True if is valid read timeout value.
        """
        return (Ut.is_numeric(timeout) and timeout >= 0) or timeout is None

    @staticmethod
    def is_serial_port(serial_port: Optional[str]) -> bool:
        """
        Test if is valid serial port.

        First split the serial port in path and port name.
        Then test if serial port is a string, if path and port name are valid.
        :Example :
            >>> SerialConnection.is_serial_port(
            >>>     serial_port="/tmp/vmodem0"
            >>> )
            >>> True
            >>> SerialConnection.is_serial_port(
            >>>     serial_port="/run/vmodem0"
            >>> )
            >>> False
        :param serial_port: The serial_port to test.
        :return: True if the serial port is valid or None.
        """
        name, path = SerialConnection._split_serial_port(serial_port)
        return (Ut.is_str(serial_port, not_null=True)
                and SerialConnection.is_serial_path(path)
                and Ut.is_serial_port_name_pattern(name)) \
            or serial_port is None

    @staticmethod
    def is_serial_path(path: str) -> bool:
        """
        Test if is valid serial path.

        For win32 systems path must be null (None or "").
        For unix systems path must be
            - /dev
            - or in get_virtual_ports_paths() method.
        :Example :
            >>> SerialConnection.is_serial_path(serial_port="/tmp")
            >>> True
            >>> SerialConnection.is_serial_path(serial_port="/run")
            >>> False
        :param path: The serial port path to test.
        :return: True if the serial port path is valid.
        """
        return (USys.is_op_sys_type('win32')
                and path is None or path == "")\
            or (USys.is_op_sys_type('unix')
                and Ut.is_str(path)
                and (path in SerialConnection._get_virtual_ports_paths()
                     or path == "/dev"))
