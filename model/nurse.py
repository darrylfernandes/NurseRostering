class Nurse(object):
    def __init__(self, name, shift_state):
        """

        :param name: Name of the Nurse
        :param shift_state: Entity of type ShiftState
        """
        self.name = name
        self.shift_state = shift_state


class ShiftState(object):
    def __init__(self):
        """
            Initializes the Nurse's Working Shift State
            week_shift_status:      Depending on the start day of the month, the day of the week on which the shift
                                    was assigned will be marked as True
            night_shifts_per_month: Incremented by 1 each time a nurse is assigned a night shift
            shift_per_day:          Incremented by 1 each time a nurse is assigned either
                                    morning, evening or night shift
        """
        self.shift_per_day = 0
        self.week_shift_status = (False, False, False, False, False, False, False)
        self.night_shifts_per_month = 0
