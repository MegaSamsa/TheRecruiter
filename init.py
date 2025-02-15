from tkinter import *
from tkinter import messagebox
import random as rnd
import json
import names

from methods import read_json

config = read_json('data/config.json')
general_settings = config.get('general_settings', {})

sql_settings = config.get('sql_settings', {})
db_tables = sql_settings['tables']

window_settings = config.get('window_settings', {})

unit_settings = config.get('unit_settings', {})
units_per_session = unit_settings['units_per_session']

specifications_json = read_json('data/specifications.json')
specifications_list = list(specifications_json)
specifications_num = len(specifications_list)
