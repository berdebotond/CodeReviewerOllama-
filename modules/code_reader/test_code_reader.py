import subprocess

import pytest
from unittest.mock import patch, mock_open
from code_reader import CodeReader  # Ensure the module name is correct


def test_integration_with_real_repository():
    """
    Integration test to verify that the CodeReader can successfully clone and read from a real GitHub repository.
    """
    # URL of the repository you want to test with
    test_github_url = 'https://github.com/berdebotond/GoCineAPI'  # Use a lightweight repo for testing

    try:
        # Initialize the CodeReader with the test GitHub URL
        code_reader = CodeReader(test_github_url)

        # Assert that some expected file (example: 'README.md') is in the cloned code
        assert '.gitignore' in code_reader.code, "README.md should be in the code dictionary"

        # Optionally, check the content of a file or that multiple expected files are present
        # assert 'some_file.py' in code_reader.code, "Expected Python file should be present"

        # Add any additional checks here, like inspecting file contents:
        # expected_content_snippet = "def hello_world():"
        # assert expected_content_snippet in code_reader.code['some_file.py'], "File content is not as expected"

    finally:
        # Cleanup to ensure that the temporary directory is removed after the test
        del code_reader

def test_clone_failure_raises_runtime_error():
    """
    Test that a RuntimeError is raised if the repository cannot be cloned.
    """
    with patch('tempfile.mkdtemp', return_value='/fake/tmpdir'), \
            patch('subprocess.check_call', side_effect=subprocess.CalledProcessError(1, 'git')), \
            pytest.raises(RuntimeError) as exc_info:
        cr = CodeReader('https://github.com/invalid/repo')
    assert "Failed to clone the repository." in str(exc_info.value)


def test_read_code_skips_binary_files():
    """
    Test that binary files are skipped when reading code.
    """
    binary_data = bytes([0] * 1024)  # Simulate binary file with null bytes
    with patch('tempfile.mkdtemp', return_value='/fake/tmpdir'), \
            patch('subprocess.check_call'), \
            patch('os.walk') as mock_walk, \
            patch('builtins.open', mock_open(read_data=binary_data)):
        mock_walk.return_value = [('/fake/tmpdir', ('subdir',), ('binaryfile',))]
        cr = CodeReader('https://github.com/valid/repo')
        assert 'binaryfile' not in cr.code


def test_cleanup_on_del():
    """
    Test that the temporary directory is cleaned up upon object deletion.
    """
    with patch('tempfile.mkdtemp', return_value='/fake/tmpdir'), \
            patch('subprocess.check_call'), \
            patch('shutil.rmtree') as mock_rmtree:
        cr = CodeReader('https://github.com/valid/repo')
        del cr
        mock_rmtree.assert_called_once_with('/fake/tmpdir')


# Setup pytest to mock logger and test the log output.
def test_logging_errors_on_file_read():
    """
    Test logging of errors during file reading.
    """
    with patch('tempfile.mkdtemp', return_value='/fake/tmpdir'), \
            patch('subprocess.check_call'), \
            patch('os.walk') as mock_walk, \
            patch('builtins.open', mock_open()) as mock_file_open, \
            patch('loguru.logger.error') as mock_logger_error:
        mock_walk.return_value = [('/fake/tmpdir', ('subdir',), ('test.py',))]
        mock_file_open.side_effect = Exception("mocked error")
        cr = CodeReader('https://github.com/valid/repo')
        mock_logger_error.assert_called_with("Error reading test.py: mocked error")
