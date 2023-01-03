#!/usr/bin/env python

import logging
import os
from datetime import date, datetime, time, timedelta
from pprint import pformat

import pandas as pd
import pandas_datareader.data as pdd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def main():
    logger = logging.getLogger(__name__)
    logger.debug(f'__file__: {__file__}')
    api_key = os.environ['ALPHAVANTAGE_API_KEY']
    today = date.today()
    st.header('Historical Time Series Data from Alpha Vantage')
    with st.sidebar.form('condition'):
        st.header('Condition')
        st.session_state['symbol'] = st.text_input(
            'Symbol:', value=(st.session_state.get('symbol') or '')
        )
        endpoint_options = (
            'av-intraday', 'av-daily', 'av-daily-adjusted', 'av-weekly',
            'av-weekly-adjusted', 'av-monthly', 'av-monthly-adjusted',
            'av-forex-daily'
        )
        endpoint = st.selectbox(
            'Time Series Endpoint:', options=endpoint_options,
            index=(st.session_state.get('endpoint_index') or 0)
        )
        st.session_state['endpoint_index'] = endpoint_options.index(endpoint)
        st.session_state['date_from'] = st.date_input(
            'From:', value=(st.session_state.get('date_from') or today)
        )
        st.session_state['date_to'] = st.date_input(
            'To:', value=(st.session_state.get('date_to') or today)
        )
        submitted = st.form_submit_button('Submit')
    if submitted:
        if not st.session_state['symbol']:
            st.error('A symbol is required!', icon='🚨')
        elif st.session_state['date_from'] > st.session_state['date_to']:
            st.error('The date interval is invalid!', icon='🚨')
        else:
            df = _load_data_with_pandas_datareader(
                name=st.session_state['symbol'], data_source=endpoint,
                start=datetime.combine(st.session_state['date_from'], time()),
                end=(
                    datetime.combine(st.session_state['date_to'], time())
                    + timedelta(days=1)
                ),
                api_key=api_key
            ).reset_index().assign(
                time=lambda d: pd.to_datetime(d['index'])
            ).drop(columns='index')
            st.plotly_chart(
                go.Figure(
                    data=[
                        go.Candlestick(
                            x=df['time'], open=df['open'], high=df['high'],
                            low=df['low'], close=df['close']
                        )
                    ]
                ),
                theme='streamlit', use_container_width=True
            )
            st.plotly_chart(
                px.area(df, x='time', y='volume'),
                theme='streamlit', use_container_width=True
            )
            st.write('Data Frame:', df.set_index('time'))


def _load_data_with_pandas_datareader(**kwargs):
    logger = logging.getLogger(__name__)
    logger.info('Argments for DataReader:' + os.linesep + pformat(kwargs))
    return pdd.DataReader(**kwargs)


if __name__ == '__main__':
    main()
