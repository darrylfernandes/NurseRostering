class Nurse(object):
    def __init__(self, name):
        """

        :param name: Name of the Nurse

        current_shift_state: Entity of type ShiftState
        """
        self.name = name
        self.current_shift_state = ShiftState()


class ShiftState(object):
    def __init__(self):
        """
            Initializes the Nurse's Working Shift State
            shift_state:      Depending on the start day of the month, the day of the week on which the shift
                                    was assigned will be marked.
                                    {"2018-05-20":"Morning", "2018-05-21":None, "2018-05-22": "Night", ...}
            night_shifts_per_month: Incremented by 1 each time a nurse is assigned a night shift
        """
        self.shift_state = {}
        self.night_shifts_per_month = 0

