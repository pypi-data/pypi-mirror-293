import logging
import requests
import argparse
import base64

def update_file_in_repo(repo_name, org_name, file_path, file_content, commit_message, token, sha):
    """
    Updates a file in a repository.

    Args:
        repo_name (str): The name of the repository.
        org_name (str): The name of the organization.
        file_path (str): Path of the file in the repo.
        file_content (str): The updated content of the file.
        commit_message (str): Commit message for the update.
        token (str): GitHub token for authentication.
        sha (str): The SHA of the file to be updated.
    """
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/contents/{file_path}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'message': commit_message,
        'content': base64.b64encode(file_content.encode('utf-8')).decode('utf-8'),
        'sha': sha,
        'branch': 'main'
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logging.info(f"File {file_path} updated in {repo_name} successfully.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Failed to update file {file_path} in {repo_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Update a file in a repository.")
    parser.add_argument('repo_name', type=str, help="Name of the repository.")
    parser.add_argument('org_name', type=str, help="Name of the organization.")
    parser.add_argument('file_path', type=str, help="Path of the file in the repository.")
    parser.add_argument('file_content', type=str, help="Updated content of the file.")
    parser.add_argument('commit_message', type=str, help="Commit message for the update.")
    parser.add_argument('token', type=str, help="GitHub token for authentication.")
    parser.add_argument('sha', type=str, help="SHA of the file to update.")
    
    args = parser.parse_args()
    update_file_in_repo(args.repo_name, args.org_name, args.file_path, args.file_content, args.commit_message, args.token, args.sha)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
