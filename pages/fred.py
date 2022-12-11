#!/usr/bin/env python

import logging
import os
from datetime import datetime
from pprint import pformat

# import altair as alt
# import numpy as np
# import pandas as pd
import pandas_datareader.data as pdd
import streamlit as st


def main():
    logger = logging.getLogger(__name__)
    logger.debug(f'__file__: {__file__}')
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


if __name__ == '__main__':
    main()
