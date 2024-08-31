import logging
import requests
import argparse

def delete_repo(repo_name, org_name, token):
    """
    Deletes a repository in a specified organization.

    Args:
        repo_name (str): The name of the repository to delete.
        org_name (str): The name of the organization.
        token (str): GitHub token for authentication.
    """
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        logging.info(f"Repository {repo_name} deleted successfully.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Failed to delete repository {repo_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Delete a repository from an organization.")
    parser.add_argument('repo_name', type=str, help="Name of the repository to delete.")
    parser.add_argument('org_name', type=str, help="Name of the organization.")
    parser.add_argument('token', type=str, help="GitHub token for authentication.")
    
    args = parser.parse_args()
    delete_repo(args.repo_name, args.org_name, args.token)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
