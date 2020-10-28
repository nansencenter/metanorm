"""Normalizer for the interpretation of file name convention"""

import calendar
import logging
import re
from datetime import datetime
from urllib.parse import urlparse

import pythesint as pti
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc

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

    keys_for_geometry_dictionary = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/',
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10',
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25',
        "ftp://ftp.remss.com/gmi/",
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046",
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003",
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024"
    }

    urls_geometry = dict.fromkeys(keys_for_geometry_dictionary,
                                  ('POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'))

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

    urls_entry_id = {
        "https://thredds.met.no/thredds/": re.compile(r"([^/]+)\.nc(\.dods)?$"),
        "https://opendap.jpl.nasa.gov/opendap/": re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$"),
        "ftp://ftp.remss.com/gmi": re.compile(r"([^/]+)\.gz$"),
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/":
            re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$"),
        "ftp://nrt.cmems-du.eu/Core/": re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$"),
        "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/":
            re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$")
    }

    urls_dsp = {
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

    @staticmethod
    def find_matching_value(associated_dict, raw_attributes):
        """ Loop through <associated_dict> and get the matching value  """
        if 'url' in raw_attributes:
            for url in associated_dict.keys():
                if raw_attributes['url'].startswith(url):
                    return associated_dict[url]
        return None

    @staticmethod
    def extract_time(time_text):
        """ Extract time from file name """
        if not time_text:
            return None
        # tuple of all formats for usage of "strptime" function of datetime
        # Order of this tuple matters! so the more generic formats must be in the end of tuple
        strp_format = (
            # for ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4
            "dataset-uv-nrt-hourly_%Y%m%dT%H%MZ",
            "dataset-uv-nrt-monthly_%Y%mT%H%MZ",
            "dataset-uv-nrt-daily_%Y%m%dT%H%MZ",
            # for ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4
            "mercatorpsy4v3r1_gl12_so_%Y%m%d_%H",
            "mercatorpsy4v3r1_gl12_thetao_%Y%m%d_%H",
            "mercatorpsy4v3r1_gl12_uovo_%Y%m%d_%H",
            "SMOC_%Y%m%d",
            "mercatorpsy4v3r1_%Y%m%d",
            "mercatorpsy4v3r1_%Y%m.nc",
            # for ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4
            "nrt_global_allsat_phy_l4_%Y%m%d",  # e.x.: 'nrt_global_allsat_phy_l4_20200206'
            "mercatorpsy4v3r1_%Y%m%d",
            # for remss
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
        return relativedelta(days=calendar.monthrange(
            extracted_date.year, extracted_date.month)[1] - 1)

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

    def get_time_coverage_start(self, raw_attributes):
        """return the start time with "start" flag equals to "True" for the method."""
        return self.find_time_coverage(raw_attributes, start=True)

    def get_time_coverage_end(self, raw_attributes):
        """return the end time with "start" flag equals to "False" for the method."""
        return self.find_time_coverage(raw_attributes, start=False)

    def find_time_coverage(self, raw_attributes, start):
        """find out the time based on the filename and them some modification based on path.
        'start' is a flag that indicates whether it is a "start time usage" of function or "start
        time usage" of it.start=True is for find the "time_coverage_start". """
        if 'url' in raw_attributes:
            url_path_and_file_name = urlparse(raw_attributes['url']).path
            file_name = url_path_and_file_name.split('/')[-1]
            url_path_and_file_name_splitted = url_path_and_file_name.split('/')
            file_name_splitted = None
            if '_' in file_name:
                file_name_splitted = file_name.split('_')
            # proper splitting or modification of filename is done by this dictionary(url_time)
            # in order to be ready for sending into "self.extract_time".
            # Sometimes there is constant value needed for this calculation instead of filename
            url_time = {
                'ftp://ftp.remss.com': file_name,
                'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1':
                    "19820101" if start else "20100101",
                "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2":
                    file_name_splitted[0] + '_' +
                    file_name_splitted[1] if file_name_splitted else None,
                "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4":
                    file_name[:33],
                "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003":
                    file_name_splitted[0] + '_' +
                    file_name_splitted[1] if file_name_splitted else None,
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/":
                    file_name_splitted[0] + '_' +
                    file_name_splitted[-2] if file_name_splitted else None,
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-so/":
                    file_name[:36],
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-thetao":
                    file_name[:40],
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-uovo":
                    file_name[:38],
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-merged-uv":
                    file_name_splitted[0] + '_' +
                file_name_splitted[1] if file_name_splitted else None,
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/":
                    file_name_splitted[0] + '_' +
                    file_name_splitted[-2] if file_name_splitted else None,
                "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-monthly/":
                    file_name_splitted[0] + '_' +
                    file_name_splitted[-1] if file_name_splitted else None
            }
            extracted_date = self.extract_time(self.find_matching_value(
                url_time, raw_attributes))
            if not extracted_date:
                return None
            ########################################################################################
            # further modification of "extracted time" based on other semantics of parts of the path
            if raw_attributes['url'].startswith('ftp://ftp.remss.com'):
                # 'd3d' cases are the average of three consequent days! so start day is yesterday!
                # if condition is the search of 'd3d' in the filename
                if 'd3d' in file_name:
                    relative_days = -1 if start else 1
                    extracted_date = extracted_date + relativedelta(days=relative_days)
                # for weekly average ones in the "weeks" folder
                # if condition is the search of "weeks" folder in the FTP path
                elif "weeks" in url_path_and_file_name_splitted:
                    relative_days = -3 if start else 3
                    extracted_date = extracted_date + relativedelta(days=relative_days)
                elif re.search(r"^f35_[0-9]{6}v[0-9]\.[0-9]\.gz$", file_name):
                    # file is a month file.So,the end time must be the end of month.
                    # python "strptime" always gives the first day. So the length of month in that
                    # year is added.
                    extracted_date = extracted_date if start else \
                        extracted_date + self.length_of_month(extracted_date)
            elif raw_attributes['url'].startswith(
                    'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1'):
                # the constant date is corrected based on the few letter at the beginning of file name
                extracted_date += relativedelta(days=int(file_name[1:4]) - 1)
            elif raw_attributes['url'].startswith(
                    'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2'):
                if file_name_splitted[1].endswith('00'):  # it is a month file
                    extracted_date = extracted_date if start else \
                        extracted_date + self.length_of_month(extracted_date)
            elif raw_attributes['url'].startswith(
                    "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046"):
                extracted_date = extracted_date if start else extracted_date + relativedelta(days=1)
            elif raw_attributes['url'].startswith(
                    'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'):
                if "monthly" in file_name:
                    extracted_date = extracted_date if start else \
                        extracted_date + self.length_of_month(extracted_date)
                if "hourly" in file_name or "daily" in file_name:
                    extracted_date = extracted_date if start else \
                        extracted_date + relativedelta(days=1)
            elif raw_attributes['url'].startswith(
                    'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'):
                if any(path_part.endswith("monthly") for path_part in url_path_and_file_name_splitted):
                    extracted_date = extracted_date if start else \
                        extracted_date + self.length_of_month(extracted_date)
                elif any("3dinst" in path_part for path_part in url_path_and_file_name_splitted):
                    extracted_date = extracted_date if start else \
                        extracted_date + relativedelta(hours=6)
                else:
                    extracted_date = extracted_date if start else \
                        extracted_date + relativedelta(days=1)
            return extracted_date

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
            self.urls_dsp, raw_attributes)) or []

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
