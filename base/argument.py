#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("data_date", type=str, help="data date format to 'yyyy-mm-dd'")
args = parser.parse_args()
