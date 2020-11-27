"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
from datetime import datetime
from urllib.parse import urlparse

import pythesint as pti
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc

import metanorm.utils as utils
from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class URLMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for hardcoding information based on URLS """

    urls_platforms = {
        "ftp://ftp.remss.com/gmi": 'GPM',
        "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/": 'Earth Observation Satellites',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W": 'GCOM-W1',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046":
            'Earth Observation satellites',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": 'Earth Observation satellites',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": 'OPERATIONAL MODELS'
    }

    urls_instruments = {
        'ftp://ftp.remss.com/gmi': 'GMI',
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/':
            'Imaging Spectrometers/Radiometers',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046": 'altimeters',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": 'altimeters',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": 'computer'
    }

    urls_provider = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA/CCI',
        "ftp://ftp.remss.com/gmi/": 'NASA/GSFC/SED/ESD/LA/GPM',
        "ftp://ftp.gportal.jaxa.jp/standard": 'JP/JAXA/EOC',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046": 'cmems',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": 'cmems',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": 'cmems'
    }

    WORLD_WIDE_COVERAGE_WKT = 'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'
    urls_geometry = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': WORLD_WIDE_COVERAGE_WKT,
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10': WORLD_WIDE_COVERAGE_WKT,
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25': WORLD_WIDE_COVERAGE_WKT,
        "ftp://ftp.remss.com/gmi/": WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046":
            WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": WORLD_WIDE_COVERAGE_WKT,
    }

    urls_title = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1':
            'ESA SST CCI OSTIA L4 Climatology',
        "ftp://ftp.remss.com/gmi/":
            'Atmosphere parameters from Global Precipitation Measurement Microwave Imager',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/":
            'AMSR2-L2 Sea Surface Temperature',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10/":
            'AMSR2-L2 Sea Surface Temperature',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/":
            'AMSR2-L3 Sea Surface Temperature',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046":
            'GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003":
            'GLOBAL TOTAL SURFACE AND 15M CURRENT FROM ALTIMETRIC '
            'GEOSTROPHIC CURRENT AND MODELED EKMAN CURRENT PROCESSING',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024":
            'GLOBAL OCEAN 1_12 PHYSICS ANALYSIS AND FORECAST UPDATED DAILY'
    }

    NC_H5_FILENAME_MATCHER = re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$")
    urls_entry_id = {
        "https://thredds.met.no/thredds/": re.compile(r"([^/]+)\.nc(\.dods)?$"),
        "https://opendap.jpl.nasa.gov/opendap/": NC_H5_FILENAME_MATCHER,
        "ftp://ftp.remss.com/gmi": re.compile(r"([^/]+)\.gz$"),
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/":
            NC_H5_FILENAME_MATCHER,
        "ftp://nrt.cmems-du.eu/Core/": NC_H5_FILENAME_MATCHER,
        "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/":
            NC_H5_FILENAME_MATCHER
    }

    urls_dataset_parameters = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': ['sea_surface_temperature'],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST': [
            'sea_surface_temperature'
        ],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10': [
            'sea_surface_temperature'
        ],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25': [
            'sea_surface_temperature'
        ],
        "ftp://ftp.remss.com/gmi/": [
            'wind_speed',
            'atmosphere_mass_content_of_water_vapor',
            'atmosphere_mass_content_of_cloud_liquid_water',
            'rainfall_rate'
        ],
        # based on http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct&service=SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046-TDS&product=dataset-duacs-nrt-global-merged-allsat-phy-l4
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046": [
            'surface_geostrophic_eastward_sea_water_velocity',
            'surface_geostrophic_eastward_sea_water_velocity_assuming_sea_level_for_geoid',
            'surface_geostrophic_northward_sea_water_velocity',
            'surface_geostrophic_northward_sea_water_velocity_assuming_sea_level_for_geoid'
        ],
        # based on http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct&service=MULTIOBS_GLO_PHY_NRT_015_003-TDS&product=dataset-uv-nrt-daily
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": [
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ],
        # based on http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct&service=GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS&product=global-analysis-forecast-phy-001-024
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": [
            # 'sea_water_potential_temperature_at_sea_floor', # problematic for pti!! DANGER TODO
            'ocean_mixed_layer_thickness_defined_by_sigma_theta',
            'sea_ice_area_fraction',
            'sea_ice_thickness',
            'sea_water_salinity',
            'sea_water_potential_temperature',
            'eastward_sea_water_velocity',
            'eastward_sea_ice_velocity',
            'northward_sea_water_velocity',
            'northward_sea_ice_velocity',
            'sea_surface_height_above_geoid'
        ]
    }

    # See the docstring of find_time_coverage() to get
    # information about the dictionary structure
    urls_time = {
        'ftp://ftp.remss.com/gmi': [
            (
                re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+\.gz$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+_d3d\.gz$'),
                utils.create_datetime,
                lambda time: (time - relativedelta(days=2), time + relativedelta(days=1))
            ),
            (
                re.compile(r'/weeks/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+\.gz$'),
                utils.create_datetime,
                lambda time: (time - relativedelta(days=6), time + relativedelta(days=1))
            ),
            (
                re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTH_REGEX + r'v[\d.]+\.gz$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': [
            (   # model data over a year, based on observations from 1982 to 2010. TODO: confirm
                re.compile(r'/D(?P<d>\d{3})-.*\.nc$'),
                lambda d: utils.create_datetime(1982, day_of_year=d),
                lambda time: (time, datetime(2010, time.month, time.day).replace(tzinfo=tzutc()))
            )
        ],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3': [
            (
                re.compile(r'/[A-Z\d]+_' + utils.YEARMONTHDAY_REGEX + r'_\d{2}D.*\.h5$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(r'/[A-Z\d]+_' + utils.YEARMONTH_REGEX + r'00_\d{2}M.*\.h5$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
        'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/' +
        'dataset-duacs-nrt-global-merged-allsat-phy-l4': [
            (
                re.compile(r'/nrt_global_allsat_phy_l4_' + utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'),
                utils.create_datetime,
                lambda time: (time - relativedelta(hours=12), time + relativedelta(hours=12))
            )
        ],
        'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003': [
            (
                re.compile(r'/dataset-uv-nrt-(daily|hourly)_' +
                    utils.YEARMONTHDAY_REGEX + r'T.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(r'/dataset-uv-nrt-monthly_' + utils.YEARMONTH_REGEX + r'T.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            )
        ],
        'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/': [
            (
                re.compile(
                    r'/(SMOC|mercatorpsy4v3r1_gl12_(mean|hrly))_' +
                    utils.YEARMONTHDAY_REGEX +
                    r'_R.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(r'/mercatorpsy4v3r1_gl12_mean_' + utils.YEARMONTH_REGEX + r'.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
            (
                re.compile(
                    r'/mercatorpsy4v3r1_gl12_(thetao|so|uovo)_' +
                    utils.YEARMONTHDAY_REGEX +
                    r'_(?P<hour>\d{2})h_R.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time)
            ),
        ],
    }

    @staticmethod
    def find_matching_value(associated_dict, raw_attributes):
        """ Loop through <associated_dict> and get the matching value  """
        if 'url' in raw_attributes:
            for url in associated_dict.keys():
                if raw_attributes['url'].startswith(url):
                    return associated_dict[url]
        return None

    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        found_value = self.find_matching_value(self.urls_platforms, raw_attributes)
        if found_value:
            return pti.get_gcmd_platform(found_value)

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        found_value = self.find_matching_value(self.urls_instruments, raw_attributes)
        if found_value:
            return pti.get_gcmd_instrument(found_value)

    def find_time_coverage(self, raw_attributes):
        """Find the time coverage based on the 'url' raw attribute.
        Returns a 2-tuple containing the start and end time,
        or a 2-tuple containing None if no time coverage was found.

        This method uses the `urls_time` dictionary.
        This dictionary has the following structure:
        urls_time = {
            'url_prefix': [
                (
                    compiled_regex,
                    datetime_creation_function,
                    time_coverage_function
                ),
                (...)
            ],
            ...
        }
        Where:
          - "url_prefix" is the prefix matched against the 'url' raw
            attribute

          - "compiled_regex" is a compiled regular expresion used to
            extract the time information from the URL. It should
            contain named groups which will be given as arguments
            to the datetime_creation_function

          - "datetime_creation_function" is a function which creates
            a datetime object from the information extracted using
            the regex.

          - "time_coverage_function" is a function which takes the
            datetime object returned by datetime_creation_function
            and returns the time coverage as a 2-tuple
        """
        if 'url' in raw_attributes:
            time_finder = self.find_matching_value(self.urls_time, raw_attributes)
            if time_finder:
                for matcher, get_time, get_coverage in time_finder:
                    match = matcher.search(raw_attributes['url'])
                    if match:
                        file_time = get_time(**match.groupdict())
                        return (get_coverage(file_time)[0], get_coverage(file_time)[1])
        return (None, None)

    def get_time_coverage_start(self, raw_attributes):
        """Returns the start time"""
        return self.find_time_coverage(raw_attributes)[0]

    def get_time_coverage_end(self, raw_attributes):
        """Return the end time"""
        return self.find_time_coverage(raw_attributes)[1]

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        found_value = self.find_matching_value(self.urls_provider, raw_attributes)
        if found_value:
            return pti.get_gcmd_provider(found_value)

    @staticmethod
    def create_parameter_list(parameters):
        """ Convert list with standard names into list with Pythesing dicts """
        if parameters:
            return [pti.get_cf_standard_name(cf_parameter) for cf_parameter in parameters]

    def get_dataset_parameters(self, raw_attributes):
        """ return list with different parameter(s) from cf_standard_name """
        return self.create_parameter_list(self.find_matching_value(
            self.urls_dataset_parameters, raw_attributes)) or []

    def get_location_geometry(self, raw_attributes):
        """ returns the suitable location geometry based on the filename """
        return self.find_matching_value(self.urls_geometry, raw_attributes)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable entry_title based on the filename """
        return self.find_matching_value(self.urls_title, raw_attributes)

    def get_entry_id(self, raw_attributes):
        """ returns the suitable entry_id based on the filename """
        file_name = None
        if 'url' in raw_attributes:
            for url_start in self.urls_entry_id:
                if raw_attributes['url'].startswith(url_start):
                    try:
                        file_name = self.urls_entry_id[url_start].search(
                            raw_attributes['url']).group(1)
                    except AttributeError:
                        file_name = None
        return file_name
