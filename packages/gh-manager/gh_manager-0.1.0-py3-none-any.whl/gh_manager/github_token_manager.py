import os
import logging
import requests
import argparse

def github_get_token():
    """
    Returns the user's GitHub personal access token (PAT) from the environment variable.

    Returns:
        str: The GitHub PAT, or None if not set.
    """
    return os.getenv('GITHUB_PAT')

def github_set_token(token):
    """
    Sets the user's GitHub personal access token (PAT) by defining the GITHUB_PAT environment variable.

    Args:
        token (str): The GitHub PAT to set.
    """
    os.environ['GITHUB_PAT'] = token
    logging.info("GitHub PAT set successfully.")

def github_reset_token():
    """
    Removes the value stored in the GITHUB_PAT environment variable.
    """
    if 'GITHUB_PAT' in os.environ:
        del os.environ['GITHUB_PAT']
        logging.info("GitHub PAT reset successfully.")
    else:
        logging.warning("No GitHub PAT was set.")

def github_test_token():
    """
    Checks if a PAT is valid by attempting to authenticate with the GitHub API.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    token = github_get_token()
    if not token:
        logging.error("No GitHub PAT found. Please set the token first.")
        return False

    url = "https://api.github.com/user"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.info("GitHub PAT is valid.")
        return True
    else:
        logging.error(f"GitHub PAT is invalid: {response.json().get('message', 'Unknown error')}")
        return False

def github_token_scopes():
    """
    Returns a list of scopes granted to the token.

    Returns:
        list: A list of scopes, or an empty list if the token is invalid or no scopes found.
    """
    token = github_get_token()
    if not token:
        logging.error("No GitHub PAT found. Please set the token first.")
        return []

    url = "https://api.github.com/"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        scopes = response.headers.get('X-OAuth-Scopes', '')
        scope_list = scopes.split(', ') if scopes else []
        logging.info(f"GitHub PAT scopes: {scope_list}")
        return scope_list
    else:
        logging.error(f"Failed to retrieve scopes: {response.json().get('message', 'Unknown error')}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Manage GitHub Personal Access Tokens (PAT).")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    subparsers.add_parser('get', help='Get the current GitHub PAT')

    set_parser = subparsers.add_parser('set', help='Set the GitHub PAT')
    set_parser.add_argument('token', type=str, help='The GitHub PAT to set')

    subparsers.add_parser('reset', help='Reset the GitHub PAT')

    subparsers.add_parser('test', help='Test if the GitHub PAT is valid')

    subparsers.add_parser('scopes', help='Get the scopes of the GitHub PAT')

    args = parser.parse_args()

    if args.command == 'get':
        token = github_get_token()
        if token:
            print(f"Current GitHub PAT: {token}")
        else:
            print("No GitHub PAT is currently set.")

    elif args.command == 'set':
        github_set_token(args.token)

    elif args.command == 'reset':
        github_reset_token()

    elif args.command == 'test':
        if github_test_token():
            print("GitHub PAT is valid.")
        else:
            print("GitHub PAT is invalid.")

    elif args.command == 'scopes':
        scopes = github_token_scopes()
        if scopes:
            print(f"GitHub PAT scopes: {', '.join(scopes)}")
        else:
            print("No scopes found or token is invalid.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
