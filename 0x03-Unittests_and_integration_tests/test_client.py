#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
        
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

    def test_public_repos(self):
        """Test that public_repos returns all repository names."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)


    def test_public_repos_with_license(self):
        """Test that public_repos filtered by license returns expected repos."""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

@patch("client.get_json")
def test_public_repos(self, mock_get_json):
    # 1. Mock get_json return value (payload of your choice)
    mock_get_json.return_value = [
        {"name": "repo1"},
        {"name": "repo2"},
    ]

    # 2. Mock _public_repos_url (context manager)
    with patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock,
        return_value="https://api.github.com/orgs/test_org/repos"
    ) as mock_url:

        client = GithubOrgClient("test_org")
        result = client.public_repos()

        # 3. Validate returned repository names
        self.assertEqual(result, ["repo1", "repo2"])

        # 4. Ensure mocks were called correctly
        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test_org/repos"
        )

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return fixture data based on URL."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect function to return correct payload per URL
        def side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url.endswith("/orgs/google"):
                mock_resp.json.return_value = cls.org_payload
            else:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected repository names."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    

