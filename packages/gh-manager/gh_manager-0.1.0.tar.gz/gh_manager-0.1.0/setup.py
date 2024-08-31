from setuptools import setup, find_packages

setup(
    name='gh_manager',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0',  # Add other dependencies here if needed
    ],
    entry_points={
        'console_scripts': [
            # Define command-line scripts if needed, e.g., 'delete-repo=gh_manager.delete_repo:main'
            'delete-repo=gh_manager.delete_repo:main',
            'add-user=gh_manager.org_username_add:main',
            'add-file=gh_manager.repo_file_add:main',
            'update-file=gh_manager.repo_file_update:main',
            'github-token=gh_manager.github_token_manager:main',
        ],
    },
    author='Greg Chism',
    author_email='gchism@arizona.edu',
    description='A versatile toolkit for managing GitHub repositories, users, and personal access tokens.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/gh_manager',  # Update with your actual GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    include_package_data=True,  # If you have additional files to include in the package
)