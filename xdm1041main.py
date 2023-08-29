from xdm1041defs import XDM1041Mode, XDM1041Cmd
import logging
import serial
import time


class XDM1041:
    rng_dcv = {1: "50mV", 2: "500mV", 3: "5V", 4: "50V", 5: "500V", 6: "1000V"}
    rng_acv = {1: "500mV", 2: "5V", 3: "50V", 4: "500V", 5: "750V"}
    rng_dci = {1: "500uA", 2: "5mA", 3: "50mA", 4: "500mA", 5: "5A", 6: "10A"}
    rng_aci = {1: "500uA", 2: "5mA", 3: "50mA", 4: "500mA", 5: "5A", 6: "10A"}
    rng_res = {1: "500\u03A9", 2: "5K\u03A9", 3: "50K\u03A9", 4: "500K\u03A9", 5: "5M\u03A9", 6: "50M\u03A9"}
    rng_cap = {1: "50nF", 2: "500nF", 3: "5\u03BCF", 4: "50\u03BCF", 5: "500\u03BCF", 6: "5mF", 7: "50mF"}
    rng_tmp = {1: "KITS90", 2: "PT100"}

    range_ref_dict = {
        XDM1041Mode.MODE_VOLTAGE_DC: rng_dcv,
        XDM1041Mode.MODE_VOLTAGE_AC: rng_acv,
        XDM1041Mode.MODE_CURRENT_DC: rng_dci,
        XDM1041Mode.MODE_CURRENT_AC: rng_aci,
        XDM1041Mode.MODE_RES: rng_res,
        XDM1041Mode.MODE_CAPACITANCE: rng_cap,
        XDM1041Mode.MODE_TEMP: rng_tmp
    }

    @classmethod
    def show_available_ranges(cls):
        for xdm_mode in cls.range_ref_dict.keys():
            range_dict = cls.range_ref_dict[xdm_mode]
            print("Supported ranges for {}: ".format(xdm_mode.name), end='')
            for key, value in range_dict.items():
                print("{}:{} ".format(key, value), end='')
            print('')

    def __init__(self, mode: XDM1041Mode, rng: int = 0, serial_device="/dev/ttyUSB0"):

        self.mode = mode
        self.logger = logging.getLogger(__name__)

        self.serial = serial.Serial(
            port=serial_device,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
            xonxoff=False,
            writeTimeout=0.5
        )

        self.logger.info("Serial port status:{}".format(self.serial.is_open))

        self.set_mode(mode)
        self.set_range(rng)

    def connect(self):
        """
        """
        if self.serial and self.serial.is_open is False:
            self.serial.open()

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()

    def set_range(self, rng: int) -> bool:

        """
        We must first detect the mode, then ensure the range is within the allowed values
        Name        Type        Range

                                DCV 1(50mV), 2(500mV), 3(5V), 4(50V), 5(500V), 6(1000V)
                                ACV 1(500mV), 2(5V), 3(50V), 4(500V), 5(750V)
                                DCI 1(500uA), 2(5mA), 3(50mA), 4(500mA), 5(5A), 6(10A)
        <range1>    Discrete    ACI 1(500uA), 2(5mA), 3(50mA), 4(500mA), 5(5A), 6(10A)
                                RES 1(500Ω), 2(5KΩ), 3(50KΩ), 4(500KΩ), 5(5MΩ), 6(50MΩ)
                                CAP 1(50nF), 2(500nF), 3(5uF), 4(50uF), 5(500uF), 6(5mF) ,7(50mF)
                                TEMP 1(KITS90),2(PT100)
        """
        if self.mode not in XDM1041.range_ref_dict:
            self.logger.error("Selected mode:{} does not support range selection!".format(self.mode.name))
            return -1

        range_dict = XDM1041.range_ref_dict[self.mode]
        if rng not in range_dict.keys():
            self.logger.error("Selected range: {} is not supported!".format(rng))
            return -1

        # we made it, set the range
        cmd = str(XDM1041Cmd.SET_RANGE).format(rng)
        self.send_cmd(cmd)

    def test_conn(self):
        cmd = str(XDM1041Cmd.IDN)
        self.send_cmd(cmd)
        time.sleep(0.2)
        manuf_info = self.read_result()
        str_to_k = manuf_info.split(',')
        print(str_to_k)

    def send_cmd(self, cmd: str):
        """
        Take one of the string commands and encode it and send it over the wire
        """
        self.serial.write(cmd.encode())

    def read_result(self) -> str:
        """
        Not too much to do here, all the output from the instrument are ascii strings with linefeed
        just read a line and return
        """
        ret_str = self.serial.readline()
        return ret_str.decode()

    def read_val1_raw(self):
        """
        Read the raw value for measurement 1
        """
        cmd = str(XDM1041Cmd.MEASURE_1_RAW)
        self.send_cmd(cmd)
        val_str = self.read_result()
        ret_float = float(val_str)
        return ret_float

    def read_val2_raw(self):
        """
        Read the raw value for measurement 2
        """
        cmd = str(XDM1041Cmd.MEASURE_2_RAW)
        self.send_cmd(cmd)
        val_str = self.read_result()
        ret_float = float(val_str)
        return ret_float

    def read_val1_str(self):
        """
        Read the value for measurement 1 (includes units)
        """
        cmd = str(XDM1041Cmd.MEASURE_1)
        self.send_cmd(cmd)
        val_str = self.read_result()
        return val_str

    def read_val2_str(self):
        """
        Read the value for measurement 2 (includes units)
        """
        cmd = str(XDM1041Cmd.MEASURE_2)
        self.send_cmd(cmd)
        val_str = self.read_result()
        return val_str

    def set_mode(self, mode: XDM1041Mode):
        cmd = str(mode)
        self.send_cmd(cmd)

    def set_sample_speed_slow(self):
        cmd = str(XDM1041Cmd.RATE_S)
        self.send_cmd(cmd)
        time.sleep(0.2)

    def set_sample_speed_med(self):
        cmd = str(XDM1041Cmd.RATE_M)
        self.send_cmd(cmd)
        time.sleep(0.2)

    def set_sample_speed_fast(self):
        cmd = str(XDM1041Cmd.RATE_F)
        self.send_cmd(cmd)
        time.sleep(0.2)

    def set_calc_avg(self):
        """
        Set the CALC function to averaging mode
        """
        cmd = str(XDM1041Cmd.SET_CALC_FUNC_AVG)
        self.send_cmd(cmd)
        time.sleep(0.2)

    def get_calc_avg(self):
        """Get the calculated average"""
        cmd = str(XDM1041Cmd.GET_CALC_AVG)
        self.send_cmd(cmd)
        time.sleep(0.05)
        result = self.read_result()
        result = float(result)
        return result

    def get_calc_min(self):
        """Get the calculated minimum"""
        cmd = str(XDM1041Cmd.GET_CALC_MIN)
        self.send_cmd(cmd)
        time.sleep(0.05)
        result = self.read_result()
        result = float(result)
        return result

    def get_calc_max(self):
        """Get the calculated maximum"""
        cmd = str(XDM1041Cmd.GET_CALC_MAX)
        self.send_cmd(cmd)
        time.sleep(0.05)
        result = self.read_result()
        result = float(result)
        return result
