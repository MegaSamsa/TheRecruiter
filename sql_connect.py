from init import sql_settings, db_tables, specifications_list
import psycopg2

class SqlConnector():
    def __init__(self):
        self._connection = psycopg2.connect(dbname=sql_settings['db_name'], host=sql_settings['db_host'], user=sql_settings['db_user'], password=sql_settings['db_pass'], port=sql_settings['db_port'])
        self._cursor = self._connection.cursor()

    def close(self):
        self._cursor.close()
        if self._cursor.closed: print("Cursor closed")
        self._connection.close()
    
    def set_data(self, instruction: str):
        self._cursor.execute(instruction)
        self._connection.commit()
    
    def get_data(self, instruction: str):
        self._cursor.execute(instruction)
        self._connection.commit()
        return self._cursor.fetchone()
    
    def clear_table(self, table: str):
        self.set_data(f"DELETE FROM {table}")

    def delete_table(self, table: str):
        self.set_data(f"DROP TABLE {table};")

class SqlUnits(SqlConnector):   
    def create_table_units(self):
        self.set_data(f"CREATE TABLE {db_tables['units']} (Id SERIAL PRIMARY KEY, Name VARCHAR(16), Age INTEGER, Sex BOOLEAN);")

    def create_table_specifications(self):
        specifications_sql = ", ".join(f"{key.capitalize()} INTEGER" for key in specifications_list)
        self.set_data(f"CREATE TABLE {db_tables['specifications']} (Id SERIAL PRIMARY KEY, UnitId INTEGER, {specifications_sql}, Sum INTEGER, FOREIGN KEY (UnitId) REFERENCES {db_tables['units']}(Id));")

    def write_unit(self, unit: object):
        self.set_data(f"INSERT INTO {db_tables['units']} (Name, Age, Sex) VALUES ('{unit.get_name()}', {unit.get_age()}, {unit.get_sex()});")
        unit_id = self.get_unit_id(unit=unit)[0]

        specifications_names_list = ", ".join(f"{key.capitalize()}" for key in specifications_list)
        specifications_values_list = ", ".join(str(value) for value in unit.get_specifications().values())
        self.set_data(f"INSERT INTO {db_tables['specifications']} (UnitId, {specifications_names_list}, Sum) VALUES ({unit_id}, {specifications_values_list}, {unit.get_specifications_sum()});")

    def get_unit_id(self, unit: object):
        return self.get_data(f"SELECT Id FROM {db_tables['units']} WHERE Name='{unit.get_name()}' and Age={unit.get_age()} and Sex={unit.get_sex()};")

    def clear_tables(self):
        self.clear_table(table=db_tables['specifications'])
        self.clear_table(table=db_tables['units'])
