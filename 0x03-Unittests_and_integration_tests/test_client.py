#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient  # adjust import based on your project structure


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
            
    def test_public_repos_url(self):
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}  
        with patch('client.GithubOrgClient.org',new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            
            client = GithubOrgClient("test_org")
            result = client._public_repos_url
            self.assertEqual(test_payload,result["repos_url"])
            mock_org.assert_called_once()
    
    @patch("utils.get_json")
    def test_public_repos(self,mock_get_json):
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload
        with patch("GithubOrgClient._public_repos_url",new_callable=PropertyMock) as mock_public_repo:            
            mock_public_repo.return_value = "https://api.github.com/orgs/google/repos"
            
            result = GithubOrgClient("google").public_repos()
            
            
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            
            mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/google/repos")
            mock_public_repo.assert_called_once()
  