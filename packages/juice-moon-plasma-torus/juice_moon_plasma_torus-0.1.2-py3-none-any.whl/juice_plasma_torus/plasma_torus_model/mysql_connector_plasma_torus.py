"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)
"""

import os
import sys
import logging
import mysql.connector
import datetime

from juice_plasma_torus.commons.mysql_connector import MysqlConnector


class MysqlConnectorMoonTorus(MysqlConnector):
    """
    This class allows to connect to my_sql using my_sql python package.
    """

    def create_db_table_object(self, table_name, flag_recreate=True, engine='MyISAM'):
        """
        This routine allows to create tables in the database

        :param table_name: name of the table
        :param flag_recreate: if True drops the tableName (if exists)
        :param engine: database engine [MyISAM,InnoDB]
        """

        flag_create = True

        if self.table_exists(table_name) == 1:

            logging.info(f'Table {table_name} already exists in db {self.db}')
            if flag_recreate:
                self.drop_table(table_name)
                logging.info(f'Drop and recreate Table {table_name} in db {self.db}')
            else:
                flag_create = False

        if flag_create:
            cnx = self.get_mysql_connector()
            cursor = cnx.cursor()
            query = ('CREATE TABLE IF NOT EXISTS`' + table_name + '`' +
                     '''(`id` mediumint(9) NOT NULL AUTO_INCREMENT,
                          `ev_type` char(40) DEFAULT NULL,
                          `ev_utc` char(17) DEFAULT NULL,
                          `ev_utc_cal` char(20) DEFAULT NULL,
                          `ev_et` double DEFAULT NULL,
                          `dsk_frame` char(17) DEFAULT NULL,
                          `ssc_lon` double DEFAULT NULL,
                          `ssc_lat` double DEFAULT NULL,
                          `radius` double DEFAULT NULL,
                          `is_s_n` `boolean NOT NULL DEFAULT 0,
                          `is_back_torus_intercept` boolean NOT NULL DEFAULT 0,
                          `is_gs_vis` boolean NOT NULL DEFAULT 0,
                          `is_gs_pass` boolean NOT NULL DEFAULT 0,
                          `nb_intercept_points` int NOT NULL DEFAULT 0,
                          `group_counter` int NOT NULL DEFAULT 0,
                          PRIMARY KEY (`id`)
                    ) ENGINE={} DEFAULT CHARSET=latin1 MAX_ROWS=4294967295
                    COMMENT='{}';
            '''.format(engine, 'Table loaded'))

            print(query)

            cursor.execute(query)

            logging.info(f'query completed in db {self.db} ; table created/re-created {table_name}')

    def create_db_table_object_ingress_egress(self, table_name, flag_recreate=True, engine='MyISAM'):
        """
        This routine allows to create tables in the database

        :param table_name: name of the table
        :param flag_recreate: if True drops the tableName (if exists)
        :param engine: database engine [MyISAM,InnoDB]
        """

        flag_create = True

        if self.table_exists(table_name) == 1:

            logging.info(f'Table {table_name} already exists in db {self.db}')
            if flag_recreate:
                self.drop_table(table_name)
                logging.info(f'Drop and recreate Table {table_name} in db {self.db}')
            else:
                flag_create = False

        if flag_create:
            cnx = self.get_mysql_connector()
            cursor = cnx.cursor()
            query = ('CREATE TABLE IF NOT EXISTS`' + table_name + '`' +
                     '''(`id` mediumint(9) NOT NULL AUTO_INCREMENT,
                          `ev_type` char(40) DEFAULT NULL,
                          `ev_utc` char(17) DEFAULT NULL,
                          `ev_utc_cal` char(20) DEFAULT NULL,
                          `ev_et` double DEFAULT NULL,
                          `dsk_frame` char(17) DEFAULT NULL,
                          `ssc_lon` double DEFAULT NULL,
                          `ssc_lat` double DEFAULT NULL,
                          `radius` double DEFAULT NULL,
                          `is_back_torus_intercept` boolean NOT NULL DEFAULT 0,
                          `is_gs_vis` boolean NOT NULL DEFAULT 0,
                          `is_gs_pass` boolean NOT NULL DEFAULT 0,
                          `nb_intercept_points` int NOT NULL DEFAULT 0,
                          `group_counter` int NOT NULL DEFAULT 0,
                          PRIMARY KEY (`id`)
                    ) ENGINE={} DEFAULT CHARSET=latin1 MAX_ROWS=4294967295
                    COMMENT='{}';
            '''.format(engine, 'Table loaded'))

            print(query)

            cursor.execute(query)

            logging.info(f'query completed in db {self.db} ; table created/re-created {table_name}')

    def create_db_table_object_within_moon_plasma_torus(self, table_name, flag_recreate=True, engine='MyISAM'):
        """
        This routine allows to create tables in the database

        :param table_name: name of the table
        :param flag_recreate: if True drops the tableName (if exists)
        :param engine: database engine [MyISAM,InnoDB]
        """

        flag_create = True

        if self.table_exists(table_name) == 1:

            logging.info(f'Table {table_name} already exists in db {self.db}')
            if flag_recreate:
                self.drop_table(table_name)
                logging.info('Drop and recreate Table {table_name} in db {self.db}')
            else:
                flag_create = False

        if flag_create:
            cnx = self.get_mysql_connector()
            cursor = cnx.cursor()
            query = ('CREATE TABLE IF NOT EXISTS`' + table_name + '`' +
                     '''(`id` mediumint(9) NOT NULL AUTO_INCREMENT,
                          `ev_type` char(40) DEFAULT NULL,
                          `ev_utc` char(17) DEFAULT NULL,
                          `ev_utc_cal` char(20) DEFAULT NULL,
                          `ev_et` double DEFAULT NULL,
                          `dsk_frame` char(17) DEFAULT NULL,
                          `s_point_lon` double DEFAULT NULL,
                          `s_point_lat` double DEFAULT NULL,
                          `s_point_radius` double DEFAULT NULL,
                          `is_back_torus_intercept` boolean NOT NULL DEFAULT 0,
                          `nb_intercept_points` int NOT NULL DEFAULT 0,
                          `group_counter` int NOT NULL DEFAULT 0,
                          PRIMARY KEY (`id`)
                    ) ENGINE={} DEFAULT CHARSET=latin1 MAX_ROWS=4294967295
                    COMMENT='{}';
            '''.format(engine, 'Table loaded'))

            print(query)

            cursor.execute(query)

            logging.info(f'query completed in db {self.db}; table created/re-created {table_name}')

    def create_db_table_object_within_moon_plasma_torus_simple(self, table_name, flag_recreate=True, engine='MyISAM'):
        """
        This routine allows to create tables in the database

        :param table_name: name of the table
        :param flag_recreate: if True drops the tableName (if exists)
        :param engine: database engine [MyISAM,InnoDB]
        """

        flag_create = True

        if self.table_exists(table_name) == 1:

            logging.info('Table {1} already exists in db {0}'.format(self.db, table_name))
            if flag_recreate:
                self.drop_table(table_name)
                logging.info('Drop and recreate Table {1} in db {0}'.format(self.db, table_name))
            else:
                flag_create = False

        if flag_create:
            cnx = self.get_mysql_connector()
            cursor = cnx.cursor()
            query = ('CREATE TABLE IF NOT EXISTS`' + table_name + '`' +
                     '''(`id` mediumint(9) NOT NULL AUTO_INCREMENT,
                          `ev_type` char(40) DEFAULT NULL,
                          `ev_utc` char(17) DEFAULT NULL,
                          `ev_utc_cal` char(20) DEFAULT NULL,
                          `ev_et` double DEFAULT NULL,
                          `s_point_lon` double DEFAULT NULL,
                          `s_point_lat` double DEFAULT NULL,
                          `s_point_radius` double DEFAULT NULL,
                          PRIMARY KEY (`id`)
                    ) ENGINE={} DEFAULT CHARSET=latin1 MAX_ROWS=4294967295
                    COMMENT='{}';
            '''.format(engine, 'Table loaded'))

            print(query)

            cursor.execute(query)

            logging.info(f'query completed in db {self.db}; table created/re-created {table_name}')

    def create_db_table_object_sc2Earth_intercept_moon_plasma_torus(self, table_name, flag_recreate=True, engine='MyISAM'):
        """
        This routine allows to create tables in the database

        :param table_name: name of the table
        :param flag_recreate: if True drops the tableName (if exists)
        :param engine: database engine [MyISAM,InnoDB]
        """

        flag_create = True

        if self.table_exists(table_name) == 1:

            logging.info('Table {1} already exists in db {0}'.format(self.db, table_name))
            if flag_recreate:
                self.drop_table(table_name)
                logging.info('Drop and recreate Table {1} in db {0}'.format(self.db, table_name))
            else:
                flag_create = False

        if flag_create:
            cnx = self.get_mysql_connector()
            cursor = cnx.cursor()
            query = ('CREATE TABLE IF NOT EXISTS`' + table_name + '`' +
                     '''(`id` mediumint(9) NOT NULL AUTO_INCREMENT,
                          `ev_type` char(40) DEFAULT NULL,
                          `ev_utc` char(17) DEFAULT NULL,
                          `ev_utc_cal` char(20) DEFAULT NULL,
                          `ev_et` double DEFAULT NULL,
                          `s_point_lon` double DEFAULT NULL,
                          `s_point_lat` double DEFAULT NULL,
                          `s_point_radius` double DEFAULT NULL,
                          `is_back_torus_intercept` boolean NOT NULL DEFAULT 0,
                          `is_gs_vis` boolean NOT NULL DEFAULT 0,
                          `is_gs_pass` boolean NOT NULL DEFAULT 0,
                          `nb_intercept_points` int NOT NULL DEFAULT 0,
                          `group_counter` int NOT NULL DEFAULT 0,
                          PRIMARY KEY (`id`)
                    ) ENGINE={} DEFAULT CHARSET=latin1 MAX_ROWS=4294967295
                    COMMENT='{}';
            '''.format(engine, 'Table loaded'))

            print(query)

            cursor.execute(query)

            logging.info(f'query completed in db {self.db}; table created/re-created {table_name}')