import logging
import requests
import argparse

def add_user_to_org(username, org_name, token):
    """
    Adds a user to an organization.

    Args:
        username (str): The username of the user.
        org_name (str): The name of the organization.
        token (str): GitHub token for authentication.
    """
    url = f"https://api.github.com/orgs/{org_name}/memberships/{username}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'role': 'member'
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logging.info(f"User {username} added to organization {org_name} successfully.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Failed to add user {username} to organization {org_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Add a user to an organization.")
    parser.add_argument('username', type=str, help="Username of the user to add.")
    parser.add_argument('org_name', type=str, help="Name of the organization.")
    parser.add_argument('token', type=str, help="GitHub token for authentication.")
    
    args = parser.parse_args()
    add_user_to_org(args.username, args.org_name, args.token)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
