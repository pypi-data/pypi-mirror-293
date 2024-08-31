import unittest
from unittest.mock import patch
from gh_manager.repo_file_add import add_file_to_repo
import base64

class TestAddFileToRepo(unittest.TestCase):

    @patch('gh_manager.repo_file_add.requests.put')
    def test_add_file_to_repo_success(self, mock_put):
        mock_put.return_value.status_code = 201
        add_file_to_repo('test-repo', 'test-org', 'test.txt', 'Hello, world!', 'Add test.txt', 'fake-token')
        encoded_content = base64.b64encode('Hello, world!'.encode('utf-8')).decode('utf-8')
        mock_put.assert_called_once_with(
            'https://api.github.com/repos/test-org/test-repo/contents/test.txt',
            headers={'Authorization': 'token fake-token', 'Accept': 'application/vnd.github.v3+json'},
            json={'message': 'Add test.txt', 'content': encoded_content, 'branch': 'main'}
        )

    @patch('gh_manager.repo_file_add.requests.put')
    def test_add_file_to_repo_failure(self, mock_put):
        mock_put.return_value.status_code = 404
        add_file_to_repo('nonexistent-repo', 'test-org', 'test.txt', 'Hello, world!', 'Add test.txt', 'fake-token')
        mock_put.assert_called_once()

if __name__ == '__main__':
    unittest.main()
