import logging
import sys


if __name__ == '__main__':

    import mysql.connector
    import pandas as pd

    mysql_config = {
        'user': 'test',
        'password': 'test',
        'host': '127.0.0.1',
        'database': 'test',
        'raise_on_warnings': False,
    }

    # Import sql table in database
    from esac_juice_pyutils.db.mysql_import_dump_file import import_dump_file

    import_dump_file('../TDS/references/juice_crema_5_0_sc2earth_ray_crossing_europa_plasma_torus.sql',
                     mysql_config['database'], mysql_config['user'], mysql_config['password'])

    my_conn = mysql.connector.connect(**mysql_config)

    table = "juice_crema_5_0_sc2earth_ray_crossing_europa_plasma_torus"
    my_data = pd.read_sql("DESC {}".format(table), my_conn)
    print(my_data)

    query = """SELECT * from {}""".format(table)
    print('\nquery = {}'.format(query))
    df = pd.read_sql(query, my_conn)
    print('Number of row = {}'.format(len(df)))

    query = "SELECT * from {} where is_gs_vis=1".format(table)
    print('\nquery = {}'.format(query))
    df = pd.read_sql(query, my_conn)
    print('Number of row = {}'.format(len(df)))