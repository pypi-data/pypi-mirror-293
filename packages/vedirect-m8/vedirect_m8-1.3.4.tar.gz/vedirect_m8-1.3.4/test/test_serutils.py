"""
SerialUtils unittest class.

Use pytest package.
"""
from vedirect_m8.serutils import SerialUtils as Ut

__author__ = "Eli Serra"
__copyright__ = "Copyright 2020, Eli Serra"
__deprecated__ = False
__license__ = "MIT"
__status__ = "Production"
__version__ = "1.0.0"


class TestSerialUtils:
    """
    SerialUtils unittest class.

    Use pytest package.
    """
    @staticmethod
    def test_is_key_pattern():
        """Test is_key_pattern method."""
        datas = [
            '_hello', 'hel lo', "#hj_58Hyui#",  # false
            "hj_58Hyui"  # true
        ]
        tests = [x for x in datas if Ut.is_key_pattern(x)]
        assert len(tests) == 1

    @staticmethod
    def test_is_serial_key_pattern():
        """Test is_serial_key_pattern method."""
        datas = [
            '_hello', 'hel lo',  # false
            "hj_58Hyui", "#hj_58Hyui#"  # true
        ]
        tests = [x for x in datas if Ut.is_serial_key_pattern(x)]
        assert len(tests) == 2

    @staticmethod
    def test_is_serial_port_name_pattern():
        """Test is_serial_port_name_pattern method."""
        datas = [
            'USB1', 'ttyUsb1', 'ttyUS1',  # false
            'ACM1', 'ttyAcm1', 'ttyAC1',  # false
            'AMA1', 'ttyAma1', 'ttyAM1',  # false
            "ttyUSB1", "ttyACM1", "ttyAMA1", "vmodem1", "COM1"  # true
        ]
        tests = [x for x in datas if Ut.is_serial_port_name_pattern(x)]
        assert len(tests) == 5

    @staticmethod
    def test_is_unix_serial_port_pattern():
        """Test is_unix_serial_port_pattern method."""
        datas = [
            '/etc/ttyUSB1', "/dev/tty", "/dev/tty1",  # false
            "/dev/ttyACM1", "/dev/ttyUSB3"  # true
        ]
        tests = [x for x in datas if Ut.is_unix_serial_port_pattern(x)]
        assert len(tests) == 2

    @staticmethod
    def test_is_win_serial_port_pattern():
        """Test is_win_serial_port_pattern method."""
        datas = [
            '/etc/ttyUSB1', "/dev/COM3", "/COM3", "COM"  # false
            "COM255", "COM3", "COM0"  # true
        ]
        tests = [x for x in datas if Ut.is_win_serial_port_pattern(x)]
        assert len(tests) == 2
