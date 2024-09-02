"""
Created on April, 2020

@author: Claudio Munoz Crego (ESAC)

Python module to handle Juice Segment files

"""

import os
import sys
import logging
from operator import itemgetter

import esac_juice_pyutils.commons.tds_spicey as tds_spi
import esac_juice_pyutils.commons.tds as tds


def write_csv_segment(segments, csv_file, event_id, fmt='%Y-%m-%dT%H:%M:%SZ',
                      time_representation='et', working_group='WGX'):
    """
    Write csv data file

    :param time_representation: segment period as ephemeris times (et) or datetime
    :param fmt: UTC date time format
    :param csv_file: csv segment file name path
    :param segments: dictionary of segments periods
    :return:
    """

    dir_path = os.path.dirname(csv_file)
    if not os.path.exists(dir_path):
        logging.error('Path does not exists: {}'.format(dir_path))
        sys.exit()

    csv_data = []

    for key in segments.keys():

        segment_id = event_id.format(key)

        for p in segments[key]:

            if time_representation == 'et':
                (start, end) = (tds_spi.et2utc(p[0], fmt), tds_spi.et2utc(p[1], fmt))
            elif time_representation == 'datetime':
                (start, end) = (tds.datetime2utc(p[0], fmt), tds.datetime2utc(p[1], fmt))
            else:
                logging.error('invalid representation time')
                sys.exit()

            csv_data.append([segment_id, start, end, '', working_group])

    csv_data = sorted(csv_data, key=itemgetter(1, 2))

    f = open(csv_file, 'w')

    for row in csv_data:
        line = ','.join(tuple(row)) + '\n'

        f.write(line)

    f.close()

    logging.info('New file created: {}'.format(csv_file))
