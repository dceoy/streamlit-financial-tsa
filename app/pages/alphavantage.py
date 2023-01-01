#!/usr/bin/env python

import logging
import os
from datetime import date, datetime, time, timedelta
from pprint import pformat

import pandas_datareader.data as pdd
import streamlit as st


def main():
    logger = logging.getLogger(__name__)
    logger.debug(f'__file__: {__file__}')
    api_key = os.environ['ALPHAVANTAGE_API_KEY']
    today = date.today()
    st.header('Historical Time Series Data from Alpha Vantage')
    with st.sidebar.form('condition'):
        st.header('Condition')
        symbol = st.text_input('Symbol:', value='')
        endpoint = st.selectbox(
            'Time Series Endpoint:',
            options=(
                'av-intraday', 'av-daily', 'av-daily-adjusted', 'av-weekly',
                'av-weekly-adjusted', 'av-monthly', 'av-monthly-adjusted',
                'av-forex-daily'
            )
        )
        date_from = st.date_input('From:', value=today)
        date_to = st.date_input('To:', value=today)
        submitted = st.form_submit_button('Submit')
    if submitted:
        if not symbol:
            st.error('A symbol is required!', icon='🚨')
        elif date_from > date_to:
            st.error('The date interval is invalid!', icon='🚨')
        else:
            df = _load_data_with_pandas_datareader(
                name=symbol, data_source=endpoint,
                start=datetime.combine(date_from, time()),
                end=(datetime.combine(date_to, time()) + timedelta(days=1)),
                api_key=api_key
            )
            st.line_chart(data=df, y='close', use_container_width=True)
            st.area_chart(data=df, y='volume', use_container_width=True)
            st.write('Data Frame:', df)


def _load_data_with_pandas_datareader(**kwargs):
    logger = logging.getLogger(__name__)
    logger.info('Argments for DataReader:' + os.linesep + pformat(kwargs))
    return pdd.DataReader(**kwargs)


if __name__ == '__main__':
    main()
