"""Normalizer for the interpretation of file name convention"""
import logging
import re
from datetime import datetime

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
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001": 'OPERATIONAL MODELS',
    }

    urls_instruments = {
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001": 'computer',
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/": 'computer',
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod": 'computer',
    }

    urls_provider = {}

    WORLD_WIDE_COVERAGE_WKT = 'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'

    urls_geometry = {
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001":
            'POLYGON((-19 56, 5 56, 5 26, -19 26, -19 56))',
    }

    urls_title = {
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001":
            'Atlantic-Iberian Biscay Irish-Ocean Physics Analysis and Forecast',
    }

    NC_H5_FILENAME_MATCHER = re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$")
    urls_entry_id = {
        "https://thredds.met.no/thredds/": re.compile(r"([^/]+)\.nc(\.dods)?$"),
        "https://opendap.jpl.nasa.gov/opendap/": NC_H5_FILENAME_MATCHER,
        "ftp://nrt.cmems-du.eu/Core/": NC_H5_FILENAME_MATCHER,
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001": NC_H5_FILENAME_MATCHER,
    }

    urls_summary = {
        'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'The operational IBI (Iberian Biscay Irish) Ocean Analysis and Forecasting'
                    ' system provides a 5-day hydrodynamic forecast including high frequency '
                    'processes of paramount importance to characterize regional scale marine '
                    'processes.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'IBI_ANALYSISFORECAST_PHY_005_001'
            }),
    }

    urls_dataset_parameters = {
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/" +
        "cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/": [
            'sea_surface_height_above_geoid',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/" +
        "cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/": [
            'sea_water_potential_temperature',
            'sea_water_salinity',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
            'sea_surface_height_above_geoid',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta',
            'sea_water_potential_temperature_at_sea_floor'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/" +
        "cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/": [
            'sea_water_potential_temperature',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
            'barotropic_eastward_sea_water_velocity',
            'barotropic_northward_sea_water_velocity',
            'sea_surface_height_above_geoid',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/" +
        "cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/": [
            'sea_water_potential_temperature',
            'sea_water_salinity',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/" +
        "cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/": [
            'sea_water_potential_temperature',
            'sea_water_salinity',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
            'sea_surface_height_above_geoid',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta',
            'sea_water_potential_temperature_at_sea_floor'
        ],
    }

    # See the docstring of find_time_coverage() to get
    # information about the dictionary structure
    urls_time = {
        'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001': [
            (
                re.compile(
                    r'/CMEMS_v5r1_IBI_PHY_NRT_PdE_(15minav|01dav|01hav(3D)?)_' +
                    utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'
                ),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(
                    r'/CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_' + utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
    }

    def find_matching_value(self, associated_dict, raw_attributes):
        """ Loop through <associated_dict> and get the matching value  """
        if 'url' in raw_attributes:
            for url in associated_dict.keys():
                if raw_attributes['url'].startswith(url):
                    attribute = associated_dict[url]
                    if callable(attribute):
                        return attribute(self, raw_attributes['url'])
                    else:
                        return attribute
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
            return [utils.get_cf_or_wkv_standard_name(cf_parameter) for cf_parameter in parameters]

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

    def get_summary(self, raw_attributes):
        """returns the suitable summary based on the url"""
        return self.find_matching_value(self.urls_summary, raw_attributes)
