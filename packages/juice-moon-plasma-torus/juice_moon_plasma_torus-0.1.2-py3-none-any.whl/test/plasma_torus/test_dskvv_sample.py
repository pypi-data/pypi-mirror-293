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

from spiceypy.utils.support_types import SpiceyError

from esac_juice_pyutils.commons.my_log import setup_logger
from juice_pylib.plasma_torus_model.io_torus import PlasmaTorus


def check_point_aligned_with_ray_vector(target_point, vect_origin, ori2target):
    """
    Check point found is aligned with spacecraft to target ray

    Note: both point and origin coordinates must be provided in the same reference frames

    :param target_point: Rectilinear coordinates xyz
    :param vect_origin: vector origin in rectilinear coordinates xyz (i.e. spacecraft)
    :return:
    """

    ori2fundarr = np.array(target_point) - np.array(vect_origin)

    vsep = (spi.vsep(ori2target, ori2fundarr))
    tang_vsep = np.tan(vsep)
    ori2target_norm = spi.vnorm(ori2fundarr)

    logging.info('sep angle = {:15.6f} deg; err target pos = {} km'.format(vsep, tang_vsep * ori2target_norm))


def found_points(spacecraft, et, dsk_frame, abrcorr, dsk_file_path):
    """
    Calculate point intersect of "target - origin" and torus

    1) get srflst id
    2) get origin and target rectilinear coordinate in dsk_frame
    3) get point intersect of "target - origin" and torus

    :param spacecraft: spacecraft spice identifier (juice)
    :param et: ephemeris time
    :param dsk_frame: dsk frame for TORUS
    :param abrcorr: aberration correction
    :param dsk_file_path: dsk file path
    :return: points
    """

    # 1) get srflst id

    handle = spi.dasopr(dsk_file_path)
    dladsc = spi.dlabfs(handle)

    dskdsc = spi.dskgd(handle, dladsc)

    # bodyid = dskdsc.center
    surfid = dskdsc.surfce
    # framid = dskdsc.frmcde
    # dtype = dskdsc.dtype
    # dclass = dskdsc.dclass

    srflst = [surfid]

    logging.info('srflst = {}'.format(srflst))

    # 2) get origin and target rectilinear coordinate in dsk_frame

    origin = spi.spkpos(spacecraft, et, dsk_frame, abrcorr, 'JUPITER')[0]

    r0, lon_0, lat_0 = spi.reclat(origin)
    lon_0 *= spi.dpr()
    lat_0 *= spi.dpr()
    logging.debug('Origin position (lon, lat, r) = ({:12.2f}, {:12.2f}, {:12.2f}) in {}'.format(
        lon_0, lat_0, r0, dsk_frame))

    ray = spi.spkpos('earth', et, dsk_frame, abrcorr, 'JUPITER')[0]
    r0, lon_0, lat_0 = spi.reclat(ray)
    lon_0 *= spi.dpr()
    lat_0 *= spi.dpr()
    logging.debug('Target position (lon, lat, r) = ({:12.2f}, {:12.2f}, {:12.2f}) in {}'.format(
        lon_0, lat_0, r0, dsk_frame))

    # 3) get point intersect of "target - origin" and torus

    ori2target = np.array(ray) - np.array(origin)

    flag = 1

    coord = []

    while flag == 1:

        xptarr, fndarr = spi.dskxv(False, 'JUICE_IO_PLASMA_TORUS', srflst, et, 'JUICE_IPT', origin, ray)

        if fndarr[0] != 0:   # [0, 0, 0]:
            r0, lon_0, lat_0 = spi.reclat(xptarr[0])
            lon_0 *= spi.dpr()
            lat_0 *= spi.dpr()
            # xyzhit = spi.latrec(r0, lon_0, lat_0)
            # d = spi.vdist(xptarr[0], xyzhit)
            logging.info('{}:|--> {} {} {} {}'.format(fndarr, xptarr[0], r0, lon_0, lat_0))
            coord.append([xptarr[0], r0, lon_0, lat_0])
            origin = xptarr[0] + ori2target / np.linalg.norm(ori2target)
            r0, lon_0, lat_0 = spi.reclat(origin)
            lon_0 *= spi.dpr()
            lat_0 *= spi.dpr()
            logging.debug('new origin: {} <=> (lon, lat, r) = ({:12.2f}, {:12.2f}, {:12.2f})'.format(
                origin, lon_0, lat_0, r0))

            # Check point found is aligned with "spacecraft to target ray"
            check_point_aligned_with_ray_vector(ray, origin, ori2target)

        flag = fndarr[0]

    return coord


if __name__ == "__main__":

    setup_logger('info')

    logging.info('start')

    # kernel_root_path = '/Users/cmunoz/Juice/JuiceKernels'

    # load dsk
    # dsk_file_path = os.path.join(dsk_file_path, 'juice_io_plasma_torus_v01.bds')
    dsk_file_path = './juice_io_plasma_torus_v04.bds'

    metakernel = "./juice_crema_3_0.tm"
    spi.furnsh(metakernel)
    spi.furnsh(dsk_file_path)

    spacecraft = 'juice'
    frame = 'JUICE_SPACECRAFT'

    target_ray = 'earth'
    observer = spacecraft
    dsk_frame = 'JUICE_IPT'
    abrcorr = 'LT+S'

    # 19-JUN-2031_01:32:00 [et=992871188.1856546]: 4 solutions!
    cuando = '19-JUN-2031 01:31:30'
    et = spi.utc2et(cuando)
    logging.info('{} --> et: {}'.format(cuando, et))
    found_points(spacecraft, et, dsk_frame, abrcorr, dsk_file_path)

    # 19-JUN-2031_01:32:00 [et=992871188.1856546]: 6 solutions!
    cuando = '19-JUN-2031 01:32:00'
    et = spi.utc2et(cuando)
    logging.info('{} --> et: {}'.format(cuando, et))
    found_points(spacecraft, et, dsk_frame, abrcorr, dsk_file_path)

    # 19-JUN-2031_01:32:00 [et=992871188.1856546]: 4 solutions!
    cuando = '19-JUN-2031 01:32:04'
    et = spi.utc2et(cuando)
    logging.info('{} --> et: {}'.format(cuando, et))
    found_points(spacecraft, et, dsk_frame, abrcorr, dsk_file_path)

    logging.info('end')
    spi.unload(dsk_file_path)



