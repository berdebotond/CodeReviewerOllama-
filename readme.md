## Project Description
This project provides a robust set of tools for retrieving and analyzing code from GitHub repositories. It utilizes a modular architecture to fetch code, summarize it, and potentially identify areas for improvement or bugs, integrating the ollama AI for automated code reviews.

## Features
### Code Fetching: 
Clones a GitHub repository and reads files, excluding binaries, to parse and store code.
### Code Analysis: 
Leverages an AI model (ollama) to generate summaries and analyses of the fetched code.
### Test Coverage: 
Includes tests for handling errors, integration with real repositories, and ensuring non-code files are skipped.
### Modules
#### Code Reader: Clones and reads code from GitHub repositories.
#### Ollama Client: Communicates with the ollama AI to analyze code and provide feedback.
#### Configuration: Manages application configurations and settings.
## Installation
Clone the repository
Install the dependencies
```
pip install -r requirements.txt
```
Ensure you have bash available for running scripts (especially on non-Unix systems).


```bash
pytest
```

## Configuration
Modify the app_config.py to change settings like the AI model used for code analysis.

## Contributing
Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.