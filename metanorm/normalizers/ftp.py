"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
from datetime import datetime

import dateutil.parser
import pythesint as pti
from dateutil.relativedelta import *
from dateutil.tz import tzutc
from django.contrib.gis.geos.geometry import GEOSGeometry

import metanorm.utils as utils

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
        if set([self.metadata_name]).issubset(raw_attributes.keys()):
            if raw_attributes['ftp_domain_name'] == 'ftp.nersc.no':
                domain_name = 'nersc'
            elif raw_attributes['ftp_domain_name'] == 'ftp.remss.com':
                domain_name = 'remss'
            elif raw_attributes['ftp_domain_name'] == 'anon-ftp.ceda.ac.uk':
                domain_name = 'ceda'
            elif raw_attributes['ftp_domain_name'] == 'ftp.gportal.jaxa.jp':
                domain_name = 'jaxa'
            return domain_name
        else:
            return None

    def get_platform(self, raw_attributes):
        """DANGER!!! returns the suitable platform based on the filename """
        platform_map = dict(ceda='dummy_platform', remss='dummy_platform2',
                            jaxa='dummy_platform3')  # DANGER! values are absolutely FAKE, must be revised
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        return utils.get_gcmd_platform(platform_map[domain_str])

    def get_instrument(self, raw_attributes):
        """DANGER!!!  returns the suitable instrument based on the filename """
        instrument_map = dict(ceda='dummy_instrument', remss='dummy_instrument2',
                              jaxa='dummy_instrument3')  # DANGER! values are absolutely FAKE, must be revised
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        return utils.get_gcmd_instrument(instrument_map[domain_str])

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        if self.match_domain(raw_attributes):
            if self.match_domain(raw_attributes) == 'nersc':
                return None
            elif self.match_domain(raw_attributes) == 'remss':
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
                return dateutil.parser.parse("19820222T000000").replace(tzinfo=tzutc())
            elif self.match_domain(raw_attributes) == 'jaxa':
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return dateutil.parser.parse(raw_attributes['ftp_add_and_file_name'].split('/')[-1].split('_')[1]).replace(tzinfo=tzutc())

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
                return dateutil.parser.parse("20100222T000000").replace(tzinfo=tzutc())
            elif self.match_domain(raw_attributes) == 'jaxa':
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return self.get_time_coverage_start(raw_attributes)
                # return dateutil.parser.parse(raw_attributes['ftp_add_and_file_name'].split('/')[-1].split('_')[1]).replace(tzinfo=tzutc())

    def get_provider(self, raw_attributes):
        """ DANGER!!!!!  returns the suitable provider based on the filename """
        provider_map = dict(ceda='dummy_provider', remss='dummy_provider2',
                            jaxa='dummy_provider3')  # DANGER! values are absolutely FAKE, must be revised
        provider_str = self.match_domain(raw_attributes)
        if provider_str is None:
            return None
        # utils.get_gcmd_provider(provider_map[provider_str])
        return utils.get_gcmd_provider(['ESA/EO'])

    def get_dataset_parameters(self, raw_attributes):
        """ DANGER!!!!! return list with different parameter from wkv variable """
        dsp_map = dict(ceda='dummy_parameter', remss='dummy_parameter2',
                       jaxa='dummy_parameter3')  # DANGER! values are absolutely FAKE, must be revised
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        elif domain_str == 'nersc':
            return [utils.get_gcmd_science_keyword(dsp_map[domain_str])]
        else:
            return []

    def get_location_geometry(self, raw_attributes):
        """ DANGER!!!!! """
        dsp_map = dict(ceda='dummy_parameter', remss='dummy_parameter2',
                       jaxa='dummy_parameter3')  # DANGER! values are absolutely FAKE, must be revised
        domain_str = self.match_domain(raw_attributes)
        if domain_str is None:
            return None
        elif domain_str == 'nersc':
            return GEOSGeometry(('POLYGON((1 1, 1 2, 2 2, 2 1, 1 1))'), srid=4326)
        else:
            return GEOSGeometry(('POLYGON((1 1, 1 2, 2 2, 2 1, 1 1))'), srid=4326)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        provider_map = dict(ceda='dummy_provider', remss='dummy_provider2',
                            jaxa='dummy_provider3')  # DANGER! values are absolutely FAKE, must be revised
        provider_str = self.match_domain(raw_attributes)
        if provider_str is None:
            return None
        return "234"  # utils.get_gcmd_provider(provider_map[provider_str])
