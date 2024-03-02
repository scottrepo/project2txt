# Imports
import argparse
import json
import os
import re

# Updated default configuration with include patterns for source code files
DEFAULT_CONFIG = {
    "include_patterns": [r"\.py$", r"\.js$", r"\.tsx$", r"\.java$", r"\.cpp$", r"\.c$", r"\.h$", r"\.cs$", r"\.php$",
                         r"\.rb$", r"\.go$"],  # Add more as needed
    "exclude_patterns": [r"\.git", r"__pycache__", r"\.md$", r"\.csv$", r"\.pdf$", r"venv"],
    # Explicitly exclude certain patterns
    "comment_patterns": {
        ".py": "#",
        ".js": "//",
        ".tsx": "//"
        # Extend this based on the languages you want to support
    },
    "output_format": {
        "delimiter": "\n<<<FILENAME:{file_path}>>>\n"
    }
}


# Utility functions and core functions go here

def should_process_file(file_path, config):
    """Determine if the file should be processed based on include and exclude patterns."""
    # Check for explicit exclusion first
    for pattern in config["exclude_patterns"]:
        if re.search(pattern, file_path):
            return False
    # Then check for inclusion (source code files)
    for pattern in config["include_patterns"]:
        if re.search(pattern, file_path):
            return True
    return False


# Utility Functions
def load_config(config_path):
    """Load configuration from a file or return default configuration."""
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}. Using default settings.")
        return DEFAULT_CONFIG


def should_exclude_file(file_path, exclude_patterns):
    """Determine if a file should be excluded based on pattern matching."""
    return any(re.search(pattern, file_path) for pattern in exclude_patterns)


def remove_comments(file_content, comment_pattern):
    """Remove single-line comments from file content."""
    clean_content = re.sub(f"{comment_pattern}.*", "", file_content)
    # Extend here for block comments or other language specifics
    return clean_content


# Core Functions
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process project files into a single text file for LLM training.")
    parser.add_argument("project_path", help="Path to the project directory")
    parser.add_argument("--output_dir", help="Directory to save the output file", default="output")
    parser.add_argument("--config", help="Path to configuration file", default="config.json")
    return parser.parse_args()


def process_file(file_path, config, output_file):
    # Check if the file should be processed based on inclusion and exclusion patterns
    if not should_process_file(file_path, config):
        print(f"Skipping {file_path}")
        return  # Skip processing for this file

    file_extension = os.path.splitext(file_path)[1]
    comment_pattern = config["comment_patterns"].get(file_extension)

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

            # Remove comments if a comment pattern is defined for the file extension
            if comment_pattern:
                # This is a simplistic approach; more complex logic might be needed for block comments, etc.
                clean_content = re.sub(f"{comment_pattern}.*", "", file_content)

                # Remove trailing whitespace and blank lines
                clean_content = os.linesep.join([s for s in clean_content.splitlines() if s.strip()])
            else:
                # If no comment pattern, just trim whitespace and blank lines
                clean_content = os.linesep.join([s for s in file_content.splitlines() if s.strip()])

        # Write the processed content to the output file with the custom delimiter
        with open(output_file, 'a') as out_file:
            delimiter = config["output_format"]["delimiter"].format(file_path=file_path)
            out_file.write(delimiter + clean_content + "\n")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def process_project(project_path, output_dir, config):
    """Walk through the project directory and process each file."""
    output_file = os.path.join(output_dir, "project_combined.txt")
    open(output_file, 'w').close()  # Clearing the output file before starting

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, config, output_file)

    print(f"Project processing complete. Output saved to {output_file}")


def main():
    """Main function to execute script logic."""
    args = parse_arguments()
    config = load_config(args.config)

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    process_project(args.project_path, args.output_dir, config)


if __name__ == "__main__":
    main()
