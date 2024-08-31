import unittest
from unittest.mock import patch
from gh_manager.delete_repo import delete_repo

class TestDeleteRepo(unittest.TestCase):

    # Patch 'requests.delete' directly from where it is used in 'delete_repo.py'
    @patch('gh_manager.delete_repo.requests.delete')
    def test_delete_repo_success(self, mock_delete):
        mock_delete.return_value.status_code = 204

        delete_repo('test-repo', 'test-org', 'fake-token')

        mock_delete.assert_called_once_with(
            'https://api.github.com/repos/test-org/test-repo',
            headers={'Authorization': 'token fake-token', 'Accept': 'application/vnd.github.v3+json'}
        )

    @patch('gh_manager.delete_repo.requests.delete')
    def test_delete_repo_failure(self, mock_delete):
        mock_delete.return_value.status_code = 404

        delete_repo('nonexistent-repo', 'test-org', 'fake-token')

        mock_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
