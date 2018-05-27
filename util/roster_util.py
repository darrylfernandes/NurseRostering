import os
import datetime
import calendar
import random

from openpyxl import Workbook
import logging

from config.roster_rules import NIGHT_SHIFT_RULE, CAN_DO_SHIFT_RULE, MORNING_SHIFT_RULE, EVENING_SHIFT_RULE
from model.nurse import Nurse
from rules_engine.util.executor import RuleExecutor

logging.basicConfig(filename='nurse_rostering.log', level=logging.INFO,
                    format='%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


def get_nurses():
    logger.info('Nurse list generation in progress......')
    filename = os.path.join(os.path.dirname(__file__), '../nurses.txt')
    with open(filename) as nurses_file:
        nurses_list = set([Nurse(name.strip('\n')) for name in nurses_file.readlines()])
    logger.info('Nurse list generation completed......')
    return nurses_list


def generate_nurses_roster_report(start_date, period='month', staff_in_each_shift=5):
    logger.info('Nurse roster preparation in progress......')
    nurses_list = get_nurses()
    logger.info('Nurse roster calculation logic in progress......')
    generate_nurses_roster(start_date, start_date, nurses_list, period=period, staff_in_each_shift=staff_in_each_shift)
    logger.info('Nurse roster calculation logic completed......')
    generate_report(start_date, nurses_list, period=period, format='xlsx', delimiter=None)
    logger.info('Nurse roster preparation completed......')


def generate_nurses_roster(start_date, for_date, nurses_list, period='month', staff_in_each_shift=5):
    execute_nurses_roster_rules(for_date, nurses_list, staff_in_each_shift=staff_in_each_shift)
    next_date = for_date + datetime.timedelta(days=1)
    if (period == 'month' and (next_date.year > start_date.year or next_date.month > start_date.month)) or \
            (period == 'year' and (next_date.year > start_date.year and next_date.month == start_date.month)):
        return # This is to force stop the roster generation logic
    else:
        generate_nurses_roster(start_date, next_date, nurses_list, period=period, staff_in_each_shift=staff_in_each_shift)


def execute_nurses_roster_rules(for_date, nurses_list, staff_in_each_shift=5):
    morning_shift_nurses = set([])
    evening_shift_nurses = set([])
    night_shift_nurses = set([])

    nurses_requiring_mandatory_dayoff = set([])
    nurses_cannot_do_night_shift = set([])
    nurses_who_can_work = set([])

    for nurse in nurses_list:
        if not nurse_can_do_night_shift(for_date, nurse):
            nurses_cannot_do_night_shift.add(nurse)
        if not nurse_can_do_shift(for_date, nurse):
            nurses_requiring_mandatory_dayoff.add(nurse)
        else:
            nurses_who_can_work.add(nurse)

    while len(nurses_who_can_work) > 0:
        nurse = random.choice(list(nurses_who_can_work))

        if len(morning_shift_nurses) < staff_in_each_shift and nurse_can_do_morning_shift(for_date, nurse):
            nurse.current_shift_state.shift_state[for_date.__str__()] = 'Morning'
            morning_shift_nurses.add(nurse)
        elif len(evening_shift_nurses) < staff_in_each_shift and nurse_can_do_evening_shift(for_date, nurse):
            nurse.current_shift_state.shift_state[for_date.__str__()] = 'Evening'
            evening_shift_nurses.add(nurse)
        elif len(night_shift_nurses) < staff_in_each_shift and nurse not in nurses_cannot_do_night_shift:
            nurse.current_shift_state.shift_state[for_date.__str__()] = 'Night'
            nurse.current_shift_state.night_shifts_per_month += 1
            night_shift_nurses.add(nurse)
        else:
            nurse.current_shift_state.shift_state[for_date.__str__()] = None
            nurses_requiring_mandatory_dayoff.add(nurse)
        nurses_who_can_work.remove(nurse)


def nurse_can_do_night_shift(for_date, nurse):
    rule_input = {'nurse': nurse, 'date': for_date.__str__()}
    rule_executor = RuleExecutor(rule_input)
    overall_rule_execution_status, overall_rule_execution_status_reason, rule_execution_trace = \
        rule_executor.execute([NIGHT_SHIFT_RULE])
    return overall_rule_execution_status


def nurse_can_do_shift(for_date, nurse):
    rule_input = {'nurse': nurse, 'date': for_date.__str__()}
    rule_executor = RuleExecutor(rule_input)
    overall_rule_execution_status, overall_rule_execution_status_reason, rule_execution_trace = \
        rule_executor.execute([CAN_DO_SHIFT_RULE])
    return overall_rule_execution_status


def nurse_can_do_morning_shift(for_date, nurse):
    rule_input = {'nurse': nurse, 'date': for_date.__str__()}
    rule_executor = RuleExecutor(rule_input)
    overall_rule_execution_status, overall_rule_execution_status_reason, rule_execution_trace = \
        rule_executor.execute([MORNING_SHIFT_RULE])
    return overall_rule_execution_status


def nurse_can_do_evening_shift(for_date, nurse):
    rule_input = {'nurse': nurse, 'date': for_date.__str__()}
    rule_executor = RuleExecutor(rule_input)
    overall_rule_execution_status, overall_rule_execution_status_reason, rule_execution_trace = \
        rule_executor.execute([EVENING_SHIFT_RULE])
    return overall_rule_execution_status


def generate_report(start_date, nurses_list, period='month', format='xlsx', delimiter=None):
    if format == 'xlsx':
        logger.info('Roster excel presentation in progress......')
        wb = Workbook()
        start_period = '{}_{}'.format(calendar.month_abbr[start_date.month], start_date.year)
        destination_filename = 'nurse_roster_{}.xlsx'.format(start_period)
        ws1 = wb.active
        ws1.title = start_period
        all_row_data = get_all_row_data(start_date, nurses_list, period=period)
        [ws1.append(row) for row in all_row_data]

        wb.save(destination_filename)
        logger.info('Roster excel presentation completed......')
    else:
        pass


def get_all_row_data(start_date, nurses_list, period='month'):
    all_row_data = []
    header_row_data = ['Nurse Name']

    for_date = start_date
    append_dates_for_month = True
    while append_dates_for_month:
        if period == 'month' and (for_date.year > start_date.year or for_date.month > start_date.month):
            append_dates_for_month = False
        else:
            header_row_data.append(for_date.__str__())
            for_date = for_date + datetime.timedelta(days=1)
    all_row_data.append(header_row_data)

    for nurse in nurses_list:
        all_row_data.append(get_roster_row_data(start_date, nurse, period='month'))

    return all_row_data


def get_roster_row_data(start_date, nurse, period='month'):
    nurse_roster_data = [nurse.name]
    for_date = start_date
    append_dates_for_month = True
    while append_dates_for_month:
        if period == 'month' and (for_date.year > start_date.year or for_date.month > start_date.month):
            append_dates_for_month = False
        else:
            for_date = for_date + datetime.timedelta(days=1)
            nurse_roster_data.append(nurse.current_shift_state.shift_state.get(for_date.__str__(), None))
    return nurse_roster_data


def date_validator(input_date_text):
    try:
        return datetime.datetime.strptime(input_date_text, '%d/%m/%Y').date()
    except ValueError:
        raise ValueError("Incorrect data format, should be mm/yyyy")


if __name__ == '__main__':
    logger.info('***************************************NURSE ROSTERING***************************************')
    input_date_text = input('Specify the Month & Year in mm/yyyy format (eg: for May 2018, enter 05/2018) : ')
    input_date_text = '{}/{}'.format('01', input_date_text)
    start_date = date_validator(input_date_text)
    generate_nurses_roster_report(start_date, period='month', staff_in_each_shift=5)
    logger.info('***************************************   TERMINATED  ***************************************')
