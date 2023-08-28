from enum import Enum


class XDM1041Mode(Enum):
    """
    Enum class to set the states of the meter and to associate __str__ with the command codes
    """

    MODE_VOLTAGE_DC = 2
    MODE_VOLTAGE_AC = 3
    MODE_CURRENT_DC = 4
    MODE_CURRENT_AC = 5
    MODE_RES = 6
    MODE_CONT = 7
    MODE_DIODE = 8
    MODE_CAPACITANCE = 9
    MODE_FREQUENCY = 10
    MODE_PERIOD = 11
    MODE_TEMP = 12

    def __str__(self):

        if self.value == XDM1041Mode.MODE_VOLTAGE_DC.value:
            return "CONF:VOLT:DC\n"

        elif self.value == XDM1041Mode.MODE_VOLTAGE_AC.value:
            return "CONF:VOLT:AC\n"

        elif self.value == XDM1041Mode.MODE_CURRENT_DC.value:
            return "CONF:CURR:DC\n"

        elif self.value == XDM1041Mode.MODE_CURRENT_AC.value:
            return "CONF:CURR:AC\n"

        elif self.value == XDM1041Mode.MODE_RES.value:
            return "CONF:RES\n"

        elif self.value == XDM1041Mode.MODE_CONT.value:
            return "CONF:CONT\n"

        elif self.value == XDM1041Mode.MODE_DIODE.value:
            return "CONF:DIOD\n"

        elif self.value == XDM1041Mode.MODE_CAPACITANCE.value:
            return "CONF:CAP\n"

        elif self.value == XDM1041Mode.MODE_FREQUENCY.value:
            return "CONF:FREQ\n"

        elif self.value == XDM1041Mode.MODE_PERIOD.value:
            return "CONF:PER\n"

        elif self.value == XDM1041Mode.MODE_TEMP.value:
            return "CONF:TEMP\n"


class XDM1041Cmd(Enum):

    IDN = 1

    RATE_S = 13
    RATE_M = 14
    RATE_F = 15

    MEASURE_1 = 16
    MEASURE_2 = 17

    MEASURE_1_RAW = 18
    MEASURE_2_RAW = 19

    SET_RANGE = 20

    def __str__(self):

        if self.value == XDM1041Cmd.IDN.value:
            return "*IDN?\n"

        elif self.value == XDM1041Cmd.RATE_S.value:
            return "RATE S\n"

        elif self.value == XDM1041Cmd.RATE_M.value:
            return "RATE M\n"

        elif self.value == XDM1041Cmd.RATE_F.value:
            return "RATE F\n"

        elif self.value == XDM1041Cmd.MEASURE_1.value:
            return "MEAS1:SHOW?\n"

        elif self.value == XDM1041Cmd.MEASURE_2.value:
            return "MEAS2:SHOW?\n"

        elif self.value == XDM1041Cmd.MEASURE_1_RAW.value:
            return "MEAS1?\n"

        elif self.value == XDM1041Cmd.MEASURE_2_RAW.value:
            return "MEAS2?\n"

        elif self.value == XDM1041Cmd.SET_RANGE.value:
            return "RANGE {}\n"
