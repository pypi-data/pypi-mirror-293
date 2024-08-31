import unittest
from unittest.mock import patch
from gh_manager.org_username_add import add_user_to_org

class TestAddUserToOrg(unittest.TestCase):

    @patch('gh_manager.org_username_add.requests.put')
    def test_add_user_to_org_success(self, mock_put):
        mock_put.return_value.status_code = 200
        add_user_to_org('test-user', 'test-org', 'fake-token')
        mock_put.assert_called_once_with(
            'https://api.github.com/orgs/test-org/memberships/test-user',
            headers={'Authorization': 'token fake-token', 'Accept': 'application/vnd.github.v3+json'},
            json={'role': 'member'}
        )

    @patch('gh_manager.org_username_add.requests.put')
    def test_add_user_to_org_failure(self, mock_put):
        mock_put.return_value.status_code = 404
        add_user_to_org('nonexistent-user', 'test-org', 'fake-token')
        mock_put.assert_called_once()

if __name__ == '__main__':
    unittest.main()
