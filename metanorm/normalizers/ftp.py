"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
from datetime import datetime

import dateutil.parser
import pythesint as pti
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc
from django.contrib.gis.geos.geometry import GEOSGeometry

from .base import BaseMetadataNormalizer


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class FTPMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for hardcoding information for the ftp-derived cases """
    metadata_name = 'ftp_domain_name'

    def match_domain(self, raw_attributes):
        """ Find the domain in raw_attributes and set "domain_name" variable.
              Return a string that determines which hardcoded values are being used
              in the following functions """
        domain_name = None
        if set([self.metadata_name]).issubset(raw_attributes.keys()):
            if raw_attributes['ftp_domain_name'] == 'ftp.remss.com':
                domain_name = 'remss'
            elif raw_attributes['ftp_domain_name'] == 'anon-ftp.ceda.ac.uk':
                domain_name = 'ceda'
            elif raw_attributes['ftp_domain_name'] == 'ftp.gportal.jaxa.jp':
                domain_name = 'jaxa'
        return domain_name


    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        platform_map = dict(ceda='Earth Observation Satellites', remss='GPM',
                            jaxa='GCOM-W1')
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        return pti.get_gcmd_platform(platform_map[domain_str])

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        instrument_map = dict(ceda='Imaging Spectrometers/Radiometers', remss='GMI',
                              jaxa='AMSR2')
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        return pti.get_gcmd_instrument(instrument_map[domain_str])

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        if self.match_domain(raw_attributes):
            if self.match_domain(raw_attributes) == 'remss':
                extracted_date = raw_attributes['ftp_add_and_file_name'].split(
                    '/')[-1].split('v')[0].split('_')[1]
                if len(extracted_date) == 6 and extracted_date.startswith('2'):
                    # adding "01" as the first day of month for the files that belong to whole month
                    extracted_date += "01"
                # 'd3d' cases are the average of three consequent days! so start day is yesterday!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in raw_attributes['ftp_add_and_file_name'].split('/')[-1]:
                    return dateutil.parser.parse(extracted_date).replace(tzinfo=tzutc())+relativedelta(days=-1)
                # for weekly average ones in the "weeks" folder
                # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in raw_attributes['ftp_add_and_file_name'].split('/'):
                    return dateutil.parser.parse(extracted_date).replace(tzinfo=tzutc())+relativedelta(days=-3)
                else:  # normal cases that are neither being 'd3d' nor inside "week"
                    return dateutil.parser.parse(extracted_date).replace(tzinfo=tzutc())

            elif self.match_domain(raw_attributes) == 'ceda':
                return dateutil.parser.parse("19820101T000000").replace(tzinfo=tzutc())+relativedelta(days=+int(raw_attributes['ftp_add_and_file_name'].split('/')[-1][1:4]))
            elif self.match_domain(raw_attributes) == 'jaxa':
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return dateutil.parser.parse(raw_attributes['ftp_add_and_file_name'].split('/')[-1].split('_')[1]).replace(tzinfo=tzutc())
        else:
            return None
    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        if self.match_domain(raw_attributes):
            if self.match_domain(raw_attributes) == 'remss':
                extracted_date = raw_attributes['ftp_add_and_file_name'].split(
                    '/')[-1].split('v')[0].split('_')[1]
                if len(extracted_date) == 6 and extracted_date.startswith('2'):
                    # adding last day of month based on the calendar
                    # as the last day of month for the files that belong to whole month
                    extracted_date += str(calendar.monthrange(
                        int(extracted_date[:4]), int(extracted_date[4:]))[1])
                # 'd3d' cases are the average of three consequent days! so end day is tomorrow!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in raw_attributes['ftp_add_and_file_name'].split('/')[-1]:
                    return dateutil.parser.parse(extracted_date).replace(tzinfo=tzutc())+relativedelta(days=+1)
                    # for weekly average ones in the "weeks" folder
                    # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in raw_attributes['ftp_add_and_file_name'].split('/'):
                    return dateutil.parser.parse(extracted_date).replace(tzinfo=tzutc())+relativedelta(days=+3)
                else:  # normal cases that are neither being 'd3d' nor inside "week"
                    return dateutil.parser.parse(extracted_date).replace(tzinfo=tzutc())

            elif self.match_domain(raw_attributes) == 'ceda':
                return dateutil.parser.parse("20100101T000000").replace(tzinfo=tzutc())+relativedelta(days=+int(raw_attributes['ftp_add_and_file_name'].split('/')[-1][1:4]))

            elif self.match_domain(raw_attributes) == 'jaxa':
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return self.get_time_coverage_start(raw_attributes)
                # return dateutil.parser.parse(raw_attributes['ftp_add_and_file_name'].split('/')[-1].split('_')[1]).replace(tzinfo=tzutc())
        else:
            return None
    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        provider_map = dict(ceda='ESA/CCI', remss='NASA/GSFC/SED/ESD/LA/GPM',
                            jaxa='JP/JAXA/EOC')
        provider_str = self.match_domain(raw_attributes)
        if provider_str is None:
            return None
        return pti.get_gcmd_provider(provider_map[provider_str])

    def get_dataset_parameters(self, raw_attributes):
        """ DANGER!!!!! return list with different parameter from wkv variable """
        dsp_map = dict(ceda=['sea_surface_temperature'],
                       jaxa=['sea_surface_temperature'],
                       remss=['wind_speed', 'atmosphere_mass_content_of_water_vapor',
                              'atmosphere_mass_content_of_cloud_liquid_water', 'rainfall_rate'],)
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return []
        else:
            return [pti.get_cf_standard_name(paramter) for paramter in dsp_map[domain_str]]

    def get_location_geometry(self, raw_attributes):
        """ DANGER!!!!! jaxa remains"""

        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        elif domain_str == 'ceda' or 'remss':
            return GEOSGeometry(('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'), srid=4326)
        else:
            return GEOSGeometry(('POLYGON((1 1, 1 2, 2 2, 2 1, 1 1))'), srid=4326)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        title_map = dict(ceda='ESA SST CCI OSTIA L4 Climatology',
                         remss="""Atmosphere parameters from Global Precipitation Measurement Microwave Imager""",
                         jaxa='AMSR2-L2 Sea Surface Temperature')
        title_str = self.match_domain(raw_attributes)
        if title_str is None:
            return None
        return title_map[title_str]
