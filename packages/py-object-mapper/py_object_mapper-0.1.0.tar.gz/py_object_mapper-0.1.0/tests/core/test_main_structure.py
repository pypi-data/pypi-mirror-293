import json
import unittest

from src.mapper.core.mapper import Mapper
from tests.model.range import Range
from tests.model.range_wrapper import RangeWrapper, OptionalRangeWrapper, \
    DefaultRangeWrapper


# noinspection PyArgumentList
class TestMainStructure(unittest.TestCase):

    def setUp(self):
        self.mapper = Mapper()

    def test_is_singleton(self):
        self.assertIs(self.mapper, Mapper())

    def test_simple_mapping_obj(self):
        interval: Range = self.mapper.map(dict(start=1, end=10), Range)
        self.assertIsInstance(interval, Range)
        self.assertEqual(interval.start, 1)
        self.assertEqual(interval.end, 10)

    def test_simple_mapping_dict(self):
        interval = Range(1, 10)
        self.interval_dict = self.mapper.to_dict(interval)

        self.assertIsInstance(self.interval_dict, dict)
        self.assertEqual(self.interval_dict, dict(start=1, end=10))

    def test_simple_mapping_json(self):
        interval = Range(1, 10)
        interval_json = self.mapper.to_json(interval)

        self.assertIsInstance(interval_json, str)
        self.assertEqual(interval_json, json.dumps(dict(start=1, end=10)))

    def test_simple_composite_obj(self):
        wrapper_input = dict(
            description="test",
            interval=Range(1, 10)
        )

        wrapper: RangeWrapper = self.mapper.map(
            wrapper_input,
            RangeWrapper
        )

        self.assertIsInstance(wrapper, RangeWrapper)
        self.assertEqual(wrapper.description, "test")
        self.assertEqual(wrapper.interval.start, 1)
        self.assertEqual(wrapper.interval.end, 10)

    def test_simple_composite_dict(self):
        wrapper = RangeWrapper("test", Range(1, 10))
        wrapper_dict = self.mapper.to_dict(wrapper)

        wrapper_input = dict(
            description="test",
            interval=dict(start=1, end=10)
        )

        self.assertIsInstance(wrapper_dict, dict)
        self.assertEqual(wrapper_dict, wrapper_input)

    def test_simple_composite_json(self):
        wrapper = RangeWrapper("test", Range(1, 10))
        wrapper_json = self.mapper.to_json(wrapper)
        wrapper_input = dict(
            description="test",
            interval=dict(start=1, end=10)
        )

        self.assertIsInstance(wrapper_json, str)
        self.assertEqual(wrapper_json, json.dumps(wrapper_input))

    def test_optional_composite_obj(self):
        optional_wrapper_input = dict(description="test")
        optional_wrapper: OptionalRangeWrapper = self.mapper.map(
            optional_wrapper_input,
            OptionalRangeWrapper
        )

        self.assertIsInstance(optional_wrapper, OptionalRangeWrapper)
        self.assertEqual(optional_wrapper.description, "test")
        self.assertIsNone(optional_wrapper.interval)

    def test_optional_composite_dict(self):
        optional_wrapper_input = dict(description="test")
        optional_wrapper = OptionalRangeWrapper("test")
        optional_wrapper_dict = self.mapper.to_dict(optional_wrapper)

        self.assertIsInstance(optional_wrapper_dict, dict)
        self.assertEqual(optional_wrapper_dict, optional_wrapper_input)

    def test_optional_composite_json(self):
        optional_wrapper_input = dict(description="test")
        optional_wrapper = OptionalRangeWrapper("test")
        optional_wrapper_json = self.mapper.to_json(optional_wrapper)

        self.assertIsInstance(optional_wrapper_json, str)
        self.assertEqual(optional_wrapper_json,
                         json.dumps(optional_wrapper_input))

    def test_default_composite_obj(self):
        default_wrapper_input = dict(description="test")
        default_wrapper: DefaultRangeWrapper = self.mapper.map(
            default_wrapper_input,
            DefaultRangeWrapper
        )
        self.assertIsInstance(default_wrapper, DefaultRangeWrapper)
        self.assertEqual(default_wrapper.description, "test")
        self.assertEqual(default_wrapper.interval.start, 1)
        self.assertEqual(default_wrapper.interval.end, 10)

    def test_default_composite_dict(self):
        default_wrapper_input = dict(description="test",
                                     interval=dict(start=1, end=10))
        default_wrapper = DefaultRangeWrapper("test")
        default_wrapper_dict = self.mapper.to_dict(default_wrapper)

        self.assertIsInstance(default_wrapper_dict, dict)
        self.assertEqual(default_wrapper_dict, default_wrapper_input)

    def test_default_composite_json(self):
        default_wrapper_input = dict(description="test",
                                     interval=dict(start=1, end=10))
        default_wrapper = DefaultRangeWrapper("test")
        default_wrapper_json = self.mapper.to_json(default_wrapper)

        self.assertIsInstance(default_wrapper_json, str)
        self.assertEqual(default_wrapper_json,
                         json.dumps(default_wrapper_input))


if __name__ == '__main__':
    unittest.main()
