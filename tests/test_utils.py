import re
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.utils as utils

class TimeTestCase(unittest.TestCase):
    """Tests for utilities dealing with time"""

    def test_create_datetime_year_month_day(self):
        """test create_datetime with a year, month and day"""
        self.assertEqual(
            utils.create_datetime(2020, 10, 15),
            datetime(2020, 10, 15).replace(tzinfo=tzutc())
        )

    def test_create_datetime_year_day_of_year(self):
        """test create_datetime with a year and day of year"""
        self.assertEqual(
            utils.create_datetime(2020, day_of_year=35),
            datetime(2020, 2, 4).replace(tzinfo=tzutc())
        )

    def test_create_datetime_year_month_day_time(self):
        """test create_datetime with a year, month, day and time"""
        self.assertEqual(
            utils.create_datetime(2020, 10, 15, hour=10, minute=25, second=38),
            datetime(2020, 10, 15, 10, 25, 38).replace(tzinfo=tzutc())
        )

    def test_create_datetime_year_day_of_year_time(self):
        """test create_datetime with a year, day of year and time"""
        self.assertEqual(
            utils.create_datetime(2020, day_of_year=35, hour=23, minute=1, second=40),
            datetime(2020, 2, 4, 23, 1, 40).replace(tzinfo=tzutc())
        )

    def test_yearmonth_regex(self):
        """The YEARMONTH_REGEX should provide a 'year' and 'month'
        named groups
        """
        self.assertDictEqual(
            re.match(utils.YEARMONTH_REGEX, '202010').groupdict(),
            {'year': '2020', 'month': '10'}
        )

    def test_yearmonthday_regex(self):
        """The YEARMONTHDAY_REGEX should provide a 'year', 'month'
        and 'day' named groups
        """
        self.assertDictEqual(
            re.match(utils.YEARMONTHDAY_REGEX, '20201017').groupdict(),
            {'year': '2020', 'month': '10', 'day': '17'}
        )

class UtilsTestCase(unittest.TestCase):
    """Test case for utils functions"""
    def test_dict_to_string(self):
        """dict_to_string() should return the proper representation"""
        self.assertEqual(
            utils.dict_to_string({'key1': 'value1', 'key2': 'value2'}),
            'key1: value1;key2: value2'
        )

    def test_empty_dict_to_string(self):
        """The representation of an empty dict is an empty string"""
        self.assertEqual(utils.dict_to_string({}), '')

    def test_translate_pythesint_keyword(self):
        """Should return the right keyword given an alias"""
        translation_dict = {
            'keyword1': ('alias11', 'alias12'),
            'keyword2': ('alias21', 'alias22'),
        }
        self.assertEqual(utils.translate_pythesint_keyword(translation_dict, 'alias11'), 'keyword1')
        self.assertEqual(utils.translate_pythesint_keyword(translation_dict, 'alias22'), 'keyword2')
        self.assertEqual(utils.translate_pythesint_keyword(translation_dict, 'alias3'), 'alias3')

    def test_get_gcmd_metopb_platform(self):
        """Test getting the right METOP-B platform"""
        self.assertEqual(
            utils.get_gcmd_platform('METOP_B'),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', 'METOP'),
                         ('Short_Name', 'METOP-B'),
                         ('Long_Name', 'Meteorological Operational Satellite - B')]))
