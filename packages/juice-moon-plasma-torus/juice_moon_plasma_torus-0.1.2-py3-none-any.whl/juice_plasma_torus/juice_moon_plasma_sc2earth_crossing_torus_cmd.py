"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

Python module to calculate Jupiter Moon Plasma Torus intercept by a ray spacecraft-to-body
"""

import argparse
import logging
import os
import signal
import sys
import spiceypy as spi

import esac_juice_pyutils.commons.my_log as my_log
from esac_juice_pyutils.commons import json_handler as my_json

from juice_plasma_torus import version
from juice_plasma_torus.plasma_torus_model.sc_ray_crossing_plasma_torus import PlasmaTorus, \
    generate_sql_table, generate_simple_ql_table, generate_segment, generate_eps_event_file
from juice_plasma_torus.plasma_torus_model.mysql_connector_plasma_torus import MysqlConnectorMoonTorus


def func_signal_handler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parse_options():
    """
    This function allow to specify the input parameters

    - OutputDir: path of the Output directory
    - CfgFile: path of the configuration file
    - loglevel: debug, info

    :returns args; argument o parameter list passed by command line
    :rtype list
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--CfgFile",
                        help="Path of CfgFile",
                        required=True)

    parser.add_argument("-l", "--loglevel",
                        help=" Must be debug, info ",
                        required=False)

    parser.add_argument("-v", "--version",
                        help="version number",
                        action="version",
                        version='%(prog)s {}'.format(version))

    args = parser.parse_args()
    return args


def main():
    """
        Entry point for processing

        :return:
        """

    signal.signal(signal.SIGINT, func_signal_handler)

    args = parse_options()

    logging.getLogger().setLevel(logging.DEBUG)

    log_level = 'info'
    if args.loglevel:
        if args.loglevel in ['info', 'debug']:
            log_level = args.loglevel
            my_log.add_console_logger(log_level)
        else:
            my_log.add_console_logger(log_level)
            logging.warning(
                'log level value "{0}" not valid (use debug); So default INFO level applied'.format(args.loglevel))
    else:
        my_log.add_console_logger(log_level)

    if args.CfgFile:
        if not os.path.exists(args.CfgFile):
            logging.error('Configuration File "{}" does not exist'.format(args.CfgFile))
            sys.exit(0)

        cfg_file = args.CfgFile

    else:
        logging.error('Please define a valid Configuration File')
        sys.exit(0)

    logging.info('Start...')

    package_dir = os.path.abspath(os.path.dirname(__file__))
    working_dir = os.getcwd()
    config = my_json.load_to_dic(os.path.join(working_dir, cfg_file))
    cfg = config['main']
    output_dir = os.path.join(working_dir, cfg['output_path'])

    crema = cfg['crema']
    dsk_frame = cfg['dsk_frame']
    spacecraft = cfg['spacecraft']

    os.chdir(package_dir)
    logging.info('goto root test directory: {}'.format(os.getcwd()))

    p = PlasmaTorus(cfg)

    log_file = os.path.join(output_dir, 'plasma_torus_model_{}.log'.format(crema))
    my_log.add_log_file_logger(log_file)

    values = p.generate_intercept_ingres_egres(spacecraft, dsk_frame,
                                               max_dist_to_torus_center_km=cfg['distance_sc_to_Jupiter']['max'],
                                               min_dist_to_torus_center_km=cfg['distance_sc_to_Jupiter']['min'])

    logging.info('Generate table')

    mysql_config = None
    if 'mysql_config_file' in cfg:
        mysql_config = os.path.join(working_dir, cfg['mysql_config_file'])
        if not os.path.exists(mysql_config):
            logging.error('my_sql connexion file does not exist:{}'.format(mysql_config))
            sys.exit()

    generate_sql_table(values, output_dir, mysql_config, table_name=cfg["table_name"])

    dt = cfg["interval"]
    table_name_query = cfg["table_name"]

    generate_simple_ql_table(output_dir,
                             cfg["event_id"],
                             mysql_config,
                             table_name_query=table_name_query,
                             table_name=cfg["table_name_simple"],
                             dt=dt)

    if 'segment_file' in list(cfg.keys()) and cfg['segment_file']['generate']:
        generate_segment(output_dir,
                         cfg['segment_file']['event_type'],
                         mysql_config,
                         table_name_query=table_name_query,
                         working_group=cfg['segment_file']['working_group'],
                         dt=60)

    if 'event_file' in list(cfg.keys()) and cfg['event_file']['generate']:
        generate_eps_event_file(output_dir,
                                cfg['event_file'],
                                mysql_config,
                                table_name_query=table_name_query,
                                dt=60)

    os.chdir(package_dir)
    logging.debug('goto root original directory: {}'.format(package_dir))

    logging.info('End!')


def debug():
    """
    debug: Print exception and stack trace
    """

    e = sys.exc_info()
    print("type: %s" % e[0])
    print("Msg: %s" % e[1])
    import traceback
    traceback.print_exc(e[2])
    traceback.print_tb(e[2])


if __name__ == "__main__":

    try:
        main()
    except SystemExit as e:
        print(e)
        print("<h5>Internal Error. Please contact JUICE SOC </h5>")
        raise

    sys.exit(0)
