"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
from datetime import datetime
from urllib.parse import urlparse

import pythesint as pti
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc
from django.contrib.gis.geos.geometry import GEOSGeometry

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class URLMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for hardcoding information based on URLS """
    urls_platforms = {
        "ftp://ftp.remss.com/gmi": 'GPM',
        "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/": 'Earth Observation Satellites',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W": 'GCOM-W1'}

    urls_instruments = {
        'ftp://ftp.remss.com/gmi': 'GMI',
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/':
        'Imaging Spectrometers/Radiometers', }

    urls_provider = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA/CCI',
        "ftp://ftp.remss.com/gmi/": 'NASA/GSFC/SED/ESD/LA/GPM',
        "ftp://ftp.gportal.jaxa.jp/standard": 'JP/JAXA/EOC'}

    urls_geometry = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/':
                     ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'),
                     'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10':
                     ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'),
                     'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25':
                     ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'),
                     "ftp://ftp.remss.com/gmi/":
                     ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')}

    urls_title = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA SST CCI OSTIA L4 Climatology',
        "ftp://ftp.remss.com/gmi/": 'Atmosphere parameters from Global Precipitation Measurement Microwave Imager',
        "ftp://ftp.gportal.jaxa.jp/standard": 'AMSR2-L2 Sea Surface Temperature'}

    urls_dsp = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': ['sea_surface_temperature'],
                'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST':
                ['sea_surface_temperature'],
                'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10':
                ['sea_surface_temperature'],
                'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25':
                ['sea_surface_temperature'],
                "ftp://ftp.remss.com/gmi/":
                ['wind_speed', 'atmosphere_mass_content_of_water_vapor',
                 'atmosphere_mass_content_of_cloud_liquid_water', 'rainfall_rate'], }

    @staticmethod
    def find_matching_value(associated_dict, raw_attributes, desired_function):
        """ Loop through <associated_dict> and get the matching value using appropriate function """
        if 'url' in raw_attributes:
            for url in associated_dict.keys():
                if raw_attributes['url'].startswith(url):
                    return desired_function(associated_dict[url])
        return None

    @staticmethod
    def extract_time(time_text):
        """ Extract time from file name """
        # tuple of all formats for usage of "strptime" function of datetime
        # Order of this tuple matters! so the more generic formats must be in the end of tuple
        strp_format = (
            "f35_%Y%m%dv8.2_d3d.gz",
            "f35_%Y%m%dv8.2.gz",
            "f35_%Y%mv8.2.gz",
            # for normal daily files of jaxa GCOM-W.AMSR2 folder
            "GW1AM2_%Y%m%d",
            # for month files of jaxa GCOM-W.AMSR2 (MUST below the one for daily files)
            "GW1AM2_%Y%m%H",
            "%Y%m%d%H%M",
            "%Y%m%d",
        )
        for _format in strp_format:
            try:
                extracted_date = datetime.strptime(time_text, _format).replace(tzinfo=tzutc())
            except ValueError:
                continue  # if the format is incorrect, then try another format for "strptime"
            else:
                return extracted_date

    @staticmethod
    def length_of_month(extracted_date):
        """ length of the month that 'extracted_date' has been found in it """
        return relativedelta(days=calendar.monthrange(extracted_date.year, extracted_date.month)[1]-1)

    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        return self.find_matching_value(self.urls_platforms, raw_attributes, pti.get_gcmd_platform)

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        return self.find_matching_value(self.urls_instruments, raw_attributes, pti.get_gcmd_instrument)

    def get_time_coverage_start(self, raw_attributes):
        return self.find_time_coverage(raw_attributes, start=True)

    def get_time_coverage_end(self, raw_attributes):
        return self.find_time_coverage(raw_attributes, start=False)

    @staticmethod
    def find_time_coverage(raw_attributes, start):
        if 'url' in raw_attributes:
            url_path_and_file_name = urlparse(raw_attributes['url']).path
            file_name = url_path_and_file_name.split('/')[-1]
            # proper splitting or modification of filename is done by this dictionary(url_time_start)
            # in order to be ready for sending into "self.extract_time".
            # Sometimes there is constant value needed for this calculation instead of filename
            url_time_ = {
                'ftp://ftp.remss.com': file_name,
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': "19820101" if start else "20100101",
                "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2":
                file_name.split('_')[0]+'_'+file_name.split('_')[1] if '_' in file_name else None
            }
            extracted_date = URLMetadataNormalizer.find_matching_value(
                url_time_, raw_attributes, URLMetadataNormalizer.extract_time)
            if not extracted_date:
                return None
            ########################################################################################
            # further modification of "extracted time" based on other semantics of parts of the path
            if raw_attributes['url'].startswith('ftp://ftp.remss.com'):
                # 'd3d' cases are the average of three consequent days! so start day is yesterday!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in file_name:
                    d = -1 if start else 1
                    extracted_date = extracted_date+relativedelta(days=d)
                # for weekly average ones in the "weeks" folder
                # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in url_path_and_file_name.split('/'):
                    d = -3 if start else 3
                    extracted_date = extracted_date+relativedelta(days=d)
                elif re.search("^f35_......v8\.2\.gz$", file_name):
                    # file is a month file.So,the end time must be the end of month.
                    # python "strptime" always gives the first day. So the length of month in that
                    # year is added.
                    extracted_date = extracted_date if start else \
                            extracted_date + URLMetadataNormalizer.length_of_month(extracted_date)
            elif raw_attributes['url'].startswith('ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1'):
                # the constant date is corrected based on the few letter at the beginning of file name
                return extracted_date+relativedelta(days=+int(file_name[1:4]))
            elif raw_attributes['url'].startswith('ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2'):
                if file_name.split('_')[1].endswith('00'):  # it is a month file
                    extracted_date = extracted_date if start else \
                            extracted_date + URLMetadataNormalizer.length_of_month(extracted_date)
            return extracted_date

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        return self.find_matching_value(self.urls_provider, raw_attributes, pti.get_gcmd_provider)

    @staticmethod
    def create_parameter_list(parameters):
        """ Convert list with standard names into list with Pythesing dicts """
        return [pti.get_cf_standard_name(cf_parameter) for cf_parameter in parameters]

    def get_dataset_parameters(self, raw_attributes):
        """ return list with different parameter(s) from cf_standard_name """
        return self.find_matching_value(self.urls_dsp, raw_attributes, self.create_parameter_list) or []

    def get_location_geometry(self, raw_attributes):
        """ returns the suitable location geometry based on the filename """
        return self.find_matching_value(self.urls_geometry, raw_attributes, GEOSGeometry)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        return self.find_matching_value(self.urls_title, raw_attributes, str)
