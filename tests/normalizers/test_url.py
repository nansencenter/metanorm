"""Tests for the URL normalizer """
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc
import metanorm.normalizers as normalizers


class URLMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the URL normalizer"""
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
            datetime(year=1982, month=12, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_jaxa(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_20120702_01D_EQOD_L3SGSSTLB3300300.h5'}),
            datetime(year=2012, month=7, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_jaxa_month_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2013/07/GW1AM2_20130700_01M_EQMA_L3SGSSTLB3300300.h5'}),
            datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2016/03/mercatorpsy4v3r1_gl12_mean_20160303_R20160316.nc'}),
            datetime(year=2016, month=3, day=3, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_3dinst_so(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-so/2019/04/mercatorpsy4v3r1_gl12_so_20190403_18h_R20190404.nc'}),
            datetime(year=2019, month=4, day=3, hour=18, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_3dinst_thetao(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-thetao/2020/04/mercatorpsy4v3r1_gl12_thetao_20200404_18h_R20200405.nc'}),
            datetime(year=2020, month=4, day=4, hour=18, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_3dinst_uovo(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-uovo/2020/04/mercatorpsy4v3r1_gl12_uovo_20200403_06h_R20200404.nc'}),
            datetime(year=2020, month=4, day=3, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_hourly_merged_uv(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-merged-uv/2019/05/SMOC_20190515_R20190516.nc'}),
            datetime(year=2019, month=5, day=15, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_hourly_t_u_v_ssh(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/2020/05/mercatorpsy4v3r1_gl12_hrly_20200511_R20200520.nc'}),
            datetime(year=2020, month=5, day=11, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_monthly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-monthly/2018/mercatorpsy4v3r1_gl12_mean_201807.nc'}),
            datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4/2019/04/nrt_global_allsat_phy_l4_20190403_20200320.nc'}),
            datetime(year=2019, month=4, day=3, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_multiobs_glo_phy_nrt_015_003_daily(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-daily/2020/03/dataset-uv-nrt-daily_20200301T0000Z_P20200307T0000.nc'}),
            datetime(year=2020, month=3, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_multiobs_glo_phy_nrt_015_003_monthly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-monthly/2020/dataset-uv-nrt-monthly_202004T0000Z_P20200506T0000.nc'}),
            datetime(year=2020, month=4, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_multiobs_glo_phy_nrt_015_003_hourly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-hourly/2020/09/dataset-uv-nrt-hourly_20200906T1800Z_P20200918T0000.nc'}),
            datetime(year=2020, month=9, day=6, hour=18, minute=0, second=0, tzinfo=tzutc()))

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
            datetime(year=2010, month=12, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_jaxa_single_day_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2015/04/GW1AM2_20150401_01D_EQOD_L3SGSSTLB3300300.h5'}),
            datetime(year=2015, month=4, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_jaxa_month_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2015/04/GW1AM2_20150400_01M_EQMD_L3SGSSTLB3300300.h5'}),
            datetime(year=2015, month=4, day=30, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2016/03/mercatorpsy4v3r1_gl12_mean_20160303_R20160316.nc'}),
            datetime(year=2016, month=3, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_3dinst_so(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-so/2019/04/mercatorpsy4v3r1_gl12_so_20190403_18h_R20190404.nc'}),
            datetime(year=2019, month=4, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_3dinst_thetao(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-thetao/2020/04/mercatorpsy4v3r1_gl12_thetao_20200404_18h_R20200405.nc'}),
            datetime(year=2020, month=4, day=5, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_3dinst_uovo(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-uovo/2020/04/mercatorpsy4v3r1_gl12_uovo_20200403_06h_R20200404.nc'}),
            datetime(year=2020, month=4, day=3, hour=12, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_hourly_merged_uv(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-merged-uv/2019/05/SMOC_20190515_R20190516.nc'}),
            datetime(year=2019, month=5, day=16, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_hourly_t_u_v_ssh(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/2020/05/mercatorpsy4v3r1_gl12_hrly_20200511_R20200520.nc'}),
            datetime(year=2020, month=5, day=12, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_monthly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-monthly/2018/mercatorpsy4v3r1_gl12_mean_201807.nc'}),
            datetime(year=2018, month=7, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4/2019/04/nrt_global_allsat_phy_l4_20190403_20200320.nc'}),
            datetime(year=2019, month=4, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_multiobs_glo_phy_nrt_015_003_daily(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-daily/2020/03/dataset-uv-nrt-daily_20200302T0000Z_P20200307T0000.nc'}),
            datetime(year=2020, month=3, day=3, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_multiobs_glo_phy_nrt_015_003_monthly(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-monthly/2020/dataset-uv-nrt-monthly_202004T0000Z_P20200506T0000.nc'}),
            datetime(year=2020, month=4, day=30, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_multiobs_glo_phy_nrt_015_003_hourly(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-hourly/2020/09/dataset-uv-nrt-hourly_20200906T0000Z_P20200918T0000.nc'}),
            datetime(year=2020, month=9, day=7, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_instrument_jaxa(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
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

    def test_instrument_global_analysis_forecast_phy_001_024(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')])
        )

    def test_instrument_multiobs_glo_phy_nrt_015_003(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_platform_jaxa(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
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

    def test_platform_global_analysis_forecast_phy_001_024(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category','Models/Analyses'),
                        ('Series_Entity',''),
                        ('Short_Name','OPERATIONAL MODELS'),
                        ('Long_Name','')])
        )

    def test_platform_multiobs_glo_phy_nrt_015_003(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category','Earth Observation Satellites'),
                        ('Series_Entity',''),
                        ('Short_Name',''),
                        ('Long_Name','')])
        )

    def test_platform_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category','Earth Observation Satellites'),
                        ('Series_Entity',''),
                        ('Short_Name',''),
                        ('Long_Name','')])
        )

    def test_provider_jaxa(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
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

    def test_provider_global_analysis_forecast_phy_001_024(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_provider_multiobs_glo_phy_nrt_015_003(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_provider_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_dataset_parameters_jaxa(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
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

    def test_dataset_parameters_phy_001_024(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [
                OrderedDict([('standard_name', 'ocean_mixed_layer_thickness_defined_by_sigma_theta'),
                             ('canonical_units', 'm'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'The ocean mixed layer is the upper part of the ocean, regarded as being well-mixed. The base of the mixed layer defined by temperature, sigma or sigma_theta is the level at which the quantity indicated differs from its surface value by a certain amount.')]),
                OrderedDict([('standard_name', 'sea_ice_area_fraction'),
                             ('canonical_units', '1'),
                             ('grib', '91'),
                             ('amip', 'sic'),
                             ('description', '"X_area_fraction" means the fraction of horizontal area occupied by X. "X_area" means the horizontal area occupied by X within the grid cell. Sea ice area fraction is area of the sea surface occupied by sea ice. It is also called "sea ice concentration".')]),
                OrderedDict([('standard_name', 'sea_ice_thickness'),
                             ('canonical_units', 'm'),
                             ('grib', '92'),
                             ('amip', 'sit'),
                             ('description', 'The surface temperature is the (skin) temperature at the interface, not the bulk temperature of the medium above or below.  "Sea ice surface temperature" is the temperature that exists at the interface of sea ice and an overlying medium which may be air or snow.  In areas of snow covered sea ice, sea_ice_surface_temperature is not the same as the quantity with standard name surface_temperature.')]),
                OrderedDict([('standard_name', 'sea_water_salinity'),
                             ('canonical_units', '1e-3'),
                             ('grib', '88'),
                             ('amip', 'so'),
                             ('description', 'Sea water salinity is the salt content of sea water, often on the Practical Salinity Scale of 1978. However, the unqualified term \'salinity\' is generic and does not necessarily imply any particular method of calculation. The units of salinity are dimensionless and the units attribute should normally be given as 1e-3 or 0.001 i.e. parts per thousand. There are standard names for the more precisely defined salinity quantities: sea_water_knudsen_salinity, S_K (used for salinity observations between 1901 and 1966),  sea_water_cox_salinity, S_C (used for salinity observations between 1967 and 1977), sea_water_practical_salinity, S_P (used for salinity observations from 1978 to the present day), sea_water_absolute_salinity, S_A, sea_water_preformed_salinity, S_*, and sea_water_reference_salinity. Practical Salinity is reported on the Practical Salinity Scale of 1978 (PSS-78), and is usually based on the electrical conductivity of sea water in observations since the 1960s. Conversion of data between the observed scales follows: S_P = (S_K - 0.03) * (1.80655 / 1.805) and S_P = S_C, however the accuracy of the latter is dependent on whether chlorinity or conductivity was used to determine the S_C value, with this inconsistency driving the development of PSS-78. The more precise standard names should be used where appropriate for both modelled and observed salinities. In particular, the use of sea_water_salinity to describe salinity observations made from 1978 onwards is now deprecated in favor of the term sea_water_practical_salinity which is the salinity quantity stored by national data centers for post-1978 observations. The only exception to this is where the observed salinities are definitely known not to be recorded on the Practical Salinity Scale. The unit "parts per thousand" was used for sea_water_knudsen_salinity and sea_water_cox_salinity.')]),
                OrderedDict([('standard_name', 'sea_water_potential_temperature'),
                             ('canonical_units', 'K'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'Potential temperature is the temperature a parcel of air or sea water would have if moved adiabatically to sea level pressure.')]),
                OrderedDict([('standard_name', 'eastward_sea_water_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', '49'),
                             ('amip', ''),
                             ('description', 'A velocity is a vector quantity. "Eastward" indicates a vector component which is positive when directed eastward (negative westward).')]),
                OrderedDict([('standard_name', 'eastward_sea_ice_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', '95'),
                             ('amip', ''),
                             ('description', 'A velocity is a vector quantity. "Eastward" indicates a vector component which is positive when directed eastward (negative westward). Sea ice velocity is defined as a two-dimensional vector, with no vertical component.')]),
                OrderedDict([('standard_name', 'northward_sea_water_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', '50'),
                             ('amip', ''),
                             ('description', 'A velocity is a vector quantity. "Northward" indicates a vector component which is positive when directed northward (negative southward).')]),
                OrderedDict([('standard_name', 'northward_sea_ice_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', '96'),
                             ('amip', ''),
                             ('description', 'A velocity is a vector quantity. "Northward" indicates a vector component which is positive when directed northward (negative southward). Sea ice velocity is defined as a two-dimensional vector, with no vertical component.')]),
                OrderedDict([('standard_name', 'sea_surface_height_above_geoid'),
                             ('canonical_units', 'm'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'The geoid is a surface of constant geopotential with which mean sea level would coincide if the ocean were at rest. (The volume enclosed between the geoid and the sea floor equals the mean volume of water in the ocean.) In an ocean GCM the geoid is the surface of zero depth, or the rigid lid if the model uses that approximation. "Sea surface height" is a time-varying quantity. By definition of the geoid, the global average of the time-mean sea surface height (i.e. mean sea level) above the geoid must be zero. The standard name for the height of the sea surface above mean sea level is sea_surface_height_above_sea_level. The standard name for the height of the sea surface above the reference ellipsoid is sea_surface_height_above_reference_ellipsoid.')])
            ]
        )

    def test_dataset_parameters_multiobs_glo_phy_nrt_015_003(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [
                OrderedDict([('standard_name', 'eastward_sea_water_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', '49'),
                             ('amip', ''),
                             ('description', 'A velocity is a vector quantity. "Eastward" indicates a vector component which is positive when directed eastward (negative westward).')]),
                OrderedDict([('standard_name', 'northward_sea_water_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', '50'),
                             ('amip', ''),
                             ('description', 'A velocity is a vector quantity. "Northward" indicates a vector component which is positive when directed northward (negative southward).')]),
            ]
        )

    def test_dataset_parameters_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [
                OrderedDict([('standard_name', 'surface_geostrophic_eastward_sea_water_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'The surface called "surface" means the lower boundary of the atmosphere. A velocity is a vector quantity. "Eastward" indicates a vector component which is positive when directed eastward (negative westward). "Geostrophic" indicates that geostrophic balance is assumed. "Water" means water in all phases. surface_geostrophic_eastward_sea_water_velocity is the sum of a variable part, surface_geostrophic_eastward_sea_water_velocity_assuming_sea_level_for_geoid, and a constant part due to the stationary component of ocean circulation.')]),
                OrderedDict([('standard_name', 'surface_geostrophic_eastward_sea_water_velocity_assuming_sea_level_for_geoid'),
                             ('canonical_units', 'm s-1'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'The surface called "surface" means the lower boundary of the atmosphere. A velocity is a vector quantity. "Eastward" indicates a vector component which is positive when directed eastward (negative westward). "Geostrophic" indicates that geostrophic balance is assumed. "Water" means water in all phases. "sea_level" means mean sea level. The geoid is a surface of constant geopotential with which mean sea level would coincide if the ocean were at rest. surface_geostrophic_eastward_sea_water_velocity_assuming_sea_level_for_geoid is the variable part of surface_geostrophic_eastward_sea_water_velocity. The assumption that sea level is equal to the geoid means that the stationary component of ocean circulation is equal to zero.')]),
                OrderedDict([('standard_name', 'surface_geostrophic_northward_sea_water_velocity'),
                             ('canonical_units', 'm s-1'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'The surface called "surface" means the lower boundary of the atmosphere. A velocity is a vector quantity. "Northward" indicates a vector component which is positive when directed northward (negative southward). "Geostrophic" indicates that geostrophic balance is assumed. "Water" means water in all phases. surface_geostrophic_northward_sea_water_velocity is the sum of a variable part, surface_geostrophic_northward_sea_water_velocity_assuming_sea_level_for_geoid, and a constant part due to the stationary component of ocean circulation.')]),
                OrderedDict([('standard_name', 'surface_geostrophic_northward_sea_water_velocity_assuming_sea_level_for_geoid'),
                             ('canonical_units', 'm s-1'),
                             ('grib', ''),
                             ('amip', ''),
                             ('description', 'The surface called "surface" means the lower boundary of the atmosphere. A velocity is a vector quantity. "Northward" indicates a vector component which is positive when directed northward (negative southward). "Geostrophic" indicates that geostrophic balance is assumed. "Water" means water in all phases. "sea_level" means mean sea level. The geoid is a surface of constant geopotential with which mean sea level would coincide if the ocean were at rest. surface_geostrophic_northward_sea_water_velocity_assuming_sea_level_for_geoid is the variable part of surface_geostrophic_northward_sea_water_velocity. The assumption that sea level is equal to the geoid means that the stationary component of ocean circulation is equal to zero.')])
            ]
        )

    def test_entry_title_jaxa(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes), 'AMSR2-L3 Sea Surface Temperature')

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

    def test_entry_title_global_analysis_forecast_phy_001_024(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),'GLOBAL OCEAN 1_12 PHYSICS ANALYSIS AND FORECAST UPDATED DAILY')

    def test_entry_title_multiobs_glo_phy_nrt_015_003(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),'GLOBAL TOTAL SURFACE AND 15M CURRENT FROM ALTIMETRIC GEOSTROPHIC CURRENT AND MODELED EKMAN CURRENT PROCESSING')

    def test_entry_title_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),'GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT')

    def test_entry_id_jaxa(self):
        """entry_id from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes), 'GW1AM2_201207031905_134D_L2SGSSTLB3300300')

    def test_entry_id_remss(self):
        """entry_id from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140603v8.2.gz'}
        self.assertEqual(self.normalizer.get_entry_id(attributes),
                         'f35_20140603v8.2')

    def test_entry_id_ceda(self):
        """entry_id from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), 'D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0')

    def test_entry_id_for_unkown_file_type(self):
        """entry_id shall equal to None for an unknown fileformat """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.bb'}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), None)

    def test_entry_id_for_thredds_met_no_dods(self):
        """entry_id from URLMetadataNormalizer for a dods URL from thredds.met.no"""
        attributes = {
            'url': "https://thredds.met.no/thredds/dodsC/osisaf/met.no/ice/Some/path/to/file/ice_type_sh_polstere-100_multi_201609261200.nc.dods"}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'ice_type_sh_polstere-100_multi_201609261200')

    def test_entry_id_for_thredds_met_no_fileserver(self):
        """entry_id from URLMetadataNormalizer for a fileServer URL from thredds.met.no"""
        attributes = {
            'url': "https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/Some/path/to/file/ice_type_sh_polstere-100_multi_201609261200.nc"}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'ice_type_sh_polstere-100_multi_201609261200')

    def test_entry_id_for_podaac_ingester(self):
        """entry_id from URLMetadataNormalizer for PODAAC metadata"""
        attributes = {
            'url': "https://opendap.jpl.nasa.gov/opendap/Some/path/to/file/20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0.nc"}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), '20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0')

    def test_entry_id_for_marine_copernicus(self):
        """entry_id from URLMetadataNormalizer for marine copernicus metadata"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/Some/path/to/file/20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0.nc"}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), '20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0')

    def test_geometry_jaxa_the_first_type_of_sst(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_jaxa_the_second_type_of_sst(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_phy_001_024(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_multiobs_glo_phy_nrt_015_003(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_remss(self):
        """geometry from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_ceda(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

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
        self.assertIsNone(self.normalizer.get_entry_id({'url': 'ftp://test/'}))

    def test_for_delivering_none_when_lacking_url_in_raw_attributes(self):
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
        self.assertIsNone(self.normalizer.get_entry_id({'none-url': 'ftp://test/'}))
