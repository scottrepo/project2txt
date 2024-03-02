# Imports
import argparse
import json
import os
import re

# Configuration Defaults
DEFAULT_CONFIG = {
    "exclude_patterns": [".git", "__pycache__", "node_modules"],
    "comment_patterns": {
        ".py": "#",
        ".js": "//",
        ".tsx": "//",
        # More patterns can be added here for different languages
    },
    "output_format": {
        "delimiter": "\n<<<FILENAME:{file_path}>>>\n"
    }
}


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
    """Process individual files: filter, remove comments, and write to output."""
    if should_exclude_file(file_path, config["exclude_patterns"]):
        return  # File is excluded based on the config

    file_extension = os.path.splitext(file_path)[1]
    comment_pattern = config["comment_patterns"].get(file_extension)

    with open(file_path, 'r') as file:
        file_content = file.read()
        if comment_pattern:
            file_content = remove_comments(file_content, comment_pattern)

    file_content = os.linesep.join([s for s in file_content.splitlines() if s.strip()])
    with open(output_file, 'a') as out_file:
        delimiter = config["output_format"]["delimiter"].format(file_path=file_path)
        out_file.write(delimiter + file_content + "\n")


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
