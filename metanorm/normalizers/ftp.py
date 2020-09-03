"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
import pythesint as pti
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc
from django.contrib.gis.geos.geometry import GEOSGeometry
from urllib.parse import urlparse
from .base import BaseMetadataNormalizer
from datetime import datetime


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class URLMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for hardcoding information based on URLS """

    def find_matching_value(self, associated_dict, raw_attributes_url, url_function):
        """ Loop through <associated_dict> and get the matching value using appropriate function """
        for url in associated_dict.keys():
            if raw_attributes_url.startswith(url):
                return url_function(associated_dict[url])
        return None

    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        if 'url' in raw_attributes:
            urls_platforms = {
                "ftp://ftp.remss.com/gmi": 'GPM',
                "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/": 'Earth Observation Satellites',
                "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W": 'GCOM-W1'}
            return self.find_matching_value(urls_platforms, raw_attributes['url'], pti.get_gcmd_platform)

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        if 'url' in raw_attributes:
            urls_instruments = {
                'ftp://ftp.remss.com/gmi': 'GMI',
                'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/':
                'Imaging Spectrometers/Radiometers',
            }
            return self.find_matching_value(urls_instruments, raw_attributes['url'], pti.get_gcmd_instrument)

    def time_extractor(self, time_text):
        """ time_extractor is a helper function. It extractors the time from file name """
        # tuple of all formats for usage of "strptime" function of datetime
        strp_format = ("f35_%Y%m%dv8.2_d3d.gz",
                       "f35_%Y%m%dv8.2.gz",
                       "f35_%Y%mv8.2.gz",
                       "%Y%m%d",
                       "%Y%m%d%H%M",)
        for _format in strp_format:
            try:
                extracted_date = datetime.strptime(time_text, _format).replace(tzinfo=tzutc())
            except ValueError:
                continue  # if the format is incorrect, then try another format for "strptime"
            else:
                return extracted_date

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        if 'url' in raw_attributes:
            url_path_and_file_name = urlparse(raw_attributes['url']).path
            file_name = url_path_and_file_name.split('/')[-1]
            #proper splitting or modification of filename is done by this dictionary(url_time_start)
            # in order to be ready for sending into "self.time_extractor".
            # Sometimes there is constant value needed for this calculation instead of filename
            url_time_start = {
                'ftp://ftp.remss.com': file_name,
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': "19820101",
                # or "_")
                "ftp://ftp.gportal.jaxa.jp": file_name.split('_')[1] if '_' in file_name else None
            }
            extracted_date = self.find_matching_value(
                url_time_start, raw_attributes['url'], self.time_extractor)
            # further modification of "extracted time" based on other semantics of parts of the path
            if raw_attributes['url'].startswith('ftp://ftp.remss.com'):
                # 'd3d' cases are the average of three consequent days! so start day is yesterday!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in file_name:
                    extracted_date = extracted_date+relativedelta(days=-1)
                # for weekly average ones in the "weeks" folder
                # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in url_path_and_file_name.split('/'):
                    extracted_date = extracted_date+relativedelta(days=-3)
                return extracted_date
            elif raw_attributes['url'].startswith('ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1'):
                # the constant date is correct based on the few letter at the beginning of file name
                return extracted_date+relativedelta(days=+int(file_name[1:4]))
            return extracted_date

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        if 'url' in raw_attributes:
            url_path_and_file_name = urlparse(raw_attributes['url']).path
            file_name = url_path_and_file_name.split('/')[-1]
            #proper splitting or modification of filename is done by this dictionary(url_time_start)
            # in order to be ready for sending into "self.time_extractor".
            # Sometimes there is constant value needed for this calculation instead of filename
            url_time_end = {
                'ftp://ftp.remss.com': file_name,
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': "20100101",
                "ftp://ftp.gportal.jaxa.jp": file_name.split('_')[1] if '_' in file_name else None,
            }
            extracted_date = self.find_matching_value(
                url_time_end, raw_attributes['url'], self.time_extractor)
            # further modification of "extracted time" based on other semantics of parts of the path
            if raw_attributes['url'].startswith('ftp://ftp.remss.com'):
                # 'd3d' cases are the average of three consequent days!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in file_name:
                    # end time is one day after start day
                    return extracted_date+relativedelta(days=+1)
                # for weekly average ones in the "weeks" folder
                # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in url_path_and_file_name.split('/'):
                    # end time is three days after start day
                    return extracted_date+relativedelta(days=+3)
                elif re.search("^f35_......v8\.2\.gz$", file_name):
                    # file is a month file.So,the end time must be the end of month.
                    # python "strptime" always gives the first day. SO the length of month in that
                    # year is added
                    return extracted_date + relativedelta(
                        days=calendar.monthrange(extracted_date.year, extracted_date.month)[1]-1)
            elif raw_attributes['url'].startswith('ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1'):
                # the constant date is correct based on the few letter at the beginning of file name
                return extracted_date+relativedelta(days=+int(file_name[1:4]))
            return extracted_date

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if 'url' in raw_attributes:
            urls_provider = {
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA/CCI',
                "ftp://ftp.remss.com/gmi/": 'NASA/GSFC/SED/ESD/LA/GPM',
                "ftp://ftp.gportal.jaxa.jp/standard": 'JP/JAXA/EOC'}
            return self.find_matching_value(urls_provider, raw_attributes['url'], pti.get_gcmd_provider)

    def get_dataset_parameters(self, raw_attributes):
        """ DANGER!!!!! return list with different parameter from wkv variable """
        if 'url' in raw_attributes:
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
            for url in urls_dsp.keys():
                if raw_attributes['url'].startswith(url):
                    return [pti.get_cf_standard_name(cf_parameter) for cf_parameter in urls_dsp[url]]
        return []

    def get_location_geometry(self, raw_attributes):
        """ DANGER!!!!! jaxa remains(others must be checked!)"""
        if 'url' in raw_attributes:
            urls_geometry = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/':
                             ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'),
                             'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10':
                                 ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'),
                             'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25':
                                 ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'),
                             "ftp://ftp.remss.com/gmi/":
                             ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')}
            return self.find_matching_value(urls_geometry, raw_attributes['url'], GEOSGeometry)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if 'url' in raw_attributes:
            urls_title = {
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA SST CCI OSTIA L4 Climatology',
                "ftp://ftp.remss.com/gmi/": 'Atmosphere parameters from Global Precipitation Measurement Microwave Imager',
                "ftp://ftp.gportal.jaxa.jp/standard": 'AMSR2-L2 Sea Surface Temperature'}
            return self.find_matching_value(urls_title, raw_attributes['url'], str)
