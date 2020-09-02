"""Tests for the FTP normalizer of some ftp resources"""
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers


class URLMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the FTP normalizer"""
    @classmethod
    def setUpClass(cls):
        cls.normalizer = normalizers.URLMetadataNormalizer([], [])

    def test_time_coverage_start_remss_month_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_201406v8.2.gz'}),
            datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_remss_single_day_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140604v8.2.gz'}),
            datetime(year=2014, month=6, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_remss_week_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/weeks/f35_20140610v8.2.gz'}),
            datetime(year=2014, month=6, day=7, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_remss_3d3_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140630v8.2_d3d.gz'}),
            datetime(year=2014, month=6, day=29, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ceda(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}),
            datetime(year=1983, month=1, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_jaxa(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}),
            datetime(year=2012, month=7, day=3, hour=19, minute=5, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_single_day_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140620v8.2.gz'}),
            datetime(year=2014, month=6, day=20, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_month_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_201406v8.2.gz'}),
            datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_week_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/weeks/f35_20140610v8.2.gz'}),
            datetime(year=2014, month=6, day=13, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_3d3_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140620v8.2_d3d.gz'}),
            datetime(year=2014, month=6, day=21, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ceda(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}),
            datetime(year=2011, month=1, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_jaxa(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}),
            datetime(year=2012, month=7, day=3, hour=19, minute=5, second=0, tzinfo=tzutc()))

    def test_instrument_jaxa(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'AMSR2'),
                         ('Long_Name', 'Advanced Microwave Scanning Radiometer 2')])
        )

    def test_instrument_remss(self):
        """instrument from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'GMI'),
                         ('Long_Name', 'Global Precipitation Measurement Microwave Imager')])
        )

    def test_instrument_ceda(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_platform_jaxa(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'GCOM-W1'),
                         ('Long_Name', 'Global Change Observation Mission 1st-Water')])
        )

    def test_platform_remss(self):
        """platform from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'GPM'),
                         ('Long_Name', 'Global Precipitation Measurement')])
        )

    def test_platform_ceda(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_provider_jaxa(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'GOVERNMENT AGENCIES-NON-US'),
                         ('Bucket_Level1', 'JAPAN'),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'JP/JAXA/EOC'),
                         ('Long_Name', 'Earth Observation Center, Japan Aerospace Exploration Agency, Japan'),
                         ('Data_Center_URL', 'http://www.eorc.jaxa.jp/en/index.html')])
        )

    def test_provider_remss(self):
        """provider from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'GOVERNMENT AGENCIES-U.S. FEDERAL AGENCIES'),
                         ('Bucket_Level1', 'NASA'),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'NASA/GSFC/SED/ESD/LA/GPM'),
                         ('Long_Name', 'GPM Project Office, Laboratory for Atmospheres, Earth Sciences Division, Science and Exploration Directorate, Goddard Space Flight Center, NASA'),
                         ('Data_Center_URL', 'https://pmm.nasa.gov/')])
        )

    def test_provider_ceda(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'ESA/CCI'),
                         ('Long_Name', 'Climate Change Initiative, European Space Agency'),
                         ('Data_Center_URL', '')])
        )

    def test_dataset_parameters_jaxa(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [OrderedDict([('standard_name', 'sea_surface_temperature'),
                          ('canonical_units', 'K'),
                          ('grib', ''),
                          ('amip', ''),
                          ('description', 'Sea surface temperature is usually abbreviated as "SST". It is the temperature of sea water near the surface (including the part under sea-ice, if any), and not the skin temperature, whose standard name is surface_temperature. For the temperature of sea water at a particular depth or layer, a data variable of sea_water_temperature with a vertical coordinate axis should be used.')]), ]
        )

    def test_dataset_parameters_remss(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [OrderedDict([('standard_name', 'wind_speed'),
                          ('canonical_units', 'm s-1'),
                          ('grib', '32'),
                          ('amip', ''),
                          ('description', 'Speed is the magnitude of velocity. Wind is defined as a two-dimensional (horizontal) air velocity vector, with no vertical component. (Vertical motion in the atmosphere has the standard name upward_air_velocity.) The wind speed is the magnitude of the wind velocity.')]),
             OrderedDict([('standard_name', 'atmosphere_mass_content_of_water_vapor'),
                          ('canonical_units', 'kg m-2'),
                          ('grib', '54'),
                          ('amip', 'prw'),
                          ('description', '"Content" indicates a quantity per unit area. The "atmosphere content" of a quantity refers to the vertical integral from the surface to the top of the atmosphere. For the content between specified levels in the atmosphere, standard names including content_of_atmosphere_layer are used. Atmosphere water vapor content is sometimes referred to as "precipitable water", although this term does not imply the water could all be precipitated.')]),
             OrderedDict([('standard_name', 'atmosphere_mass_content_of_cloud_liquid_water'),
                          ('canonical_units', 'kg m-2'),
                          ('grib', ''),
                          ('amip', ''),
                          ('description', '"Content" indicates a quantity per unit area. The "atmosphere content" of a quantity refers to the vertical integral from the surface to the top of the atmosphere. For the content between specified levels in the atmosphere, standard names including content_of_atmosphere_layer are used.')]),
             OrderedDict([('standard_name', 'rainfall_rate'),
                          ('canonical_units', 'm s-1'),
                          ('grib', ''),
                          ('amip', ''),
                          ('description', 'In accordance with common usage in geophysical disciplines, "flux" implies per unit area, called "flux density" in physics.')]),
             ]
        )

    def test_dataset_parameters_ceda(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [OrderedDict([('standard_name', 'sea_surface_temperature'),
                          ('canonical_units', 'K'),
                          ('grib', ''),
                          ('amip', ''),
                          ('description', 'Sea surface temperature is usually abbreviated as "SST". It is the temperature of sea water near the surface (including the part under sea-ice, if any), and not the skin temperature, whose standard name is surface_temperature. For the temperature of sea water at a particular depth or layer, a data variable of sea_water_temperature with a vertical coordinate axis should be used.')]), ]
        )

    def test_entry_title_jaxa(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes), 'AMSR2-L2 Sea Surface Temperature')

    def test_entry_title_remss(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(self.normalizer.get_entry_title(attributes),
                         'Atmosphere parameters from Global Precipitation Measurement Microwave Imager')

    def test_entry_title_ceda(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(self.normalizer.get_entry_title(
            attributes), 'ESA SST CCI OSTIA L4 Climatology')

    def test_none_for_incorrect_ftp_resource(self):
        """shall return None in the case of incorrect ftp resource (incorrect 'ftp_domain_name')
        and [] for the cumulative ones """
        self.assertEqual([], self.normalizer.get_dataset_parameters({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_entry_title({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_instrument({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_platform({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_provider({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_end({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_start({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_location_geometry({'url': 'ftp://test/'}))

    def test_none_when_lacking_url_in_raw_attributes(self):
        """shall return None in the case of no 'url' field in the raw_attribute dictionary
        and [] for the cumulative ones.
        This test is for asserting the correct behavior of this normalizer inside
        the chain of normalizer in order not to intract with other type of raw_attributes """
        self.assertEqual([], self.normalizer.get_dataset_parameters({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_entry_title({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_instrument({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_platform({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_provider({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_end({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_start({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_location_geometry({'none-url': 'ftp://test/'}))
