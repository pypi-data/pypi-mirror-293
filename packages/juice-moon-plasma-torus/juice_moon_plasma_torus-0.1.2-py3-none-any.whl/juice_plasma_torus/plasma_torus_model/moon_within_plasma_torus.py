"""
Created on Jan, 2021

@author: Claudio Munoz Crego (ESAC)

Python module to handle Plasma Torus Model

"""

import os
import sys
import logging
import spiceypy as spi
import numpy as np
import pandas as pd

from spiceypy.utils.exceptions import SpiceyError

import esac_juice_pyutils.commons.tds_spicey as tds_spicey
import esac_juice_pyutils.gti.gti_handler as gti_handler

from juice_plasma_torus.plasma_torus_model.mysql_connector_plasma_torus import MysqlConnectorMoonTorus
from juice_plasma_torus.plasma_torus_model.plasma_torus import PlasmaTorus, print_df_as_tab
from juice_plasma_torus.plasma_torus_model.gf_distance import GfDistance


class PlasmaTorus(PlasmaTorus):

    def generate_sc_within_torus(self, spacecraft='JUICE',
                                 dsk_frame='JUICE_EPT',
                                 abcorr='None',
                                 interval=60,
                                 target='JUPITER',
                                 max_dist_to_torus_center_km=900000,
                                 min_dist_to_torus_center_km=0):
        """
        Calculate periods where spacecraft is within moon plasma torus

        the output listing all events types the output listing all events types

        0) Select periods where Juice spacecraft distance to Jupiter is within
        [max_dist_to_torus_center_km, min_dist_to_torus_center_km]. This allows to improve drastically the next step

        Search for other intercept points (When pointing to Jupiter, ceeenter of Torus) :

            Cases (ideal):

                1) There are 3 intercept point:

                    We select just the fisr one.

        :param spacecraft: spacecraft identifier (juice)
        :param dsk_frame: Spice Naif referential frame where dsk is given and intercept points calculated
        :param abcorr: aberration correction
        :param interval: step in seconds
        :param target: target name/identifier (i.e. earth, jupiter)
        :param min_dist_to_torus_center_km: minimum distance sc_Jupiter to search intercept surface point
        :param max_dist_to_torus_center_km: maximum distance sc_Jupiter to search intercept surface point
        :return: values:  list of events types together with associated contextual geometry
        """

        logging.info('Calculating Position vector (km) and planetocentric coordinate in surface intercept ...')
        logging.info('Overall periods [{} - {}]'.format(tds_spicey.et2utc(self.start), tds_spicey.et2utc(self.end)))

        gti = [[self.start, self.end]]

        n = int((self.end - self.start) / interval)
        tt = self.start + np.array(range(n)) * interval

        gti = GfDistance().get_distance_range_periods(gti, 'Jupiter', spacecraft,
                                                      min_dist_to_torus_center_km,
                                                      max_dist_to_torus_center_km,
                                                      abcorr, 0, 600)

        nb_periods = len(gti)
        logging.info('Found {} Periods '
                     'where distance juice-to-Jupiter in [{}, {}] km'.format(nb_periods,
                                                                             min_dist_to_torus_center_km,
                                                                             max_dist_to_torus_center_km, ))

        logging.info('Print up to 100 first periods')

        count = 0
        for s, e in gti:
            count += 1
            if count <= 100:
                logging.info("{}: {} {} {} {}".format(count,
                                               spi.et2utc(s, "ISOC", 3, 25),
                                               spi.et2utc(e, "ISOC", 3, 25), round(s), round(e)))

        etimes = gti_handler.gti_where_extended(tt, gti)[3]
        nb_etimes = len(etimes)

        if nb_etimes == 0:
            logging.info('There are no potential to check, the stop!')
            sys.exit()

        per_to_check = 10
        group_counter = 0
        nb_intercept = 0
        sum_of_intercept_points = 0

        nb_prev_sol = 0

        values = []

        logging_text = '{}% processed; [{} - {}]; {} sc_to_jupiter_ray intersecting plasma torus ({} intercept points)'
        start_sub_period = tds_spicey.et2utc(tt[0], format='%d-%b-%Y_%H:%M:%S')

        count = 0
        for et in etimes:

            try:

                # If a ray spacecraft_to_earth intersects the surface at multiple points,

                ev_utc = tds_spicey.et2utc(et, format='%Y-%jT%H:%M:%S')  # '2030-280T05:06:22'
                ev_utc_cal = tds_spicey.et2utc(et, format='%d-%b-%Y_%H:%M:%S')  # '07-OCT-2030_05:06:22'
                # print(i, et, ev_utc, ev_utc_cal)

                spoints = self.found_points(spacecraft, et, dsk_frame, abcorr, target)

                nb_spoints = len(spoints)

                if nb_spoints > 0:

                    if len(spoints) != nb_prev_sol:

                        if nb_prev_sol > 0:
                            logging.debug('{}: End of {} solutions!'.format(ev_utc_cal, nb_prev_sol))

                        logging.debug('found {}: {} solutions!'.format(ev_utc_cal, len(spoints)))
                        nb_prev_sol = len(spoints)

                    vec_pos_sc_from_jupiter = np.array(spi.spkpos(spacecraft, et, dsk_frame, abcorr, 'JUPITER')[0])
                    _, lon_sc, _ = spi.reclat(vec_pos_sc_from_jupiter)

                    if nb_spoints == 1:

                        nb_intercept += 1
                        sum_of_intercept_points += nb_spoints
                        group_counter += 1

                        event_id = 'occ_egress_primary_only'

                        point, radius, lon, lat = spoints[0]

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, nb_spoints, group_counter]

                        values.append(occ_ingress)

                    elif nb_spoints == 3:

                        nb_intercept += 1
                        sum_of_intercept_points += nb_spoints
                        group_counter += 1

                        event_id = 'occ_egress_primary'

                        point, radius, lon, lat = spoints[0]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_ingress_secondary'

                        point, radius, lon, lat = spoints[1]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_egress_secondary'

                        point, radius, lon, lat = spoints[2]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, nb_spoints, group_counter]

                        values.append(occ_ingress)

            except SpiceyError as exc:

                # Display a message if an exception was thrown.
                # For simplicity, we treat this as an indication that the point of intersection was not found,
                # although it could be due to other errors. Otherwise, continue with the calculations.

                message = [l for l in exc.message.split('\n')[4:-1] if l != '']
                message = '; '.join(message)

                logging.debug(('{:s} at et{:f} - {:s}'.format(
                    message, round(et), tds_spicey.et2utc(et, format='%d-%b-%Y_%H:%M:%S'))))

            count += 1
            per_step = int(count * 100 / nb_etimes)

            if per_step >= per_to_check:
                logging.info(logging_text.format(per_step, start_sub_period, ev_utc_cal, nb_intercept,
                                                 sum_of_intercept_points))

                per_to_check += 10

        # logging.info(logging_text.format(100,
        #                                  start_sub_period, ev_utc_cal, nb_intercept, sum_of_intercept_points))

        return values

    def found_points(self, spacecraft, et, dsk_frame, aber_corr, target='earth'):
        """
        Calculate point intersect of "target - origin" and torus

        1) get srflst id
        2) get origin and target rectilinear coordinate in dsk_frame
        3) get point intersect of "target - origin" and torus


        :param spacecraft: spacecraft spice identifier (juice)
        :param et: ephemeris time
        :param dsk_frame: dsk frame for TORUS
        :param aber_corr: aberration correction
        :param target: Target/name identifier (i.e. earth)
        :return: points
        """

        # 1) get srflst id and ttorud identifier

        srflst = self.srflst
        torus_target_id = self.torus_target_id
        # logging.debug('srflst = {}'.format(srflst))

        # 2) get origin and target rectilinear coordinate in dsk_frame,
        # Actually since torus_target_id <=> target = Jupiter; origin like spi.vminus(ray)

        origin = spi.spkpos(spacecraft, et, dsk_frame, aber_corr, target)[0]

        ray = spi.spkpos(target, et, dsk_frame, aber_corr, spacecraft)[0]

        # 3) get point intersect of "target - origin" and torus

        ori2target = np.array(ray) - np.array(origin)

        flag = 1

        coord = []

        while flag == 1:

            try:

                xptarr, fndarr = spi.dskxv(False, torus_target_id, srflst, et, dsk_frame, origin, ray)

                if fndarr[0] != 0:  # [0, 0, 0]:
                    r0, lon_0, lat_0 = spi.reclat(xptarr[0])
                    lon_0 *= spi.dpr()
                    lat_0 *= spi.dpr()
                    # xyzhit = spi.latrec(r0, lon_0, lat_0)
                    # d = spi.vdist(xptarr[0], xyzhit)
                    # logging.debug('{}:|--> {} {} {} {}'.format(fndarr, xptarr[0], r0, lon_0, lat_0))
                    coord.append([xptarr[0], r0, lon_0, lat_0])
                    origin = xptarr[0] + ray / np.linalg.norm(ray) * 1e-6
                    # origin = xptarr[0] + ori2target / np.linalg.norm(ori2target)
                    r0, lon_0, lat_0 = spi.reclat(origin)
                    lon_0 *= spi.dpr()
                    lat_0 *= spi.dpr()
                    # logging.debug('new origin: {} <=> (lon, lat, r) = ({:12.2f}, {:12.2f}, {:12.2f})'.format(
                    #     origin, lon_0, lat_0, r0))

                    # Check point found is aligned with "spacecraft to target ray": This is a sanity check
                    # self.check_point_aligned_with_ray_vector(ray, origin, ori2target)

                flag = fndarr[0]

            except SpiceyError as exc:

                # Display a message if an exception was thrown.
                # For simplicity, we treat this as an indication that the point of intersection was not found,
                # although it could be due to other errors. Otherwise, continue with the calculations.

                logging.debug('{} {} {} {} {}'.format(torus_target_id, srflst, et, origin[0], ray[0]))

                message = [l for l in exc.message.split('\n')[4:-1] if l != '']
                message = '; '.join(message)

                logging.debug(('{:s} at et{:f} - {:s}'.format(
                    message, round(et), tds_spicey.et2utc(et, format='%d-%b-%Y_%H:%M:%S'))))

                flag = 0

        return coord

    def check_is_back_torus_intercept(self, ref_longitude, point):
        """
        Check if point intercept is located in the forward or backward part of the Torus as seen from observer

        Condition: separation vector sc_to_jupiter and jupiter_to_spoint < 90 deg

        if condition == True:
            point is located in IO-TORUS backward part
        else:
            point is located in IO-TORUS forward part

        :param et: ephemeris time
        :param observer: position observer in the reference frame (i.e. frame=IAU_JUPITER; observer= spacecraft)
        :param dsk_frame: reference frame for the IO_TORUS where point is located (i.e. dsk_frame=IAU_JUPITER)
        :param point: position (x,y,z) in dsk_frame
        :return: is_back_torus_intercept:
            flag = 0 is point is located in IO-TORUS forward part as seen from observer, else if backward return 1
        """

        # check with the ray intercept the forward part of the IO-TORUS
        # Condition: separation vector - sc_jupiter and jupiter_spoint < 90 deg
        # Note point is the position vector of spoint from Jupiter in IAU_frame

        _, lon_intercept_point, _ = spi.reclat(point)
        lon_intercept_point = np.rad2deg(lon_intercept_point)

        if not isinstance(ref_longitude, float):
            _, ref_longitude, _ = spi.reclat(ref_longitude)
        ref_longitude = np.rad2deg(ref_longitude)

        diff_longitude = lon_intercept_point - ref_longitude

        is_back_torus_intercept = 0
        if abs(diff_longitude) > 90:
            is_back_torus_intercept = 1

        return is_back_torus_intercept


def get_sc_within_moon_torus_periods(connection, table_name, event_eps_name=None, event_name='occ_%_primary',
                                     debug=False, dt=60):
    """
    Get spacecraft within moon torus periods

    1) get opportunity periods (start, end events +  contextual parameters)

    2) include periods where no radio source raised the spacecraft

    :param connection: db connection object
    :param table_name: sql table names
    :param event_name: event identifier filter
    :param debug: flag enforcing debugging
    :param event_eps_name: eps event identifier filter; take event_name if None; Default value is None
    :param dt: simulation step time =  60 seconds per defaults
    :return data: periods where spacecraft within moon torus periods
    """

    query = 'select * from {} where ev_type like "{}"'.format(table_name, event_name)
    df0 = pd.read_sql_query(query, con=connection)
    if debug:
        print(len(df0['ev_et']))
        print_df_as_tab(df0[:10])

    ev_et = {}

    df2 = df0.sort_values('ev_et').drop_duplicates('ev_et')
    df2 = df2.drop(columns=['is_back_torus_intercept', 'nb_intercept_points', 'group_counter', 'dsk_frame'])

    for index, row in df2.iterrows():  # Record parameters for each times

        ev_et[row['ev_et']] = row.tolist()[1:]

    etimes = list(sorted(ev_et.keys()))

    opportunity_periods = gti_handler.gti_seg(etimes, dt * 1.05, dt=dt)

    event_sql_name = 'event'
    if event_eps_name:
        event_sql_name = event_eps_name.upper()

    event_start = "{}_START".format(event_sql_name)
    event_end = "{}_END".format(event_sql_name)

    data = []
    windows_periods = []

    for s, e in opportunity_periods:
        data.append([event_start] + ev_et[s][1:])
        data.append([event_end] + ev_et[e - dt][1:])  # gti_Seg add by default dt for the opportunity end

        windows_periods.append([ev_et[s][2], ev_et[e - dt][2]])  # start, end periods in UTC (i.e. 01-JUN-2032_19:10:21)

    return data, windows_periods


def generate_sql_table(data, output_dir, mysql_config=None, table_name='juice_crema_5_0_sc_within_europa_torus'):
    """
    Create Mysql table and generate the corresponding sql dump file

    :param data: dataframe object containing radio source events
    :param mysql_config: path of mysql_config file including database connection parameters
    :param output_dir: output directory path
    :param table_name: Name of sql dump file
    """

    if not os.path.exists(mysql_config):
        logging.error('my_sql connexion file does no exist:{}'.format(mysql_config))
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    db.create_db_table_object_within_moon_plasma_torus(table_name, engine='InnoDB')

    logging.info('Inserting records in table {} ...'.format(table_name))

    db.insert_into_table(table_name, data)
    logging.info('{} records inserted'.format(len(data)))

    # db.dump_table(table_name)

    db.close()


def generate_simple_ql_table(output_dir, event_eps_name, mysql_config=None,
                             table_name_query='juice_crema_5_0_sc_within_europa_torus',
                             table_name='juice_crema_5_0_simple_sc_within_europa_torus', dt=60):
    """
    Create Mysql table and generate the corresponding sql dump file

    :param mysql_config: path of mysql_config file including database connection parameters
    :param event_eps_name: event_type name mask (i.e. JUICE_WITHIN_EPT)
    :param output_dir: output directory path
    :param table_name_query: Name of table to query
    :param table_name: Name of table to create,
    :param dt: simulation step time =  60 seconds per defaults
    """

    if not os.path.exists(mysql_config):
        logging.error('my_sql connexion file does no exist:{}'.format(mysql_config))
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    db.create_db_table_object_within_moon_plasma_torus_simple(table_name, engine='InnoDB')

    data, _ = get_sc_within_moon_torus_periods(db.get_mysql_connector(), table_name_query, event_eps_name, dt=dt)

    logging.info('Inserting records in table {} ...'.format(table_name))
    db.insert_into_table(table_name, data)
    logging.info('{} records inserted'.format(len(data)))

    db.dump_table(table_name)

    db.close()


def generate_segment(output_dir, event_name, mysql_config=None,
                     table_name_query='juice_crema_5_0_sc_within_europa_torus',
                     working_group='WG3', dt=60):
    """
    Create Segment file (Juice)

    :param output_dir: output directory path
    :param event_name: event_type name mask (i.e. JUICE_WITHIN_EPT)
    :param mysql_config: path of mysql_config file including database connection parameters
    :param table_name_query='juice_crema_5_0_sc_within_europa_torus'
    :param working_group: Juice working group WG[1234X]
    :param dt: simulation step time =  60 seconds per defaults
    """

    if not os.path.exists(mysql_config):
        logging.error('my_sql connexion file does no exist:{}'.format(mysql_config))
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    _, opportunity_periods = get_sc_within_moon_torus_periods(db.get_mysql_connector(), table_name_query, dt=dt)
    db.close()

    file_name = os.path.join(output_dir, event_name + '.csv')
    f_out = open(file_name, 'w')

    event_name = event_name.upper()

    for s, e in opportunity_periods:
        f_out.write('{},{},{},{},{}\n'.format(event_name, s, e, '', working_group))

    f_out.close()

    logging.info('New segment files created: {}'.format(file_name))


def generate_eps_event_file(output_dir, event_cfg, mysql_config=None,
                            table_name_query='juice_crema_5_0_sc_within_europa_torus', dt=60):
    """
    Create eps_event_file

    :param output_dir: output directory path
    :param event_cfg: event parameters
    :param mysql_config: path of mysql_config file including database connection parameters
    :param table_name_query='juice_crema_5_0_sc_within_europa_torus'
    :param dt: simulation step time =  60 seconds per defaults
    :return:
    """

    import datetime

    if not os.path.exists(mysql_config):
        logging.error('my_sql connexion file does no exist:{}'.format(mysql_config))
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    _, opportunity_periods = get_sc_within_moon_torus_periods(db.get_mysql_connector(), table_name_query, dt=dt)
    db.close()

    event_type = event_cfg['event_type']
    event_type_start = event_cfg['active']
    event_type_end = event_cfg['inactive']

    number_of_events = len(opportunity_periods)

    file_name = os.path.join(output_dir, event_type + '.evf')

    if number_of_events == 0:

        logging.warning('Cannot create event file {}; not events found!'.format(file_name))

    else:

        start, end = opportunity_periods[0][0], opportunity_periods[-1][1],

        f_out = open(file_name, 'w')

        author = 'auto'
        revision = '0001'
        id = 'TBD'
        description = ''

        creation_date = datetime.datetime.now()

        header = '#\n# EVF Filename: {}'.format(os.path.basename(file_name)) \
                 + '\n# Generation Time: {}'.format(datetime.datetime.strftime(creation_date, '%d-%b-%Y_%H:%M:%S')) \
                 + '\n#\n# Author   : {}'.format(author) \
                 + '\n# ID  : {}'.format(id) \
                 + '\n# Revision : {}\n'.format(revision) \
                 + '\n# Description : {}\n'.format(description) \
                 + '\nStart_time: {}'.format(start) \
                 + '\nEnd_time: {}\n\n'.format(end)

        header += '\n# ({} events in list)\n'.format(number_of_events)

        f_out.write(header)

        count = 0
        for s, e in opportunity_periods:
            count += 1
            f_out.write('{} {} (COUNT = {})\n'.format(event_type_start, s, count))
            f_out.write('{} {} (COUNT = {})\n'.format(event_type_end, e, count))

        f_out.close()

        logging.info('New event file {} created'.format(file_name))
