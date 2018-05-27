from rules_engine.rules.rule import Rule, wrap_rule_exception
from config.rules_config import NIGHT_SHIFTS_PER_MONTH, CONSECUTIVE_DAYS_SHIFT, MINIMUM_DAYS_OFF_SHIFT
import datetime


class DayShiftRule(Rule):
    """
        In a DayShiftRule, it checks if a nurse is eligible to do a shift. By default, only one shift per day is allowed
    """

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        parent_rule_id = parent_rule.rule_id if parent_rule else None
        parent_rule_description = parent_rule.rule_description if parent_rule else None
        if rule_input:
            nurse = rule_input.get("nurse")
            present_date = rule_input.get("date")
            if not (nurse and present_date):
                return self.rule_id, self.rule_description, False, \
                       "Expected a Rule Input to contain nurse and date to execute the Rule.", \
                       parent_rule_id, parent_rule_description, []
            if not nurse.current_shift_state.shift_state or \
                    (nurse.current_shift_state.shift_state and
                     present_date not in nurse.current_shift_state.shift_state):
                return self.rule_id, self.rule_description, True, "Pass", parent_rule_id, parent_rule_description, []
            else:
                return self.rule_id, self.rule_description, False, \
                       "Nurse {} is already assigned {} shift on {} and hence cannot do more " \
                       "than one shift per day".format(nurse.name,
                                                       nurse.current_shift_state.shift_state.get(
                                                                                present_date), present_date), \
                       parent_rule_id, parent_rule_description, []
        else:
            return self.rule_id, self.rule_description, False, "Expected a Rule Input to execute the Rule.", \
                   parent_rule_id, parent_rule_description, []


class MorningShiftRule(DayShiftRule):
    """
        In a MorningShiftRule, it checks if a nurse is eligible to do a morning shift. If a nurse is already assigned
        a shift either on morning, evening or night, the nurse cannot be assigned another shift within 24 hours.
    """

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        rule_id, rule_description, status, status_reason, parent_rule_id, parent_rule_description, child_rules = \
            super(MorningShiftRule, self).execute(rule_input, parent_rule=parent_rule)
        if status:
            nurse = rule_input.get("nurse")
            present_date = rule_input.get("date")
            previous_day = datetime.datetime.strptime(present_date, '%Y-%m-%d').date() - datetime.timedelta(days=1)
            previous_day_text = previous_day.__str__()
            if not nurse.current_shift_state.shift_state \
                    or (nurse.current_shift_state.shift_state
                        and ((previous_day_text in nurse.current_shift_state.shift_state
                             and ('Morning' == nurse.current_shift_state.shift_state.get(previous_day_text)
                                  or nurse.current_shift_state.shift_state.get(previous_day_text) is None))
                             or previous_day_text not in nurse.current_shift_state.shift_state)):
                return self.rule_id, self.rule_description, True, "Pass", \
                       parent_rule_id, parent_rule_description, child_rules + []
            else:
                return self.rule_id, self.rule_description, False, \
                       "Nurse {} cannot do Morning Shift on {} After a Previous Day's {} shift" \
                           .format(nurse.name, present_date,
                                   nurse.current_shift_state.shift_state.get(previous_day_text)), \
                       parent_rule_id, parent_rule_description, child_rules + []
        else:
            return rule_id, self.rule_description, status, status_reason, \
                   parent_rule_id, parent_rule_description, child_rules + []


class EveningShiftRule(DayShiftRule):
    """
        In a EveningShiftRule, it checks if a nurse is eligible to do an evening shift. If a nurse is already assigned
        a shift either on morning, evening or night, the nurse cannot be assigned another shift within 24 hours.
    """

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        rule_id, rule_description, status, status_reason, parent_rule_id, parent_rule_description, child_rules = \
            super(EveningShiftRule, self).execute(rule_input, parent_rule=parent_rule)
        if status:
            nurse = rule_input.get("nurse")
            present_date = rule_input.get("date")
            previous_day = datetime.datetime.strptime(present_date, '%Y-%m-%d').date() - datetime.timedelta(days=1)
            previous_day_text = previous_day.__str__()
            if not nurse.current_shift_state.shift_state \
                    or (nurse.current_shift_state.shift_state
                        and ((previous_day_text in nurse.current_shift_state.shift_state
                              and (nurse.current_shift_state.shift_state.get(previous_day_text) in ('Evening',
                                                                                                    'Morning')
                                   or nurse.current_shift_state.shift_state.get(previous_day_text) is None))
                             or previous_day_text not in nurse.current_shift_state.shift_state)):
                return self.rule_id, self.rule_description, True, "Pass", \
                       parent_rule_id, parent_rule_description, child_rules + []
            else:
                return self.rule_id, self.rule_description, False, \
                       "Nurse {} cannot do Evening Shift on {} After a Previous Day's {} shift" \
                           .format(nurse.name, present_date,
                                   nurse.current_shift_state.shift_state.get(previous_day_text)), \
                       parent_rule_id, parent_rule_description, child_rules + []
        else:
            return rule_id, rule_description, status, status_reason, \
                   parent_rule_id, parent_rule_description, child_rules + []


class NightShiftRule(DayShiftRule):
    """
        In a NightShiftRule, it checks if a nurse is eligible to do a night shift. If a nurse is already assigned
        a shift either on morning, evening or night, the nurse cannot be assigned another shift on the same day.
        Also, a nurse is not allowed to do more than certain number of night shifts per month.
    """

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        rule_id, rule_description, status, status_reason, parent_rule_id, parent_rule_description, child_rules = \
            super(NightShiftRule, self).execute(rule_input, parent_rule=parent_rule)
        if status:
            nurse = rule_input.get("nurse")
            present_date = rule_input.get("date")
            if nurse.current_shift_state.night_shifts_per_month < NIGHT_SHIFTS_PER_MONTH:
                previous_day = datetime.datetime.strptime(present_date, '%Y-%m-%d').date() - datetime.timedelta(days=1)
                previous_day_text = previous_day.__str__()
                if not nurse.current_shift_state.shift_state \
                        or (nurse.current_shift_state.shift_state
                            and ((previous_day_text in nurse.current_shift_state.shift_state
                                  and (nurse.current_shift_state.shift_state.get(previous_day_text) in ('Night',
                                                                                                        'Evening',
                                                                                                        'Morning')
                                       or nurse.current_shift_state.shift_state.get(previous_day_text) is None))
                                 or previous_day_text not in nurse.current_shift_state.shift_state)):
                    return self.rule_id, self.rule_description, True, "Pass", parent_rule_id, parent_rule_description, child_rules + []
                else:
                    return self.rule_id, self.rule_description, False, \
                           "Nurse {} cannot do Night Shift on {} After Previous Day's {} shift".format(
                               nurse.name, present_date,
                               nurse.current_shift_state.shift_state.get(previous_day_text)), \
                           parent_rule_id, parent_rule_description, child_rules + []
            else:
                return self.rule_id, self.rule_description, False, \
                       "Nurse {} cannot do more than {} night shifts per month".format(nurse.name,
                                                                                       NIGHT_SHIFTS_PER_MONTH), \
                       parent_rule_id, parent_rule_description, child_rules + []

        else:
            return rule_id, rule_description, status, status_reason, \
                   parent_rule_id, parent_rule_description, child_rules + []


class ConsecutiveDaysShiftRule(Rule):
    """
        In a ConsecutiveDaysShiftRule, it checks if a nurse is eligible to do consecutive shifts in a row. A nurse cannot
        do more than 5 consecutive days in a row.
    """

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        parent_rule_id = parent_rule.rule_id if parent_rule else None
        parent_rule_description = parent_rule.rule_description if parent_rule else None
        if rule_input:
            nurse = rule_input.get("nurse")
            present_date = rule_input.get("date")
            has_worked_until_consecutive_days_limit = self.worked_until_consecutive_days_limit(nurse, present_date)
            if not has_worked_until_consecutive_days_limit:
                return self.rule_id, self.rule_description, True, "Pass", \
                       parent_rule.rule_id, parent_rule.rule_description, []
            else:
                return self.rule_id, self.rule_description, False, \
                       "Nurse {} cannot do more than {} days of consecutive shifts.".format(
                           nurse.name, CONSECUTIVE_DAYS_SHIFT), \
                       parent_rule.rule_id, parent_rule.rule_description, []
        else:
            return self.rule_id, self.rule_description, False, "Expected a Rule Input to execute the Rule.", \
                   parent_rule_id, parent_rule_description, []

    @staticmethod
    def worked_until_consecutive_days_limit(nurse, present_date):
        has_worked_until_consecutive_days_limit = True
        for days_delta in range(1, CONSECUTIVE_DAYS_SHIFT+1):
            prior_day = datetime.datetime.strptime(present_date, '%Y-%m-%d').date() \
                        - datetime.timedelta(days=days_delta)
            prior_day_text = prior_day.__str__()
            if not nurse.current_shift_state.shift_state \
                    or (nurse.current_shift_state.shift_state
                        and prior_day_text in nurse.current_shift_state.shift_state
                        and nurse.current_shift_state.shift_state.get(prior_day_text) is None):
                has_worked_until_consecutive_days_limit = False
                break
        return has_worked_until_consecutive_days_limit


class DaysOffShiftRule(Rule):
    """
        In a DaysOffShiftRule, it checks if a nurse has taken days off in a group of two or more
    """

    def execute(self, rule_input, parent_rule=None):
        parent_rule_id = parent_rule.rule_id if parent_rule else None
        parent_rule_description = parent_rule.rule_description if parent_rule else None
        if rule_input:
            nurse = rule_input.get("nurse")
            present_date = rule_input.get("date")
            has_taken_days_off_until_limit = self.days_off_until_limit(nurse, present_date)
            if has_taken_days_off_until_limit:
                return self.rule_id, self.rule_description, True, "Pass", \
                       parent_rule.rule_id, parent_rule.rule_description, []
            else:
                return self.rule_id, self.rule_description, False, \
                       "Nurse {} has not completed the mandatory Days Off of minimum {} days or more.".format(
                           nurse.name, MINIMUM_DAYS_OFF_SHIFT), parent_rule.rule_id, parent_rule.rule_description, []
        else:
            return self.rule_id, self.rule_description, False, "Expected a Rule Input to execute the Rule.", \
                   parent_rule_id, parent_rule_description, []

    @staticmethod
    def days_off_until_limit(nurse, present_date):
        has_taken_days_off_until_limit = True
        for days_delta in range(1, MINIMUM_DAYS_OFF_SHIFT+1):
            prior_day = datetime.datetime.strptime(present_date, '%Y-%m-%d').date() \
                        - datetime.timedelta(days=days_delta)
            prior_day_text = prior_day.__str__()
            if (nurse.current_shift_state.shift_state
                    and prior_day_text in nurse.current_shift_state.shift_state
                    and nurse.current_shift_state.shift_state.get(prior_day_text) is not None):
                has_taken_days_off_until_limit = False
                break
            elif not nurse.current_shift_state.shift_state:
                break
        return has_taken_days_off_until_limit
