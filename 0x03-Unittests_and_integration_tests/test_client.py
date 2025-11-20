#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"payload": True})

    
    def test_public_repos_url(self):
        expected_url = "https://api.github.com/orgs/test_org/repos"
        payload = {"repos_url": expected_url}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=payload
        ):
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, expected_url)

