"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
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
    domain_set = {"anon-ftp.ceda.ac.uk", "ftp.remss.com", "ftp.gportal.jaxa.jp"}

    def match_domain(self, raw_attributes):
        """ Find the domain in raw_attributes  """
        if set(['ftp_domain_name']).issubset(raw_attributes.keys()):
            if raw_attributes['ftp_domain_name'] in self.domain_set:
                return raw_attributes['ftp_domain_name']

    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        platform_on_ftp = {"ftp://ftp.remss.com/gmi": 'GPM',
                           "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1": 'Earth Observation Satellites',
                           "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2": 'GCOM-W1'}  # jaxa
        for ftp_base_dir in platform_on_ftp.keys():
            if ftp_base_dir in 'ftp://'+raw_attributes['ftp_domain_name'].rstrip('/')+'/'+raw_attributes['ftp_add_and_file_name'].strip('/'):
                return pti.get_gcmd_platform(platform_on_ftp[ftp_base_dir])

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        instrument_on_ftp = {'ftp://ftp.remss.com/gmi': 'GMI',
                             'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
                             'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'Imaging Spectrometers/Radiometers',
                             }
        for ftp_base_dir in instrument_on_ftp.keys():
            if ftp_base_dir in 'ftp://'+raw_attributes['ftp_domain_name'].rstrip('/')+'/'+raw_attributes['ftp_add_and_file_name'].strip('/'):
                return pti.get_gcmd_instrument(instrument_on_ftp[ftp_base_dir])

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        match_result = self.match_domain(raw_attributes)
        if match_result:
            if match_result == "ftp.remss.com":
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

            elif match_result == "anon-ftp.ceda.ac.uk":
                return dateutil.parser.parse("19820101T000000").replace(tzinfo=tzutc())+relativedelta(days=+int(raw_attributes['ftp_add_and_file_name'].split('/')[-1][1:4]))
            elif match_result == "ftp.gportal.jaxa.jp":
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return dateutil.parser.parse(raw_attributes['ftp_add_and_file_name'].split('/')[-1].split('_')[1]).replace(tzinfo=tzutc())
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        match_result = self.match_domain(raw_attributes)
        if match_result:
            if match_result == "ftp.remss.com":
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

            elif match_result == "anon-ftp.ceda.ac.uk":
                return dateutil.parser.parse("20100101T000000").replace(tzinfo=tzutc())+relativedelta(days=+int(raw_attributes['ftp_add_and_file_name'].split('/')[-1][1:4]))

            elif match_result == "ftp.gportal.jaxa.jp":
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return self.get_time_coverage_start(raw_attributes)
                # return dateutil.parser.parse(raw_attributes['ftp_add_and_file_name'].split('/')[-1].split('_')[1]).replace(tzinfo=tzutc())
        else:
            return None

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        provider_map = {"anon-ftp.ceda.ac.uk": 'ESA/CCI',
                        "ftp.remss.com": 'NASA/GSFC/SED/ESD/LA/GPM',
                        "ftp.gportal.jaxa.jp": 'JP/JAXA/EOC'}
        match_result = self.match_domain(raw_attributes)
        if match_result is None:
            return match_result
        return pti.get_gcmd_provider(provider_map[raw_attributes['ftp_domain_name']])

    def get_dataset_parameters(self, raw_attributes):
        """ DANGER!!!!! return list with different parameter from wkv variable """
        dsp_on_ftp = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': ['sea_surface_temperature'],
                      'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': ['sea_surface_temperature'],
                      "ftp://ftp.remss.com/gmi/": ['wind_speed', 'atmosphere_mass_content_of_water_vapor',
                                                   'atmosphere_mass_content_of_cloud_liquid_water', 'rainfall_rate'], }
        match_result = self.match_domain(raw_attributes)
        if match_result is None:
            return []
        else:
            for ftp_base_dir in dsp_on_ftp.keys():
                if ftp_base_dir in 'ftp://'+raw_attributes['ftp_domain_name'].rstrip('/')+'/'+raw_attributes['ftp_add_and_file_name'].strip('/'):
                    return [pti.get_cf_standard_name(cf_parameter) for cf_parameter in dsp_on_ftp[ftp_base_dir]]

    def get_location_geometry(self, raw_attributes):
        """ DANGER!!!!! jaxa remains"""

        match_result = self.match_domain(raw_attributes)
        if match_result is None:
            return None
        elif match_result == "anon-ftp.ceda.ac.uk" or "ftp.remss.com":
            return GEOSGeometry(('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'), srid=4326)
        else:
            return GEOSGeometry(('POLYGON((1 1, 1 2, 2 2, 2 1, 1 1))'), srid=4326)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        title_map = {"anon-ftp.ceda.ac.uk": 'ESA SST CCI OSTIA L4 Climatology',
                     "ftp.remss.com": 'Atmosphere parameters from Global Precipitation Measurement Microwave Imager',
                     "ftp.gportal.jaxa.jp": 'AMSR2-L2 Sea Surface Temperature'}
        title_str = self.match_domain(raw_attributes)
        if title_str is None:
            return None
        return title_map[title_str]
