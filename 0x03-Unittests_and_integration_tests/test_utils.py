#!/usr/bin/env python3

import unittest
import requests
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict, Callable
from unittest.mock import patch, Mock
from functools import wraps


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


class TestAccessNestedMap(unittest.TestCase):
    # @parameterized.expand([
    #     ({"a": 1}, ("a",), 1),
    #     ({"a": {"b": 2}}, ("a","b"), 2),
    #     ({"a": {"b": 2}}, ("a", "b"), 2),
    # ])
    
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


def get_json(url: str) -> Dict:
    """Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
    ("http://example.com", {"payload": True}),
    ("http://holberton.io", {"payload": False}),
    ])
    
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        mock_get.return_value = mock_response
        
        result = get_json(test_url)
        
        mock_get.assert_called_once_with(test_url)
        
        self.assertEqual(result, test_payload)
 
class TestMemoize(unittest.TestCase):       
    
    def test_memoize(self):
        def memoize(fn:Callable)->Callable:
            attr_name = "_{}".format(fn.__name__)
            
            @wraps(fn)
            def memoized(self):
                if not hasattr(self, attr_name):
                    setattr(self, attr_name, fn(self))
                return getattr(self, attr_name)
            return property(memoized)
        
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with object.patch(TestClass,'a_method',return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            
            result2 = obj.a_property
            
            self.assertEqual(result1,42)
            self.assertEqual(result2,42)
            
            mock_method.assert_called_once()  # ✅ Confirm a_method was called only once
