# Project2txt - Project Code Aggregator

Project2txt `main.py` is a Python script designed to aggregate all the source code files from a specified project into a single text file. This file is optimized for training or using as input into Large Language Models (LLMs) like ChatGPT. The script intelligently filters out non-source code files, removes comments, and formats the output to preserve the original structure and logic of the project code.

## Features

- **Auto-Detection of Source Code**: Automatically includes common source code files while excluding non-essential files (like `.md`, `.csv`, `.pdf`, etc.).
- **Comment Removal**: Strips line comments from the code to ensure clean, readable output.
- **Customizable Filtering**: Allows for custom configuration to include or exclude specific file types or directories.
- **Interactive Mode**: Offers an interactive mode for easy setup without the need to manually edit configuration files.
- **Logging**: Detailed logging of the script's operations, including files processed, skipped, and any errors encountered.

## Prerequisites

Before you begin, ensure you have the latest version of Python installed on your system. This script is compatible with Python 3.6 and above.

## Installation

1. **Clone the Repository**: First, clone this repository to your local machine using:

   ```
   git clone https://your-repository-url.git
   ```

2. **Navigate to the Script Directory**: Change into the cloned directory.

   ```
   cd path/to/main.py
   ```

3. **(Optional) Virtual Environment**: It's a good practice to run Python projects in a virtual environment. Create and activate one with:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. **Install Dependencies**: This script uses the standard Python library, so no additional installations are required.

## Usage

You can run `main.py` using the command line. The script offers both standard and interactive modes for flexibility.

### Standard Mode

Run the script with the required parameters:

```
python main.py --project_path "/path/to/your/project" --output_dir "/path/to/output/directory"
```

### Interactive Mode

If you run the script without any arguments, it will enter interactive mode, guiding you through the necessary inputs:

```
python main.py
```

Follow the on-screen prompts to specify the project path and output directory.

### Configuration

The script uses a `config.json` file for custom configurations. In interactive mode, you'll be guided to create or modify this file. Alternatively, you can manually edit or create this file in the script's directory.

Example `config.json` structure:

```json
{
  "include_patterns": ["\\.py$", "\\.js$"],
  "exclude_patterns": ["\\.git", "__pycache__"],
  "comment_patterns": {
    ".py": "#",
    ".js": "//"
  },
  "output_format": {
    "delimiter": "\n<<<FILENAME:{file_path}>>>\n"
  }
}
```

### Logs

The script generates a logs to the console, logging detailed information about its execution. Consult this log for troubleshooting or to review the script's actions.

## Contributing

Contributions to improve `Python2txt` are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under [MIT License](LICENSE). Feel free to use, modify, and distribute the code as you see fit.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.
