import os
import subprocess
import tempfile
import shutil

import loguru


class CodeReader:
    """
    A class for reading code from a GitHub repository.

    Attributes:
        github_url (str): The URL of the GitHub repository to clone.
        code (dict): A dictionary containing the code files and their content.

    Methods:
        __init__(self, github_url: str):
            Clones the specified GitHub repository into a temporary directory and initializes the code dictionary.

        _clone_repo(self):
            Clones the specified GitHub repository into a temporary directory using subprocess for safety.

        __read_code(self):
            Reads code from the temporary directory and its subfolders, filtering by file type, and stores it in the code dictionary.

        __del__(self):
            Deletes the contents of the temporary directory using shutil for safe deletion.
    """

    def __init__(self, github_url: str):
        """
        Initialize the CodeReader object.

        Parameters:
            github_url (str): The URL of the GitHub repository to clone.
        """
        self.github_url = github_url
        self.temp_dir = tempfile.mkdtemp()  # Securely creating a temporary directory
        self.code = {}
        self._clone_repo()
        self.__read_code()

    def _clone_repo(self):
        """
        Clones the specified GitHub repository into the temporary directory safely using subprocess.

        """
        try:
            subprocess.check_call(['git', 'clone', self.github_url, self.temp_dir])
        except subprocess.CalledProcessError as e:
            loguru.logger.error(f"Failed to clone repo: {e}")
            raise RuntimeError("Failed to clone the repository.")

    def __read_code(self):
        """
        Reads code from the temporary directory and its subfolders, filtering out binary files, and stores it in the code dictionary.
        """
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    # Open the file in binary mode to check if it's binary
                    with open(file_path, 'rb') as f:
                        initial_bytes = f.read(1024)  # Read the first 1024 bytes of the file
                    # Check if the file has null byte, which is typical for binary files
                    if b'\0' not in initial_bytes:
                        # If no null byte, read as text file
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.code[file] = f.read()
                except Exception as e:
                    # Handling potential errors like reading a binary file as text
                    loguru.logger.error(f"Error reading {file}: {e}")

    def __del__(self):
        """
        Deletes the contents of the temporary directory safely using shutil.

        """
        shutil.rmtree(self.temp_dir)


