"""
Created on july, 2020

@author: Claudio Munoz Crego (ESAC)

Python module to handle IO_TORUS Plasma Model

"""

import os
import sys
import logging
import spiceypy as spi
import numpy as np

from esac_juice_pyutils.commons.my_log import setup_logger
from juice_plasma_torus.plasma_torus_model.io_torus import PlasmaTorus
from juice_plasma_torus.plasma_torus_model.mysql_connector_io_torus import MysqlConnectorIoTorus


if __name__ == "__main__":

    setup_logger('info')

    logging.info('start')

    param = {
        "mandatory_inputs": {
            "event_id": "IO_TORUS_SC2EARTH_INTERCEPT",
            "kernel_root_dir": '/Users/cmunoz/Juice/JuiceKernels',
            "metakernel3.2": "../test_files/juice_crema_3_2_ops.tm",
            "metakernel": "../test_files/juice_crema_3_0_ops_c_munoz.tm",
            "dsk": ["juice_io_plasma_torus_v01.bds"],
            "output_path": "../test_files/torus_plasma_model",
            "table_name": "juice_io_torus_intercept_sc2earth_ray",
            "crema": "crema_3_0",
            "spacecraft": "JUICE",
            "#start_time_utc": "2030-OCT-6 19:30:00",
            "#end_time_utc": "2030-OCT-8 20:36:00",
            "start_time_utc": "2030-DEC-26 00:00:00",
            "end_time_utc": "2031-DEC-28 00:00:00",
            "# start_time_utc": "2029-APR-7 00:00:00",
            "#end_time_utc": "2033-JUN-4 00:00:00",
            "interval": 60,
            "generate_segments": 1,
            "segment_id": "IO_TORUS_SC2EARTH_INTERCEPT",
            "malargue_vis": {
                "even_id": "GS_MAL_10",
                "description": "Juice Elevation above 10 deg. from Malargue",
                "body": "Juice",
                "station": "MALARGUE",
                "elevation": 10,
                "interval": 600,
            },
            "malargue_pass": {
                "start": 0,
                "duration": 8 * 3600
            }
        },
        "Descriptions": {
            "mandatory_inputs": {
                "event_id": "event identifier",
                "kernel_root_dir": 'path of kernel root directory',
                "metakernel": "the path to the desired metakernel file",
                "dsk": "list of dsk file to be loaded",
                "output_path": "the directory in which the outputs will be generated",
                "table_name": "table name pre_fix",
                "crema": "crema identifier",
                "spacecraft": "the observer's name",
                "start_time_utc": "the start time of the study having the following form: YYYY-MON-DD HH:MM:SS",
                "end_time_utc": "the end time of the study",
                "interval": "number of seconds (step))",
                "malargue_vis": "parameters to calculate Malargue visibilty",
                "malargue_pass": "parameters to calculate Malargue passes",
                "generate_segments": "flag allowing to generate the segment files; 0 by default"
            }
        }
    }

    print('pwd :{}'.format(os.getcwd()))

    config = param["mandatory_inputs"]
    # if not os.path.exists(config['metakernel']):
    #     logging.error('file does not exist: {}'.format(config['metakernel']))
    #     sys.exit()
    #
    # spi.furnsh(config['metakernel'])
    #
    # for f in config['dsk']:
    #     file_path = os.path.join(config['kernel_root_dir'], 'dsk')
    #     file_path = os.path.join(file_path, f)
    #     spi.furnsh(file_path)

    p = PlasmaTorus(config)
    data = p.generate_intercept_periods()

    logging.info('Generate table')

    mysql_config = {
        'user': 'test_user',
        'password': 'test',
        'host': '127.0.0.1',
        'database': 'test',
        'raise_on_warnings': True,
    }

    table_name = '_'.join([config['table_name'], config['crema']])

    db = MysqlConnectorIoTorus(mysql_config, output_path=config['output_path'])
    db.create_db_table_object(table_name, engine='InnoDB')
    db.insert_into_table(table_name, data)
    db.dump_table(table_name)

    logging.info('End!')
