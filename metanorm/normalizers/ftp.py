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
    # Since the addressing is different in the various ftp resources, below dictionary is used
    # to find the correct part of the path based on each ftp addressing criteria.
    # This dictionary contains all the folder names regardless of their hierarchy
    # in the very fto source. A regext with "compile" and "findall" is used to find the proper name
    # form it.
    domain_map = {"anon-ftp.ceda.ac.uk": re.compile(r"""esacci|aerosol|biomass|cloud|fire|ghg|
                  glaciers|ice_sheets_antarctica|ice_sheets_greenland|lakes|land_cover|ocean_colour|
                  ozone|permafrost|sea_ice|sea_level|sea_state|sea_surface_salinity|snow|
                  soil_moisture|sst""", re.VERBOSE),
                  "ftp.remss.com": re.compile(r"""amsr2|amsre|amsrj|ascat|ccmp|gmi|msu|nscat|qscat|
                  seawinds|smap|ssmi|sst|support|TC-winds|tc_wakes|tmi|vapor|water_cycle|
                  web\.config|welcome\.txt|wind|windsat""", re.VERBOSE),
                  "ftp.gportal.jaxa.jp": re.compile(r"""JERS-1|ADEOS-2|MOS-1b|SLATS|CIRC|MOS-1|AQUA|
                  GCOM-C|GCOM-W|GSMaP|ADEOS|GPM|GPMConstellation|TRMM|TRMM_GPMFormat|GCOM-W\.AMSR2|
                  L3\.PRC_10|L3\.SIC_10|L2\.TPW|L3\.TPW_25|L3\.CLW_10|L3\.SSW_10|L3\.TB36GHz_25|
                  L3\.TB6GHz_10|L2\.SIC|L3\.TB89GHz_25|L2\.SSW|L3\.TB36GHz_10|L2\.PRC|L3\.SND_25|
                  L3\.SMC_10|L3\.TB23GHz_10|L2\.SMC|L3\.TB6GHz_25|L3\.CLW_25|L3\.TB7GHz_10|L1B|
                  L3\.SSW_25|L2\.CLW|L3\.SMC_25|L3\.SND_10|L3\.SST_25|L3\.PRC_25|L3\.TB10GHz_10|
                  L3\.TB7GHz_25|L2\.SST|L3\.SIC_25|L3\.TB18GHz_10|L3\.SST_10|L3\.TB89GHz_10|L1R|
                  L3\.TB23GHz_25|L3\.TB18GHz_25|L3\.TPW_10|L2\.SND|L3\.TB10GHz_25""", re.VERBOSE)}

    def match_domain(self, raw_attributes):
        """ Find the domain in raw_attributes and set "domain_name" variable.
              Return a string that determines which hardcoded values are being used
              in the following functions """
        metadata_name = 'ftp_domain_name'
        if set([metadata_name]).issubset(raw_attributes.keys()):
            if raw_attributes['ftp_domain_name'] in self.domain_map.keys():
                return raw_attributes['ftp_domain_name']

    def dictionary_key_finder(self, raw_attributes, associated_dictionary):
        """
        Find the correct part from the string of 'folder and file name' that are present in the
        associated_dictionary. The associated_dictionary varies based on different "get_" functions.
        """
        pattern = self.domain_map[raw_attributes['ftp_domain_name']]  # , re.VERBOSE)
        return [x for x in pattern.findall(str(raw_attributes['ftp_add_and_file_name'].split('/'))) if x in associated_dictionary.keys()][0]

    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        dict_for_get_gcmd_platform = {"esacci": 'Earth Observation Satellites',  # ceda
                                      "gmi": 'GPM',  # remss
                                      "GCOM-W": 'GCOM-W1'}  # jaxa
        match_result = self.match_domain(raw_attributes)
        if match_result is None:
            return match_result
        dictionary_key = self.dictionary_key_finder(raw_attributes, dict_for_get_gcmd_platform)
        return pti.get_gcmd_platform(dict_for_get_gcmd_platform[dictionary_key])

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        # dict_for_get_gcmd_instrument = {"esacci": 'Imaging Spectrometers/Radiometers',  # ceda
        #                                "gmi": 'GMI',  # remss
        #                                "GCOM-W": 'AMSR2'}  # jaxa
        #match_result = self.match_domain(raw_attributes)
        # if match_result is None:
        #    return match_result
        #dictionary_key = self.dictionary_key_finder(raw_attributes, dict_for_get_gcmd_instrument)
        # return pti.get_gcmd_instrument(dict_for_get_gcmd_instrument[dictionary_key])
        instrument_on_ftp = {
            'ftp://ftp.remss.com/gmi/': 'gmi',
            'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
            'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1':'Imaging Spectrometers/Radiometers'
        }
        for ftp_base_dir in instrument_on_ftp.keys():
            if ftp_base_dir in 'ftp://'+raw_attributes['ftp_domain_name'].rstrip('/')+'/'+raw_attributes['ftp_add_and_file_name'].lstrip('/'):
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
        dict_for_get_cf_standard_name = {"sst": ['sea_surface_temperature'],
                                         "L2.SST": ['sea_surface_temperature'],
                                         "gmi": ['wind_speed', 'atmosphere_mass_content_of_water_vapor',
                                                 'atmosphere_mass_content_of_cloud_liquid_water', 'rainfall_rate'], }
        match_result = self.match_domain(raw_attributes)
        if match_result is None:
            return []
        else:
            dictionary_key = self.dictionary_key_finder(
                raw_attributes,  dict_for_get_cf_standard_name)
            return [pti.get_cf_standard_name(cf_parameter) for cf_parameter in dict_for_get_cf_standard_name[dictionary_key]]

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
