import os
import shutil
import subprocess
from getpass import getpass
from pathlib import Path

def publish_to_pypi(api_token):
    """
    Automates the process of publishing a Python package to PyPI.

    Args:
        api_token (str): The PyPI API token for authentication.

    Raises:
        subprocess.CalledProcessError: If any of the subprocess commands fail.
    """
    # Clean up any existing build artifacts
    for dir_name in ["build", "dist", "*.egg-info"]:
        for path in Path.cwd().glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    # Build the distribution
    subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)

    # Authenticate with PyPI
    subprocess.run(["twine", "upload", "--repository-url", "https://upload.pypi.org/legacy/", "--username", "__token__", "--password", api_token, "dist/*"], check=True)

    print("Package published successfully!")

if __name__ == "__main__":
    api_token = getpass("Enter your PyPI API token: ")
    publish_to_pypi(api_token)