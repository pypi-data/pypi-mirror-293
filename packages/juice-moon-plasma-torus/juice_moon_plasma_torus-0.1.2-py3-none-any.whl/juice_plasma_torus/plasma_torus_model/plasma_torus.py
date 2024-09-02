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
import tabulate

import esac_juice_pyutils.commons.tds_spicey as tds_spicey
import esac_juice_pyutils.gti.gti_handler as gti_handler
from esac_juice_pyutils.spiceypi import spice_kernel_utils

from juice_plasma_torus.plasma_torus_model.gs_elevation import GsElevation
from juice_plasma_torus.plasma_torus_model.gs_occult import get_non_occulted_periods


class PlasmaTorus(object):

    def __init__(self, config):

        self.config = config

        self.output_dir = config['output_path']

        self.load_spice_kernels(config['kernel'])
        self.srflst = self.get_surface_id_from_dsk(dsk_file_path=self.config['dsk'][0])
        self.torus_target_id = self.config['torus_target_id']

        self.start = spi.utc2et(self.config['start_time_utc'])
        self.end = spi.utc2et(self.config['end_time_utc'])

        self.malargues_vis, self.malargues_pass = [], []

    def get_surface_id_from_dsk(self, dsk_file_path):
        """
        Get surface id from dsk (Plasma Torus) file
        :param dsk_file_path: dsk file path
        :return:
        """

        handle = spi.dasopr(dsk_file_path)
        dladsc = spi.dlabfs(handle)

        dskdsc = spi.dskgd(handle, dladsc)

        surfid = dskdsc.surfce

        srflst = [surfid]

        # logging.debug('srflst = {}'.format(srflst))

        return srflst

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
            logging.warning('sep angle = {:15.6f} deg; err target pos = {} km'.format(vsep, tang_vsep * ori2target_norm))

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

    # def check_delta_latitude(self, et, lon, lat, prev_et, prev_lat, prev_lon, interval):
    #     """
    #     Check if trajectory is south <-> North: Current condition is delta(latitude) > 1/2 * delta(longnitude)
    #
    #     :param et: ephemeris time
    #     :param lon: point intercept longitude
    #     :param lat: point intercept latitude
    #     :param prev_et: previous (t[i-1]) ephemeris time
    #     :param prev_lat: previous (t[i-1]) point intercept latitude
    #     :param prev_lon: previous (t[i-1]) point intercept longitude
    #     :param interval: number of seconds between 2 consecutive et (et[i] - et[i-1])
    #     :return: is_s_n
    #     """
    #
    #     s_n = np.abs(lon - prev_lon) < 2 * np.abs(lat - prev_lat)
    #     dt = (et - prev_et < interval * 1.05)
    #
    #     if s_n and dt:
    #         is_s_n = 1
    #     else:
    #         is_s_n = 0
    #
    #     return is_s_n

    def generate_segment_file(self, nb_intercept, tt, intercept, interval, event_id):
        """
        Generate segment file if requested within configuration file

        :param nb_intercept: nb_of intercept
        :param tt: ephemeris times
        :param intercept: intercept values
        :param interval: delta time between 2 ephemeris time of tt
        :param event_id: id of the event/segment
        """

        if 'generate_segments' in list(self.config.keys()):

            if not self.config['generate_segments']:

                logging.info('Segment files generation not requested!')

            else:

                logging.info('Generating segment files ...')

                if nb_intercept > 0:

                    gti = gti_handler.mask2gti(tt, intercept, True)

                    for i in range(len(gti)):
                        p = gti[i]
                        (s, e) = (tds_spicey.et2utc(p[0]), tds_spicey.et2utc(p[1]))

                        print('{}: [{} - {}]'.format(i, s, e))

                    ogti = gti_handler.gti_trim(gti, max_gap=interval * 1.05, min_gti=interval)

                    for i in range(len(gti)):
                        p = gti[i]
                        (s, e) = (tds_spicey.et2utc(p[0]), tds_spicey.et2utc(p[1]))

                        print('{}: [{} - {}]'.format(i, s, e))

                    # Write segment file
                    from juice_plasma_torus.commons.segment_handler import write_csv_segment

                    segment_id = self.config['segment_id']
                    csv_file = os.path.join(self.output_dir, segment_id + '.csv')
                    segments = {event_id: ogti}

                    write_csv_segment(segments, csv_file, event_id, working_group='WG3')

        else:

            logging.info('generate_segments not defined!')

    def get_non_occulted_periods(self):
        """
        Get the periods when the observer (i.e juice) cannot see the earth

        :return: non_occulted_periods, list of non occulted periods [[start,end],...]
        """

        config = self.config['earth_not_occulted']

        non_occulted_periods = get_non_occulted_periods(self.start, self.end, config)

        for [s, e] in non_occulted_periods:
            logging.debug('non_occulted periods: {} - {} '.format(tds_spicey.et2utc(s), tds_spicey.et2utc(e)))

        return non_occulted_periods

    def get_malargue_passes(self, gti):
        """
        Get Malargue GS visibilty and passes

        :return: malargue_visibility, malargue_pass
        """

        # if gti is None:
        #     gti = [[self.start, self.end]]

        body = self.config['malargue_vis']['body']  # Juice
        gs_station = self.config['malargue_vis']['station']  # Malargue
        elevation = self.config['malargue_vis']['elevation']  # 10 deg
        interval = self.config['malargue_vis']['interval']  # 600 seconds usually used by global finder

        malargue_visibility = GsElevation()(gti, body, gs_station, elevation, interval)

        pass_start_shift = self.config['malargue_pass']['start']  # 0
        pass_duration = self.config['malargue_pass']['duration']  # 8 hours in seconds

        malargue_pass = []
        for s, e in malargue_visibility:

            pass_start = s + pass_start_shift
            if pass_start + pass_duration < e:
                pass_end = pass_start + pass_duration
            else:
                pass_end = e

            malargue_pass.append([pass_start, pass_end])

        return malargue_visibility, malargue_pass

    def is_sc_visible_from_gs(self, et):
        """
        check is GS visible for a given ephemeris time (et) or list of et

        :param et: list of ephemeris time
        :return: is_vis, is_pass, flags for ground station visibility and ground station pass
        """

        is_vis = False

        for [s, e] in self.malargues_vis:
            if et < s:
                continue
            elif et > e:
                continue
            else:
                is_vis = True

        is_pass = False

        for [s, e] in self.malargues_pass:
            if et < s:
                continue
            elif et > e:
                continue
            else:
                is_pass = True

        return is_vis, is_pass

    def is_visible_from_gs(self, et):
        """
        check is GS visible for a given ephemeris time (et) or list of et

        :param et: list of ephemeris time
        :return: is_vis, is_pass, list of flags for ground station visibility and  ground station pass
        """

        n = len(et)

        is_vis = np.full(n, 0)
        # is_vis_index = gti_handler.gti_where_extended(et, self.malargues_vis)[2]
        is_vis_index = []
        for i in range(len(et)):
            for s, e in self.malargues_vis:
                if et[i] < s:
                    continue
                elif et[i] > e:
                    break
                else:  # s <= et[i] <= e:
                    is_vis_index.append(i)
        is_vis[is_vis_index] = 1

        is_pass = np.full(n, 0)
        # is_pass_index = gti_handler.gti_where_extended(et, self.malargues_pass)[2]
        is_pass_index = []
        for i in range(len(et)):
            for s, e in self.malargues_pass:
                if et[i] < s:
                    continue
                elif et[i] > e:
                    break
                else:  # s <= et[i] <= e:
                    is_pass_index.append(i)
        is_pass[is_pass_index] = 1

        return is_vis, is_pass

    def print_kernel_info(self):
        """
        Include the list of kernel loaded and PTRM file in report
        """

        kernel_info = self.__get_kernel_loaded_info__()
        for ele in kernel_info[1:]:
            logging.debug('\t{:^6}:{}'.format(ele[1], ele[0]))

    def __get_kernel_loaded_info__(self):
        """
        Returns the current list of kernel loaded in spice
        """

        kernel_info = []
        kcount = spi.ktotal('All')
        kernel_info.append(kcount)
        for i in range(kcount):
            kernel_info.append(spi.kdata(i, 'All', 256, 256, 256))

        return kernel_info

    def load_spice_kernels(self, kernel):
        """
        Load spice kernels,

        1) first the metakernel one (by the way we temporally goto metakernel directory to allows relative path)
        2) We load specific dsk file (i.e. TORUS)
        """

        config = self.config
        if not os.path.exists(kernel['meta_kernel']):
            logging.error('file does not exist: {}'.format(kernel['meta_kernel']))
            sys.exit()

        meta_kernel = spice_kernel_utils.get_copy_spice_metakernel_dico(kernel)
        spi.furnsh(meta_kernel)

        for i in range(len(config['dsk'])):
            f = config['dsk'][i]
            if os.path.isfile(f):
                spi.furnsh(f)
            else:
                file_path = os.path.join(kernel['local_root_dir'], 'dsk', f)
                spi.furnsh(file_path)
                config['dsk'][i] = file_path

    def spice_clear(self):

        # spi.dskcls()
        # Clean up the kernels
        spi.kclear()


def print_df_as_tab(df, showindex=False):
    """
    Print a given df as a Table

    :param showindex: Flag allowing to show table index
    :param df: data frame
    """
    my_tab = tabulate(df, headers='keys', tablefmt='grid', numalign='center',
                      stralign='center',
                      showindex=showindex)

    print('\n' + my_tab + '\n')