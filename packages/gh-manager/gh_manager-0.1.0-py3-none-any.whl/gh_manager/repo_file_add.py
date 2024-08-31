import logging
import requests
import argparse
import base64

def add_file_to_repo(repo_name, org_name, file_path, file_content, commit_message, token):
    """
    Adds a file to a repository.

    Args:
        repo_name (str): The name of the repository.
        org_name (str): The name of the organization.
        file_path (str): Path of the file in the repo.
        file_content (str): The content of the file.
        commit_message (str): Commit message for the file addition.
        token (str): GitHub token for authentication.
    """
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/contents/{file_path}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'message': commit_message,
        'content': base64.b64encode(file_content.encode('utf-8')).decode('utf-8'),
        'branch': 'main'
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logging.info(f"File {file_path} added to {repo_name} successfully.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Failed to add file {file_path} to {repo_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Add a file to a repository.")
    parser.add_argument('repo_name', type=str, help="Name of the repository.")
    parser.add_argument('org_name', type=str, help="Name of the organization.")
    parser.add_argument('file_path', type=str, help="Path of the file in the repository.")
    parser.add_argument('file_content', type=str, help="Content of the file to add.")
    parser.add_argument('commit_message', type=str, help="Commit message for the addition.")
    parser.add_argument('token', type=str, help="GitHub token for authentication.")
    
    args = parser.parse_args()
    add_file_to_repo(args.repo_name, args.org_name, args.file_path, args.file_content, args.commit_message, args.token)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
