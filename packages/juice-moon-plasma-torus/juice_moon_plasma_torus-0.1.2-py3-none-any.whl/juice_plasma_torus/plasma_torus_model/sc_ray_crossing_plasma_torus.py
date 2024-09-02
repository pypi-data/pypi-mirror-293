"""
Created on Jan, 2021

@author: Claudio Munoz Crego (ESAC)

Python module to handle Plasma Torus Model

"""

import logging
import os
import sys

import numpy as np
import pandas as pd
import spiceypy as spi
from spiceypy.utils.exceptions import SpiceyError

import esac_juice_pyutils.commons.tds_spicey as tds_spicey
import esac_juice_pyutils.gti.gti_handler as gti_handler
import juice_plasma_torus.commons.numpy_utils as npp
from juice_plasma_torus.plasma_torus_model.gs_occult import get_occulted_periods_by_moon_plama_torus_dsk
from juice_plasma_torus.plasma_torus_model.gs_occult import get_occulted_periods_by_moon_plasma_torus_dsk
from juice_plasma_torus.plasma_torus_model.mysql_connector_plasma_torus import MysqlConnectorMoonTorus
from juice_plasma_torus.plasma_torus_model.plasma_torus import PlasmaTorus, print_df_as_tab


class PlasmaTorus(PlasmaTorus):

    def __init__(self, config):

        self.config = config

        self.output_dir = config['output_path']

        self.load_spice_kernels(config['kernel'])
        self.srflst = self.get_surface_id_from_dsk(dsk_file_path=self.config['dsk'][0])
        self.torus_target_id = self.config['torus_target_id']

        self.start = spi.utc2et(self.config['start_time_utc'])
        self.end = spi.utc2et(self.config['end_time_utc'])

    def generate_intercept_ingres_egres(self,
                                        spacecraft,
                                        dsk_frame,
                                        abcorr='None',
                                        interval=60,
                                        target='earth',
                                        max_dist_to_torus_center_km=900000,
                                        min_dist_to_torus_center_km=0,
                                        torus_max_rj_radius=12):

        """
        Calculate when a ray between spacecraft (observer) and target (earth) intercepts a given Juice moon Plasma Torus
        identifying all occultation events type (egress and ingress, primary and secondary) by the Io torus,
        together with a set of corresponding contextual geometry

        the output listing all events types
        (occ_ingress_primary, occ_egress_primary, occ_ingress_secondary, occ_egress_secondary)
        together with associated contextual geometry (e.g. lat/lon at occulting point in IAU_JUPITER for now,
        MLG visibility flag, communication flag).

        0) Select periods where Juice spacecraft distance to Jupiter is within
        [max_dist_to_torus_center_km, min_dist_to_torus_center_km]. This allows to improve drastically the next step

        Search for other intercept points:

            Cases (ideal):

                1) There is only one intercept point:

                    is_back_torus_intercept = 0; and then occ_ingress_primary = occ_egress_primary
                    is_back_torus_intercept = 1; and then occ_ingress_secondary = occ_egress_secondary

                2) There are 2 intercept points:

                    is_back_torus_intercept = 0; and then points are occ_ingress_primary and occ_egress_primary
                    is_back_torus_intercept = 1; and then points are occ_ingress_secondary and occ_egress_secondary

                3) there are 4 intercept points:

                    is_back_torus_intercept = 0
                    points are occ_ingress_primary, occ_egress_primary, occ_ingress_secondary, occ_egress_secondary

            Cases with missing points due to holes in TORUS DSK model:

                # dsk are not perfect since there are formed by plates, holes and duplicates values can exist.
                # This entails no solutions or unexpected solutions (not 1,2,3,4) could be found.
                # Those unexpected solution(s) will be notified by warning log in standard output and ignored.


        :param spacecraft: spacecraft identifier (juice)
        :param dsk_frame: Spice Naif referential frame where dsk is given and intercept points calculated
        :param abcorr: aberration correction
        :param interval: step in seconds
        :param target: target name/identifier (i.e. earth, jupiter)
        :param min_dist_to_torus_center_km: minimum distance sc_Jupiter to search intercept surface point
        :param max_dist_to_torus_center_km: maximum distance sc_Jupiter to search intercept surface point
        :param torus_max_rj_radius:
        :return: values:  list of events types together with associated contextual geometry
        """

        logging.info('Start Intercept Calculation')

        logging.info('Calculating Position vector (km) and planetocentric coordinate in surface intercept ...')
        logging.info('Overall periods [{} - {}]'.format(tds_spicey.et2utc(self.start), tds_spicey.et2utc(self.end)))

        gti_0 = [[self.start, self.end]]

        self.malargues_vis, self.malargues_pass = self.get_malargue_passes(gti_0)

        n = int((self.end - self.start) / interval)
        tt = self.start + np.array(range(n)) * interval

        # gti_dist = GfDistance().get_distance_periods(gti_0, 'Jupiter', spacecraft,
        #                                             max_dist_to_torus_center_km, '>', abcorr, 0, 600)
        #
        # nb_periods = len(gti_dist)
        # logging.info('Found {0} Periods '
        #              'where moon plasma Torus occulting earth for '
        #              'distance juice-to-Jupiter > {1} '.format(nb_periods,
        #                                                        max_dist_to_torus_center_km))
        #
        # logging.info('Print up to 10 first periods')
        #
        # count = 0
        # for s, e in gti_dist:
        #     count += 1
        #     if count <= 10:
        #         logging.info("{}: {} {} {} {}".format(count,
        #                                               spi.et2utc(s, "ISOC", 3, 25),
        #                                               spi.et2utc(e, "ISOC", 3, 25), round(s), round(e)))

        gti_occulted = get_occulted_periods_by_moon_plama_torus_dsk(gti_0, self.config)

        nb_periods = len(gti_occulted)
        logging.info('Found {0} Periods where moon plasma Torus occulting earth observed from Juice'.format(nb_periods))

        logging.info('Print up to up to 100 first periods earth occulted by Torus when observed by Juice')
        count = 0
        for s, e in gti_occulted:
            count += 1
            if count <= 100:
                logging.info("{}: {} {}".format(count, spi.et2utc(s, "ISOC", 3, 25), spi.et2utc(e, "ISOC", 3, 25)))

        gti = gti_occulted
        # git_dist_in = gti_handler.gti_inverse(gti_dist, self.start, self.end)

        # gti = gti_handler.gti_merge(gti_occulted, git_dist_in)

        # gti_dist = GfDistance().get_distance_range_periods(gti, 'Jupiter', spacecraft,
        #                                                    min_dist_to_torus_center_km,
        #                                                    max_dist_to_torus_center_km,
        #                                                    abcorr, 0, 600)
        #
        # gti_dist_ang = self.get_potential_sc2eath_ray_intercept_moon_plasma_torus(tt, torus_max_rj_radius)
        #
        # gti = gti_handler.gti_merge
        # (gti_dist, gti_dist_ang)
        #
        # select et where earth is not occulted by a body (i.e. juice)
        if 'remove_periods_where_earth_occulted_by_jupiter' in list(self.config.keys()):

            if self.config['remove_periods_where_earth_occulted_by_jupiter']:

                non_occulted_period = self.get_non_occulted_periods()
                gti = gti_handler.gti_overlap(gti, non_occulted_period)

                gti = gti_handler.gti_trim(gti, max_gap=interval * 1.05, min_gti=interval)

                logging.info('Removed periods where earth is occulted by Jupiter')

        if 'remove_periods_where_earth_occulted_by_io_torus' in list(self.config.keys()):

            if self.config['remove_periods_where_earth_occulted_by_io_torus']:

                occulted_periods = get_occulted_periods_by_moon_plasma_torus_dsk(gti, self.config['io_torus_occultation'])

                non_occulted_period = gti_handler.gti_inverse(occulted_periods, start=self.start, end=self.end)
                gti = gti_handler.gti_overlap(gti, non_occulted_period)

                gti = gti_handler.gti_trim(gti, max_gap=interval * 1.05, min_gti=interval)

                logging.info('Removed periods where earth is occulted by Jupiter')

        nb_periods = len(gti)
        logging.info('Found {0} Periods '
                     'where distance juice-to-Jupiter in [{1}, {2}] km, '
                     'or where moon plasma Torus occulting earth for '
                     'distance juice-to-Jupiter > {1} '.format(nb_periods,
                                                                 min_dist_to_torus_center_km,
                                                                 max_dist_to_torus_center_km))

        logging.info('Print up to 10 first periods')

        count = 0
        for s, e in gti:
            count += 1
            if count <= 150:
                logging.info("{}: {} {} {} {}".format(count,
                                                      spi.et2utc(s, "ISOC", 3, 25),
                                                      spi.et2utc(e, "ISOC", 3, 25), round(s), round(e)))

        etimes = gti_handler.gti_where_extended(tt, gti)[3]
        nb_etimes = len(etimes)

        if nb_etimes == 0:
            logging.info('There are no potential to check, the stop!')
            sys.exit()

        values = []

        per_to_check = 10
        group_counter = 0
        nb_intercept = 0
        sum_of_intercept_points = 0

        nb_prev_sol = 0

        logging_text = '{}% processed; [{} - {}]; {} sc_to_earth_ray intersecting plasma torus ({} intercept points)'
        start_sub_period = tds_spicey.et2utc(tt[0], format='%d-%b-%Y_%H:%M:%S')

        ev_utc_cal = ''

        logging.info('number of etimes: {}'.format(nb_etimes))

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

                    if nb_spoints != nb_prev_sol:

                        if nb_prev_sol > 0:
                            logging.debug('{}: End of {} solutions!'.format(ev_utc_cal, nb_prev_sol))

                        logging.debug('found {}: {} solutions!'.format(ev_utc_cal, len(spoints)))
                        nb_prev_sol = nb_spoints

                    gs_vis, gs_pass = self.is_sc_visible_from_gs(et)

                    nb_intercept += 1
                    sum_of_intercept_points += nb_spoints

                    vec_pos_sc_from_jupiter = np.array(spi.spkpos(spacecraft, et, dsk_frame, abcorr, 'JUPITER')[0])
                    _, lon_sc, _ = spi.reclat(vec_pos_sc_from_jupiter)

                    if nb_spoints == 1:

                        group_counter += 1

                        event_id = 'occ_ingress_primary_only'

                        point, radius, lon, lat = spoints[0]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                    elif nb_spoints == 2:

                        group_counter += 1

                        event_id = 'occ_ingress_primary'

                        point_0, radius, lon, lat = spoints[0]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point_0)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_egress_secondary'

                        point, radius, lon, lat = spoints[1]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(point_0, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                    elif nb_spoints == 3:

                        nb_intercept += 1
                        sum_of_intercept_points += nb_spoints
                        group_counter += 1

                        event_id = 'occ_egress_primary'

                        point, radius, lon, lat = spoints[0]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_ingress_secondary'

                        point, radius, lon, lat = spoints[1]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_egress_secondary'

                        point, radius, lon, lat = spoints[2]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                    elif nb_spoints == 4:

                        group_counter += 1

                        event_id = 'occ_ingress_primary'

                        point_0, radius, lon, lat = spoints[0]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point_0)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_egress_primary'

                        point, radius, lon, lat = spoints[1]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(point_0, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_ingress_secondary'

                        point, radius, lon, lat = spoints[2]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(point_0, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                        event_id = 'occ_egress_secondary'

                        point, radius, lon, lat = spoints[3]

                        is_back_torus_intercept = self.check_is_back_torus_intercept(point_0, point)

                        occ_ingress = [event_id, ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                       is_back_torus_intercept, gs_vis, gs_pass, nb_spoints, group_counter]

                        values.append(occ_ingress)

                    elif nb_spoints > 4:

                        logging.warning('{}: --> {} solutions > 4!'.format(ev_utc_cal, len(spoints)))

                    else:

                        logging.warning('{}: --> {} solutions, expected are 1,2 or 4!'.format(ev_utc_cal, len(spoints)))

                        ingres_counter = 1
                        egres_counter = 1

                        for p in spoints:

                            point, radius, lon, lat = p

                            # check with the ray intercept the forward part of the IO-TORUS
                            is_back_torus_intercept = self.check_is_back_torus_intercept(lon_sc, point)
                            if is_back_torus_intercept:
                                logging.debug("intercept backward par of IO_TORUS: '{}','{}','{}','{}',{},{},{}".format(
                                    ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius))

                            occ_ingress = [ev_utc, ev_utc_cal, et, dsk_frame, lon, lat, radius,
                                           is_back_torus_intercept, gs_vis, gs_pass]

                            if is_back_torus_intercept:
                                event_id = 'occ_egress_{}'.format(egres_counter)
                                egres_counter += 1
                            else:
                                event_id = 'occ_ingress_{}'.format(ingres_counter)
                                ingres_counter += 1

                            logging.warning('{}'.format([event_id] + occ_ingress))

                elif len(spoints) != nb_prev_sol:

                    logging.debug('{}: End of {} solutions!'.format(ev_utc_cal, nb_prev_sol))
                    nb_prev_sol = len(spoints)

            except SpiceyError as exc:

                # Display a message if an exception was thrown.
                # For simplicity, we treat this as an indication that the point of intersection was not found,
                # although it could be due to other errors. Otherwise, continue with the calculations.

                message = [l for l in exc.message.split('\n')[4:-1] if l != '']
                message = '; '.join(message)

                logging.debug(('{:s} at et{:f} - {:s}'.format(
                    message, round(et), tds_spicey.et2utc(et, format='%d-%b-%Y_%H:%M:%S'))))

            count += 1
            per_step = int(count * 100 /nb_etimes)

            if per_step >= per_to_check:
                logging.info(logging_text.format(per_step, start_sub_period, ev_utc_cal, nb_intercept,
                                                 sum_of_intercept_points))

                per_to_check += 10

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

        # 2) get origin and target rectilinear coordinate in dsk_frame

        origin = spi.spkpos(target, et, dsk_frame, aber_corr, torus_target_id)[0]

        ray = - spi.spkpos(target, et, dsk_frame, aber_corr, spacecraft)[0]

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

                    coord.append([xptarr[0], r0, lon_0, lat_0])
                    origin = xptarr[0] + ray / np.linalg.norm(ray) * 1e-6

                    r0, lon_0, lat_0 = spi.reclat(origin)
                    lon_0 *= spi.dpr()
                    lat_0 *= spi.dpr()

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

    def check_point_aligned_with_ray_vector(self, point, vect_origin, ori2target):
        """
        Check point found is aligned with spacecraft to target ray

        Note: both point and origin coordinates must be provided in the same reference frames

        :param point: Rectilinear coordinates xyz
        :param vect_origin: vector origin in rectilinear coordinates xyz (i.e. spacecraft)
        :return:
        """

        ori2fundarr = np.array(point) - np.array(vect_origin)

        vsep = (spi.vsep(ori2target, ori2fundarr))
        tang_vsep = np.tan(vsep)
        ori2target_norm = spi.vnorm(ori2target)
        if vsep >= 0.1:
            logging.warning(
                'sep angle = {:15.6f} deg; err target pos = {} km'.format(vsep, tang_vsep * ori2target_norm))

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
        if abs(diff_longitude) > 45:
            is_back_torus_intercept = 1

        return is_back_torus_intercept

    def check_is_back_torus_intercept_2(self, et, observer, dsk_frame, point, abcorr='LT+S'):
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

        vec_pos_sc_from_jupiter = np.array(spi.spkpos(observer, et, dsk_frame, abcorr, 'JUPITER')[0])
        ang_sc_jupiter_spoint = spi.vsep(vec_pos_sc_from_jupiter, point) * spi.dpr()

        is_back_torus_intercept = 0
        if ang_sc_jupiter_spoint > 90:
            is_back_torus_intercept = 1

        return is_back_torus_intercept

    def get_moon_torus_apparent_size(self, etimes, torus_max_rj_radius, sc='juice',
                                     target='Jupiter', ref_frame='J2000', abcorr='None',
                                     ):

        """
        1) Get the radius of the body from spice kernel

        :param etimes: list of ephemeris times
        :param sc: spacecraft identifier (juice)
        :param abcorr: aberration correction
        :param ref_frame: Spice naif reference frame
        :param torus_max_rj_radius: number of Jupiter Radius for moon plasma torus max distance
        :param target: source target identifier (i.e. Jupiter)
        :return: apparent_size, apparent size of Moon torus
        """

        r_jupiter = spi.bodvrd(sc, 'RADII', 3)[1][0]

        v_sc_to_jupiter = spi.spkpos(sc, etimes, ref_frame, abcorr, sc)[0]
        dist_sc_jupiter = np.linalg.norm(v_sc_to_jupiter, axis=1)

        torus_max_radius = torus_max_rj_radius * r_jupiter

        apparent_size = np.rad2deg(np.arctan2(torus_max_radius / dist_sc_jupiter))

        return apparent_size

    def get_potential_sc2eath_ray_intercept_moon_plasma_torus(self, etimes, torus_max_rj_radius, sc='juice',
                                                              target='Jupiter', ref_frame='J2000', abcorr='None'):
        """

        Does not work if dist_sc_jupiter < torus_max_rj_radius * r_jupiter

        Get the potential periods where a spacecraft-to-earth ray intercept the moon plasma torus,
        checking the separation angle Jupiter-spacecraft-earth < moon_torus_apparent_size

        jupiter-spacecraft-earth separation angle <= arctang (torus_max_radius / dist_sc_jupiter)

        :param etimes: list of ephemeris times
        :param sc: spacecraft identifier (juice)
        :param abcorr: aberration correction
        :param ref_frame: Spice naif reference frame
        :param torus_max_rj_radius: number of Jupiter Radius for moon plasma torus max distance
        :return:
        """

        r_jupiter = spi.bodvrd(target, 'RADII', 3)[1][0]

        v_sc_to_jupiter = spi.spkpos(target, etimes, ref_frame, abcorr, sc)[0]
        dist_sc_jupiter = np.linalg.norm(v_sc_to_jupiter, axis=1)

        torus_max_radius = torus_max_rj_radius * r_jupiter

        moon_torus_apparent_size = np.rad2deg(np.arctan2(torus_max_radius, dist_sc_jupiter))

        v_sc_to_earth = np.array(spi.spkpos('EARTH', etimes, ref_frame, abcorr, sc)[0])

        v1 = npp.normalize(v_sc_to_jupiter, 1)
        v2 = npp.normalize(v_sc_to_earth, 1)

        jupiter_sc_earth_angle = np.rad2deg(np.arccos(np.sum(v1 * v2, axis=1)))

        gti_angle = gti_handler.gti_val(etimes, 90 - np.abs(jupiter_sc_earth_angle))
        gti_dist = gti_handler.gti_val(etimes, dist_sc_jupiter > torus_max_radius)

        gti = gti_handler.gti_overlap(gti_angle, gti_dist)

        return gti

    def get_potential_sc2eath_ray_intercept_moon_plasma_torus_2(self, etimes, torus_max_rj_radius, sc='juice',
                                                                target='Jupiter', ref_frame='J2000', abcorr='None'):
        """

        Does not work if dist_sc_jupiter < torus_max_rj_radius * r_jupiter

        Get the potential periods where a spacecraft-to-earth ray intercept the moon plasma torus,
        checking the separation angle Jupiter-spacecraft-earth < moon_torus_apparent_size

        jupiter-spacecraft-earth separation angle <= arctang (torus_max_radius / dist_sc_jupiter)

        :param etimes: list of ephemeris times
        :param sc: spacecraft identifier (juice)
        :param abcorr: aberration correction
        :param ref_frame: Spice naif reference frame
        :param torus_max_rj_radius: number of Jupiter Radius for moon plasma torus max distance
        :return:
        """

        r_jupiter = spi.bodvrd(target, 'RADII', 3)[1][0]

        v_sc_to_jupiter = spi.spkpos(target, etimes, ref_frame, abcorr, sc)[0]
        dist_sc_jupiter = np.linalg.norm(v_sc_to_jupiter, axis=1)

        torus_max_radius = torus_max_rj_radius * r_jupiter

        moon_torus_apparent_size = np.rad2deg(np.arctan2(torus_max_radius, dist_sc_jupiter))

        v_sc_to_earth = np.array(spi.spkpos('EARTH', etimes, ref_frame, abcorr, sc)[0])

        v1 = npp.normalize(v_sc_to_jupiter, 1)
        v2 = npp.normalize(v_sc_to_earth, 1)

        jupiter_sc_earth_angle = np.rad2deg(np.arccos(np.sum(v1 * v2, axis=1)))

        gti = gti_handler.gti_val(etimes, moon_torus_apparent_size - np.abs(jupiter_sc_earth_angle))

        return gti


def get_sc_to_eart_ray_crossing_moon_torus_periods(connection, table_name, event_eps_name=None, event_name='occ_%_primary',
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
    df2 = df2.drop(columns=['dsk_frame'])

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


def generate_segment(output_dir, event_name, mysql_config=None,
                     table_name_query='juice_crema_5_0_intercept_sc2earth_ray_europa_torus_detailed',
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
        logging.error(f'my_sql connexion file does not exist:{mysql_config}')
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    _, opportunity_periods = get_sc_to_eart_ray_crossing_moon_torus_periods(
        db.get_mysql_connector(), table_name_query, dt=dt)
    db.close()

    file_name = os.path.join(output_dir, event_name + '.csv')
    f_out = open(file_name, 'w')

    event_name = event_name.upper()

    for s, e in opportunity_periods:
        f_out.write('{},{},{},{},{}\n'.format(event_name, s, e, '', working_group))

    f_out.close()

    logging.info('New segment files created: {}'.format(file_name))


def generate_eps_event_file(output_dir, event_cfg, mysql_config=None,
                            table_name_query='juice_crema_5_0_intercept_sc2earth_ray_europa_torus_detailed', dt=60):
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
        logging.error(f'my_sql connexion file does not exist:{mysql_config}')
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    _, opportunity_periods = get_sc_to_eart_ray_crossing_moon_torus_periods(
        db.get_mysql_connector(), table_name_query, dt=dt)
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


def generate_sql_table(data, output_dir, mysql_config=None,
                       table_name='juice_crema_5_0_intercept_sc2earth_ray_europa_torus_detailed'):
    """
    Create Mysql table and generate the corresponding sql dump file

    :param data: dataframe object containing radio source events
    :param mysql_config: path of mysql_config file including database connection parameters
    :param output_dir: output directory path
    :param table_name: Name of sql dump file
    """

    if not os.path.exists(mysql_config):
        logging.error(f'my_sql connexion file does not exist:{mysql_config}')
        sys.exit()

    db = MysqlConnectorMoonTorus(mysql_config, output_path=output_dir)
    db.create_db_table_object_ingress_egress(table_name, engine='InnoDB')

    logging.info('Inserting records in table {} ...'.format(table_name))
    db.insert_into_table(table_name, data)
    logging.info('{} records inserted'.format(len(data)))

    # db.dump_table(table_name)

    db.close()

    logging.info('Table populated: {}'.format(table_name))


def generate_simple_ql_table(output_dir, event_eps_name, mysql_config=None,
                             table_name_query='juice_crema_5_0_intercept_sc2earth_ray_europa_torus_detailed',
                             table_name='juice_crema_5_0_intercept_sc2earth_ray_europa_torus_simple', dt=60):
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
    db.create_db_table_object_sc2Earth_intercept_moon_plasma_torus(table_name, engine='InnoDB')

    data, _ = get_sc_to_eart_ray_crossing_moon_torus_periods(
        db.get_mysql_connector(), table_name_query, event_eps_name, dt=dt)

    logging.info('Inserting records in table {} ...'.format(table_name))
    db.insert_into_table(table_name, data)
    logging.info('{} records inserted'.format(len(data)))

    db.dump_table(table_name)

    db.close()
