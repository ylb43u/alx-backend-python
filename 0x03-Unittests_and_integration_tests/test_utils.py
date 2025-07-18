#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
  
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")    
