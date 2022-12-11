#!/usr/bin/env python

import argparse
import logging

import streamlit as st

__version__ = 'v0.0.1'


def main():
    args = _parse_arguments()
    _set_log_config(args=args)
    logger = logging.getLogger(__name__)
    logger.debug(f'__file__: {__file__}')
    st.set_page_config(page_title='financial-tsa', page_icon='👋')
    st.markdown('# Main page 🎈')
    st.sidebar.markdown('# Main page 🎈')


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
