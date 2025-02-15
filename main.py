from init import window_settings
from window_class import WindowUnit
from sql_connect import SqlUnits

window_size = window_settings['size']

window = WindowUnit(window_size=(window_size['width'], window_size['height']), title=window_settings['title'], icon_path=window_settings['icon_path'], db_connection=SqlUnits())
window.template()

window.start()
