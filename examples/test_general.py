from xdm1041defs import XDM1041Mode, XDM1041Cmd
from xdm1041main import XDM1041
import configparser

if __name__ == "__main__":

    XDM1041.show_available_ranges()

    # read in the global app config
    config = configparser.ConfigParser()
    config.read('config.ini')

    ser_device = config.get("SERIAL", "serial_port")

    print("Setting port to:{}".format(ser_device))

    xdm = XDM1041(XDM1041Mode.MODE_VOLTAGE_DC, 1, ser_device)

