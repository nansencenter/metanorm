"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
import dateutil.parser
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

    def get_matching_value(self, associated_dict, raw_attributes, url_function):
        """ Loop through <associated_dict> and get matching value using appropriate function """
        if 'url ' in raw_attributes:
            for url in associated_dict.keys():
                if raw_attributes['url'].startswith(url):
                    return url_function(associated_dict[url])
    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
            urls_platforms = {
            "ftp://ftp.remss.com/gmi": 'GPM',
            "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1":
            'Earth Observation Satellites',
            "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W": 'GCOM-W1'}
            return self.looper(urls_platforms, raw_attributes['url'], "get_gcmd_platform")

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        if 'url' in raw_attributes:
            urls_instruments = {
                'ftp://ftp.remss.com/gmi': 'GMI',
                'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1':
                'Imaging Spectrometers/Radiometers',
            }
            return self.looper(urls_instruments, raw_attributes['url'], "get_gcmd_instrument")

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        if 'url' in raw_attributes:
            ftp_add_and_file_name = urlparse(raw_attributes['url']).path
            file_name = ftp_add_and_file_name.split('/')[-1]
            # tuple of all formats for usage of "strptime" function of datetime
            strp_format = ("f35_%Y%m%dv8.2_d3d.gz", "f35_%Y%m%dv8.2.gz", "f35_%Y%mv8.2.gz")
            if raw_attributes['url'].startswith('ftp://ftp.remss.com'):
                for _format in strp_format:
                    try:
                        extracted_date = datetime.strptime(file_name, _format).replace(tzinfo=tzutc())
                    except ValueError:
                        continue
                    else:
                        # 'd3d' cases are the average of three consequent days! so start day is yesterday!
                        # if condition is the search of 'd3d' in the filename
                        if 'd3d' in file_name:
                            extracted_date = extracted_date+relativedelta(days=-1)
                        # for weekly average ones in the "weeks" folder
                        # if condition is the search of "weeks" folder in the FTP path
                        elif "weeks" in ftp_add_and_file_name.split('/'):
                            extracted_date = extracted_date+relativedelta(days=-3)
                        return extracted_date
            elif raw_attributes['url'].startswith('ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1'):
                return dateutil.parser.parse("19820101T000000").replace(tzinfo=tzutc())\
                    + relativedelta(days=+int(file_name[1:4]))
            elif raw_attributes['url'].startswith("ftp://ftp.gportal.jaxa.jp"):
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return dateutil.parser.parse(file_name.split('_')[1]).replace(tzinfo=tzutc())

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        if 'url' in raw_attributes:
            ftp_add_and_file_name = urlparse(raw_attributes['url']).path
            file_name = ftp_add_and_file_name.split('/')[-1]
            if raw_attributes['url'].startswith('ftp://ftp.remss.com'):
                starting_date = self.get_time_coverage_start(raw_attributes)
                # 'd3d' cases are the average of three consequent days!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in file_name:
                    return starting_date+relativedelta(days=+2)  # end time is two days after start day
                # for weekly average ones in the "weeks" folder
                # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in ftp_add_and_file_name.split('/'):
                    return starting_date+relativedelta(days=+6)  # end time is six days after start day
                elif file_name[10] == 'v':  # file is a month file.So,the end time must be  end of month
                    return starting_date + relativedelta(
                        days=calendar.monthrange(starting_date.year, starting_date.month)[1]-1)
                else:
                    return starting_date
            elif raw_attributes['url'].startswith('ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1'):
                return dateutil.parser.parse("20100101T000000").replace(tzinfo=tzutc())\
                    + relativedelta(days=+int(file_name[1:4]))
            elif raw_attributes['url'].startswith("ftp://ftp.gportal.jaxa.jp"):
                # time portion of the filename is extracted and then parsed with "dateutil.parser.parse"
                return self.get_time_coverage_start(raw_attributes)

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if 'url' in raw_attributes:
            urls_provider = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA/CCI',
                             "ftp://ftp.remss.com/gmi/": 'NASA/GSFC/SED/ESD/LA/GPM',
                             "ftp://ftp.gportal.jaxa.jp/standard": 'JP/JAXA/EOC'}
            return self.looper(urls_provider, raw_attributes['url'], "get_gcmd_provider")

    def get_dataset_parameters(self, raw_attributes):
        """ DANGER!!!!! return list with different parameter from wkv variable """
        if 'url' in raw_attributes:
            urls_dsp = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': ['sea_surface_temperature'],
                        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST': ['sea_surface_temperature'],
                        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10': ['sea_surface_temperature'],
                        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25': ['sea_surface_temperature'],
                        "ftp://ftp.remss.com/gmi/": ['wind_speed', 'atmosphere_mass_content_of_water_vapor',
                                                     'atmosphere_mass_content_of_cloud_liquid_water', 'rainfall_rate'], }
            for url in urls_dsp.keys():
                if raw_attributes['url'].startswith(url):
                    return [pti.get_cf_standard_name(cf_parameter) for cf_parameter in urls_dsp[url]]
        return []

    def get_location_geometry(self, raw_attributes):
        """ DANGER!!!!! jaxa remains(others must be checked!)"""
        if 'url' in raw_attributes:
            urls_geometry = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': GEOSGeometry(('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'), srid=4326),
                             'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10': GEOSGeometry(('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'), srid=4326),
                             'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25': GEOSGeometry(('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'), srid=4326),
                             "ftp://ftp.remss.com/gmi/": GEOSGeometry(('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'), srid=4326)}
            return self.get_matching_value(urls_geometry, raw_attributes, GEOSGeometry)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if 'url' in raw_attributes:
            title_map = {'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA SST CCI OSTIA L4 Climatology',
                         "ftp://ftp.remss.com/gmi/": 'Atmosphere parameters from Global Precipitation Measurement Microwave Imager',
                         "ftp://ftp.gportal.jaxa.jp/standard": 'AMSR2-L2 Sea Surface Temperature'}
            return self.get_matching_value(urls_geometry, raw_attributes, str)
