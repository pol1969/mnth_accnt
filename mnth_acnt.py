#!/usr/bin/env python3
"""
Author : pol1969 <podberezsky1969@gmail.com>
Date   : 2021-10-27
Purpose: Python automotion in MOOD
"""

import argparse
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import operators, extract
# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Эта программа для составления отчета по базам МООД',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-y',
                        '--year',
                        help='Год составления отчета, по умолчанию текущий',
                        metavar='year',
                        type=int,
                        default=dt.datetime.now().year)
    parser.add_argument('-m',
                        '--month',
                        help='Месяц составления отчета,по умолчанию предыдущий',
                        metavar='month',
                        type=int,
                        default=dt.datetime.now().month-1)
    parser.add_argument('-o',
                        '--otd',
                        help='Отделение',
                        metavar='otd',
                        choices =[40,30,34],
                        type=int,
                        default=40)
 
    parser.add_argument('-q',
                        '--qwart',
                        help='Отчет за месяцы с первого по q',
                        metavar='qwart',
                        type=int,
                        default=0)


    args = parser.parse_args()

    if args.year < 2000 or args.year >3000:
        parser.error('Год должен быть в пределах от 1995 до 3000')

    if args.month == 0:
        args.month=12
        args.year=args.year-1


    if args.month < 0 or args.month  >12:
        parser.error('Число месяца должно быть от 1 до 12')

    if args.qwart < 0 or args.qwart >12:
        parser.error('Месяц квартала д. б. между 1 и 12')

    return args


# --------------------------------------------------
def main():
    """ Отчет по выписанным пациентам """

    args = get_args()
    year = args.year
    month = args.month
    otd = args.otd
    qwart = args.qwart

    print(f'Год = {year}')
    print(f'Месяц = {month}')
    print(f'Отделение = {otd}')
    print(f'Месяцы с первого по  = {qwart}')

    
    Base = automap_base()
    engine = create_engine('mysql+pymysql://pol:19691319@192.168.31.1/moodMS')
    Base.prepare(engine, reflect=True)
    
    session = Session(engine)

    ills = Base.classes.ills
    kartotek = Base.classes.kartotek
    oper = Base.classes.oper

    if qwart==0:
        ''' Отчет за один месяц '''
        
        nmb = session.query(func.count(ills.AN_NOMISS)).filter(ills.I_OTDELEN==otd,
            extract('year',ills.I_DATEOU_O)==year,
            extract('month',ills.I_DATEOU_O)==month).scalar()
 

    else:
        ''' Отчет за несколько месяцев, начиная с первого '''

        nmb = session.query(func.count(ills.AN_NOMISS)).filter(ills.I_OTDELEN==otd,
            extract('year',ills.I_DATEOU_O)==year,
            extract('month',ills.I_DATEOU_O)<=qwart,
            extract('month',ills.I_DATEOU_O)>=1).scalar()
 
    print(f'Выписано за {month} месяц {year} года в {otd} отделении {nmb} пациентов')





# --------------------------------------------------
if __name__ == '__main__':
    main()


