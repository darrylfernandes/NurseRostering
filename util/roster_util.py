import os
import datetime
import calendar
from openpyxl import Workbook
import logging

from model.nurse import Nurse

logging.basicConfig(filename='nurse_rostering.log', level=logging.INFO,
                    format='%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

def get_nurses():
    logger.info('Nurse list generation in progress......')
    filename = os.path.join(os.path.dirname(__file__), '../nurses.txt')
    with open(filename) as nurses_file:
        nurses_list = [Nurse(name.strip('\n')) for name in nurses_file.readlines()]
    logger.info('Nurse list generation completed......')
    return nurses_list


def generate_nurses_roster_report(start_date):
    logger.info('Nurse roster preparation in progress......')
    nurses_list = get_nurses()
    generate_nurses_roster(start_date, nurses_list)
    generate_report(start_date, nurses_list, format='xlsx', delimiter=None)
    logger.info('Nurse roster preparation completed......')


def generate_nurses_roster(for_date, nurses_list):
    # TODO : Logic goes here
    next_date = for_date + datetime.timedelta(days=1)
    if next_date.year > start_date.year or next_date.month > start_date.month:
        return  # This is to force stop the roster generation logic
    else:
        generate_nurses_roster(next_date, nurses_list)


def generate_report(start_date, nurses_list, format='xlsx', delimiter=None):
    logger.info('Report generation in progress......')
    if format == 'xlsx':
        wb = Workbook()
        start_period = '{}_{}'.format(calendar.month_abbr[start_date.month], start_date.year)
        destination_filename = 'nurse_roster_{}.xlsx'.format(start_period)
        ws1 = wb.active
        ws1.title = start_period
        wb.save(destination_filename)
    else:
        pass
    logger.info('Report generation completed......')

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
    generate_nurses_roster_report(start_date)
    logger.info('***************************************   TERMINATED  ***************************************')
