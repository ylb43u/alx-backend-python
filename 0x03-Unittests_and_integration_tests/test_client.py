#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient  # adjust import based on your project structure
from utils import get_json          # only to show it's patched — not used directly

class TestGithubOrgClient(unittest.TestCase):
   
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    
    @patch("client.get_json")
    def test_org(self,org_name,mock_get_json):
        mock_response = {"name":org_name}
        mock_get_json.return_value = mock_response
        
        client = GithubOrgClient(org_name)
        result = client.org
        
        self.assertEqual(mock_response,result)
        
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        
