#!/usr/bin/env python

import argparse
import logging
import os
from datetime import datetime
from pprint import pformat

# import altair as alt
# import numpy as np
# import pandas as pd
import pandas_datareader.data as pdd
import streamlit as st

__version__ = 'v0.0.1'


def main():
    args = _parse_arguments()
    _set_log_config(args=args)
    logger = logging.getLogger(__name__)
    logger.info('Run the Streamlit app.')

    start = datetime(2010, 1, 1)
    end = datetime.now()
    start = end.replace(year=(end.year - 1))
    gdp = pdd.DataReader('GDP', 'fred', start, end)

    st.header('Finantial Data')
    st.write('GDP', gdp)


def _load_data_with_pandas_datareader(**kwargs):
    logger = logging.getLogger(__name__)
    logger.info('Argments for DataReader:' + os.linesep + pformat(kwargs))
    return pdd.DataReader(**kwargs)


def _set_log_config(args):
    if args.debug:
        level = logging.DEBUG
    elif args.info:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=level
    )


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog='streamlit-financial-tsa',
        description='Streamlit Application for Financial Time-series Analyses'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    logging_level_parser = parser.add_mutually_exclusive_group()
    logging_level_parser.add_argument(
        '--debug', action='store_true', help='Set logging level to DEBUG'
    )
    logging_level_parser.add_argument(
        '--info', action='store_true', help='Set logging level to INFO'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
