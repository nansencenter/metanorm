"""Tests for the utils module"""
import re
import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.errors as errors
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

    def test_raises_decorator(self):
        """Test that the `raises()` decorator raises a
        MetadataNormalizationError when the function it decorates
        raises the exception given as argument to the decorator
        """
        # the type annotation prevents Pylance from wrongfully marking
        # the following code as unreachable
        @utils.raises(KeyError)
        def get_foo(self, raw_metadata) -> None:
            raise KeyError

        with self.assertRaises(errors.MetadataNormalizationError) as raised:
            get_foo(mock.Mock(), {})
        self.assertIsInstance(raised.exception.__cause__, KeyError)

    def test_raises_decorator_with_tuple(self):
        """Test that the `raises()` decorator raises a
        MetadataNormalizationError when the function it decorates
        raises one of the exceptions given as argument to the decorator
        """
        # the type annotation prevents Pylance from wrongfully marking
        # the following code as unreachable
        @utils.raises((KeyError, IndexError))
        def get_foo(self, raw_metadata) -> None:
            raise IndexError

        with self.assertRaises(errors.MetadataNormalizationError) as raised:
            get_foo(mock.Mock(), {})
        self.assertIsInstance(raised.exception.__cause__, IndexError)

    def test_raises_decorator_wrong_exception(self):
        """Test that the `raises()` decorator does not catch exceptions
        which are not in its arguments
        """
        # the type annotation prevents Pylance from wrongfully marking
        # the following code as unreachable
        @utils.raises(KeyError)
        def get_foo(self, raw_metadata) -> None:
            raise ValueError

        with self.assertRaises(ValueError):
            get_foo(mock.Mock(), {})


class SubclassesTestCase(unittest.TestCase):
    """Tests for utility functions dealing with subclasses"""

    class Base():
        """Base class for tests"""

    class A(Base):
        """Class for testing"""

    class B(Base):
        """Class for testing"""

    class C(B):
        """Class for testing"""

    class D(A, B):
        """Class for testing"""


    def test_get_all_subclasses(self):
        """Test that get_all_subclasses() returns all subclasses of
        the base class
        """
        self.assertEqual(
            utils.get_all_subclasses(self.Base),
            set((self.A, self.B, self.C, self.D)))

    def test_export_subclasses(self):
        """Test that export_subclasses imports the modules of the
        package and adds subclasses to __all__
        """
        # simulate the output of pkgutil.iter_modules()
        # see https://docs.python.org/3.7/library/pkgutil.html#pkgutil.iter_modules
        modules = (
            (mock.Mock(), 'module1', False),
            (mock.Mock(), 'module2', False)
        )
        with mock.patch('pkgutil.iter_modules', return_value=iter(modules)), \
             mock.patch('importlib.import_module') as mock_import_module, \
             mock.patch('sys.modules') as mock_sys_modules:
            package__all__ = []
            utils.export_subclasses(package__all__, 'package', '/foo/package', self.Base)
        self.assertCountEqual(package__all__, ['Base', 'A', 'B', 'C', 'D'])
