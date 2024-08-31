import unittest
from unittest.mock import patch
from gh_manager.repo_file_update import update_file_in_repo
import base64

class TestUpdateFileInRepo(unittest.TestCase):

    @patch('gh_manager.repo_file_update.requests.put')
    def test_update_file_in_repo_success(self, mock_put):
        mock_put.return_value.status_code = 200
        update_file_in_repo('test-repo', 'test-org', 'test.txt', 'Updated content', 'Update test.txt', 'fake-token', 'fake-sha')
        encoded_content = base64.b64encode('Updated content'.encode('utf-8')).decode('utf-8')
        mock_put.assert_called_once_with(
            'https://api.github.com/repos/test-org/test-repo/contents/test.txt',
            headers={'Authorization': 'token fake-token', 'Accept': 'application/vnd.github.v3+json'},
            json={'message': 'Update test.txt', 'content': encoded_content, 'sha': 'fake-sha', 'branch': 'main'}
        )

    @patch('gh_manager.repo_file_update.requests.put')
    def test_update_file_in_repo_failure(self, mock_put):
        mock_put.return_value.status_code = 404
        update_file_in_repo('nonexistent-repo', 'test-org', 'test.txt', 'Updated content', 'Update test.txt', 'fake-token', 'fake-sha')
        mock_put.assert_called_once()

if __name__ == '__main__':
    unittest.main()
