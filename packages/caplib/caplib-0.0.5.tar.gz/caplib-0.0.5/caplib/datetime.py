# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:41:43 2022

@author: dingq
"""
from datetime import datetime

from caplibproto.dqproto import *

from caplib.processrequest import process_request 
from caplib.staticdata import create_static_data

#Frequency
def to_frequency(src):
    '''
    Convert a string to Frequency.
    
    Parameters
    ----------
    src : str
        a string of frequency, i.e. 'ANNUAL'.
    
    Returns
    -------
    Frequency       

    '''
    if src is None:
        return INVALID_FREQUENCY
    if src in ['', 'nan']:
        return INVALID_FREQUENCY
    else:
        return Frequency.DESCRIPTOR.values_by_name[src.upper()].number

#DayCountConvention
def to_day_count_convention(src):
    '''
    Convert a string to DayCountConvention.
    
    Parameters
    ----------
    src : str
        a string of day count convention, i.e. 'ACT_365_FIXED'.
    
    Returns
    -------
    DayCountConvention       

    '''
    if src is None:
        return INVALID_DAY_COUNT_CONVENTION
    if src in ['', 'nan']:
        return INVALID_DAY_COUNT_CONVENTION
    else:
        return DayCountConvention.DESCRIPTOR.values_by_name[src.upper()].number

#BusinessDayConvention
def to_business_day_convention(src):
    '''
    Convert a string to BusinessDayConvention.
    
    Parameters
    ----------
    src : str
        a string of business day convention, i.e. 'FOLLOWING'.
    
    Returns
    -------
    BusinessDayConvention       

    '''
    if src is None:
        return INVALID_BUSINESS_DAY_CONVENTION
    if src in ['', 'nan']:
        return INVALID_BUSINESS_DAY_CONVENTION
    else:
        return BusinessDayConvention.DESCRIPTOR.values_by_name[src.upper()].number

#StubPolicy
def to_stub_policy(src):
    '''
    Convert a string to StubPolicy.
    
    Parameters
    ----------
    src : str
        a string of stub policy, i.e. 'INTIAL'.

    Returns
    -------
    StubPolicy       

    '''
    if src is None:
        return INVALID_STUB_POLICY
    if src in ['', 'nan']:
        return INVALID_STUB_POLICY
    else:
        return StubPolicy.DESCRIPTOR.values_by_name[src.upper()].number

#BrokenPeriodType
def to_broken_period_type(src):
    '''
    Convert a string to BrokenPeriodType.

    Parameters
    ----------
    src : str
        a string of broken period type, i.e. 'LONG'.

    Returns
    -------
    BrokenPeriodType       

    '''
    if src is None:
        return INVALID_BROKEN_PERIOD_TYPE
    if src in ['', 'nan']:
        return INVALID_BROKEN_PERIOD_TYPE
    else:
        return BrokenPeriodType.DESCRIPTOR.values_by_name[src.upper()].number

#ScheduleGenerationMethod
def to_sched_gen_method(src):
    '''
    Convert a string to ScheduleGenerationMethod.

    Parameters
    ----------
    src : str
        a string of schedule generation method, i.e. 'ABSOLUTE_NORMAL'.

    Returns
    -------
    ScheduleGenerationMethod       

    '''
    if src is None:
        return INVALID_SCHEDULE_GENERATION_METHOD
    if src in ['', 'nan']:
        return INVALID_SCHEDULE_GENERATION_METHOD
    else:
        return ScheduleGenerationMethod.DESCRIPTOR.values_by_name[src.upper()].number

#DateRollConvention
def to_date_roll_convention(src):
    '''
    Convert a string to DateRollConvention.

    Parameters
    ----------
    src : str
        a string of date rool convention, i.e. 'EOM'.

    Returns
    -------
    DateRollConvention       

    '''
    if src is None:
        return INVALID_DATE_ROLL_CONVENTION
    if src in ['', 'nan']:
        return INVALID_DATE_ROLL_CONVENTION
    else:
        return DateRollConvention.DESCRIPTOR.values_by_name[src.upper()].number
    
#RelativeScheduleGenerationMode
def to_rel_sched_gen_mode(src):
    '''
    Convert a string to RelativeScheduleGenerationMode.

    Parameters
    ----------
    src : str
        a string of relative schedule generation mode, i.e. 'BACKWARD_WITHOUT_BROKEN'.

    Returns
    -------
    RelativeScheduleGenerationMode       

    '''
    if src is None:
        return INVALID_DATE_ROLL_CONVENTION
    if src in ['', 'nan']:
        return INVALID_DATE_ROLL_CONVENTION
    else:
        return RelativeScheduleGenerationMode.DESCRIPTOR.values_by_name[src.upper()].number

#DateGenerationMode
def to_date_gen_mode(src):
    '''
    Convert a string to DateGenerationMode.

    Parameters
    ----------
    src : str
        a string of date generation mode, i.e. 'IN_ADVANCE'.

    Returns
    -------
    DateGenerationMode       

    '''
    if src is None:
        return INVALID_DATE_GENERATION_MODE
    if src in ['', 'nan']:
        return INVALID_DATE_GENERATION_MODE
    else:
        return DateGenerationMode.DESCRIPTOR.values_by_name[src.upper()].number

#TimeUnit
def to_time_unit(src):
    if src is None:
        return INVALID_TIME_UNIT
    
    if src in ['', 'nan']:
        return INVALID_TIME_UNIT
    else:
        return TimeUnit.DESCRIPTOR.values_by_name[src.upper()].number
    
#SpecialPeriod
def to_special_period(src):
    if src is None:
        return INVALID_DATE_GENERATION_MODE
    
    if src in ['', 'nan']:
        return INVALID_DATE_GENERATION_MODE
    else:
        return SpecialPeriod.DESCRIPTOR.values_by_name[src.upper()].number
    
#Period	
def to_period(src):
    '''
    Convert a string to Period.
    
    Parameters
    ----------
    src : str
        i.e.'3M'.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    Period
        DESCRIPTION.

    '''    
    if src=='':
        raise ValueError('to_period: empty input')
            
    term = Period()
    if src.lower() == 'on':
        term.length = 1
        term.units = DAYS
        term.special_name = ON
    elif src.lower() == 'tn':
        term.length = 1
        term.units = DAYS
        term.special_name = TN
    else:
        term.special_name = INVALID_SPECIAL_PERIOD
        term.length = int(src[0:len(src) - 1])
        if src[len(src) - 1].lower() == 'd':
            term.units = DAYS
        elif src[len(src) - 1].lower() == 'w':
            term.units = WEEKS
        elif src[len(src) - 1].lower() == 'm':
            term.units = MONTHS
        elif src[len(src) - 1].lower() == 'y':
            term.units = YEARS
    return term
    
#Date
def create_date(d: datetime):
    '''
    Create a Date object

    Parameters
    ----------
    year : int, optional
        should be between 1901 and 2200. The default is 1901.
    month : int, optional
        It should be within [1,12]. The default is 1.
    day : int, optional
        It should be within [1,31]. The default is 1.

    Returns
    -------
    Date
        DESCRIPTION.

    '''    
    if d is None:
        return dqCreateProtoDate(1901, 1, 1)
    return dqCreateProtoDate(d.year, d.month, d.day)

#Calendar
def create_calendar(cal_name, 
                    holidays = [], 
                    special_business_days = []):
    '''
    Create a Calendar object and store in the object cache. 

    Parameters
    ----------
    cal_name : str
        DESCRIPTION.
    holidays : list, optional
        list of datetime. The default is [].
    special_business_days : list, optional
        list of datetime. The default is [].

    Returns
    -------
    bool
        DESCRIPTION.

    ''' 
    holidays_serial_numbers = [hol.toordinal() for hol in holidays]
    special_business_days_serial_numbers = [hol.toordinal() for hol in special_business_days]
    pb_data = dqCreateProtoCalendar(cal_name, 
                                    holidays_serial_numbers, 
                                    special_business_days_serial_numbers) 
    pb_data_list = dqCreateProtoCalendarList([pb_data])  
    return create_static_data('SDT_CALENDAR', 
                              pb_data_list.SerializeToString())
	
#Period	
def create_period(length, unit, special_name = ''):
    '''
    Create a Period object 

    Parameters
    ----------
    length : int
        DESCRIPTION.
    unit : str
        DESCRIPTION.
    special_name : SpecialPeriod, optional
        DESCRIPTION. The default is INVALID_SPECIAL_PERIOD.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    Period
        DESCRIPTION.

    '''
    return dqCreateProtoPeriod(length, to_time_unit(unit), to_special_period(special_name))

#Year Fraction
def year_frac_calculator(start_date, end_date, day_count, 
                         ref_start_date, ref_end_date, ref_period_end, frequency = 'ANNUAL', is_end_of_month = False):
    '''
    Calculate year fraction of an period.

    Parameters
    ----------
    start_date : datetime
        DESCRIPTION.
    end_date : datetime
        DESCRIPTION.
    day_count : str
        DESCRIPTION.
    ref_start_date : datetime
        DESCRIPTION.
    ref_end_date : datetime
        DESCRIPTION.
    ref_period_end : datetime
        DESCRIPTION.
    frequency : str, optional
        DESCRIPTION. The default is ANNUAL.
    is_end_of_month : bool, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    float
        DESCRIPTION.

    '''    
    pb_input = dqCreateProtoYearFractionCalculationInput(to_day_count_convention(day_count),
                                                         create_date(start_date), 
                                                         create_date(end_date),
                                                         create_date(ref_start_date), 
                                                         create_date(ref_end_date), 
                                                         create_date(ref_period_end), 
                                                         to_frequency(frequency),
                                                         is_end_of_month)
    req_name = 'YEAR_FRACTION_CALCULATOR'
    res_msg = process_request(req_name, pb_input.SerializeToString()) 
    if res_msg == None:
        raise Exception('YEAR_FRACTION_CALCULATOR ProcessRequest: failed!')       
    pb_output = YearFractionCalculationOutput()
    pb_output.ParseFromString(res_msg)        
    return pb_output.year_fraction

#Simple Year Fraction Calculation
def simple_year_frac_calculator(start_date, end_date, day_count):
    '''
    Calculate year fraction of an period.

    Parameters
    ----------
    start_date : datetime
        DESCRIPTION.
    end_date : datetime
        DESCRIPTION.
    day_count : str
        DESCRIPTION.

    Returns
    -------
    float
        DESCRIPTION.

    '''       
    return year_frac_calculator(start_date, end_date, day_count, start_date, end_date, end_date)
