#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient  # adjust import based on your project structure


class TestGithubOrgClient(unittest.TestCase):   
    """Unit tests for GithubOrgClient.has_license method."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
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
    def test_has_license(self,repo,license_key,expected):
        """Test that has_license correctly returns True or False.

        Args:
            repo (_type_): _description_
            license_key (_type_): _description_
            expected (_type_): _description_
        """
        result = GithubOrgClient("repo").has_license(repo,license_key)
        
        self.assertEqual(result,expected)
        
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos        
from parameterized import parameterized_class
from unittest.mock import Mock

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with fixtures."""
    
    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get with side_effects."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Define side_effect behavior for multiple URLs
        def side_effect(url):
            mock_resp = Mock()
            if url.endswith("/orgs/google"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that GithubOrgClient.public_repos returns expected repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos(license="apache-2.0") filters correctly"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
