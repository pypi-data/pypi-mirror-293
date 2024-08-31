import unittest
from unittest.mock import patch
from gh_manager.github_token_manager import (
    github_get_token, 
    github_set_token, 
    github_reset_token, 
    github_test_token, 
    github_token_scopes
)
import os

class TestGitHubTokenManager(unittest.TestCase):

    def test_github_get_token(self):
        os.environ['GITHUB_PAT'] = 'test-token'
        self.assertEqual(github_get_token(), 'test-token')

    def test_github_set_token(self):
        github_set_token('new-token')
        self.assertEqual(os.getenv('GITHUB_PAT'), 'new-token')

    def test_github_reset_token(self):
        os.environ['GITHUB_PAT'] = 'test-token'
        github_reset_token()
        self.assertIsNone(os.getenv('GITHUB_PAT'))

    @patch('gh_manager.github_token_manager.requests.get')
    def test_github_test_token_success(self, mock_get):
        mock_get.return_value.status_code = 200
        os.environ['GITHUB_PAT'] = 'test-token'
        self.assertTrue(github_test_token())

    @patch('gh_manager.github_token_manager.requests.get')
    def test_github_test_token_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        os.environ['GITHUB_PAT'] = 'invalid-token'
        self.assertFalse(github_test_token())

    @patch('gh_manager.github_token_manager.requests.get')
    def test_github_token_scopes_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'X-OAuth-Scopes': 'repo, user'}
        os.environ['GITHUB_PAT'] = 'test-token'
        self.assertEqual(github_token_scopes(), ['repo', 'user'])

    @patch('gh_manager.github_token_manager.requests.get')
    def test_github_token_scopes_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        os.environ['GITHUB_PAT'] = 'invalid-token'
        self.assertEqual(github_token_scopes(), [])

if __name__ == '__main__':
    unittest.main()
