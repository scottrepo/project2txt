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


def create_output_directory(base_output_dir, project_name):
    """Create an output directory for the project if it doesn't already exist."""
    output_dir_path = os.path.join(base_output_dir, f"{project_name}_combined_output")
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    return output_dir_path


def get_project_name_from_path(project_path):
    """Extract the project name from the provided project path."""
    return os.path.basename(os.path.normpath(project_path))


def process_project(project_path, base_output_dir, config):
    project_name = get_project_name_from_path(project_path)
    output_dir = create_output_directory(base_output_dir, project_name)
    output_file_path = os.path.join(output_dir, f"{project_name}.txt")

    # Ensure the output file is empty before starting
    open(output_file_path, 'w').close()

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, config, output_file_path)

    print(f"Project processing complete. Output saved to {output_file_path}")


def generate_config_interactively():
    print("Interactive Configuration Generator")
    config = {
        "include_patterns": [],
        "exclude_patterns": [],
        "comment_patterns": {},
        "output_format": {"delimiter": "\n<<<FILENAME:{file_path}>>>\n"}
    }

    # Example: Adding patterns interactively
    while True:
        pattern = input("Enter a file extension to include (e.g., .py) or 'done' to finish: ")
        if pattern.lower() == 'done':
            break
        comment = input(f"Enter the comment symbol for {pattern} (e.g., #): ")
        config["include_patterns"].append(pattern + "$")  # Ensuring it's treated as an extension
        config["comment_patterns"][pattern] = comment

    # Extend this to other configuration options as needed
    return config


def check_for_interactive_mode(args):
    # Assume interactive mode if all arguments are None (indicating they were not provided)
    return all(value is None for value in vars(args).values())


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process project files into a single text file for LLM training.")
    parser.add_argument("--project_path", help="Path to the project directory", nargs='?', const='', default=None)
    parser.add_argument("--output_dir", help="Directory to save the output file", nargs='?', const='', default=None)
    parser.add_argument("--config", help="Path to configuration file", nargs='?', const='', default="config.json")
    return parser.parse_args()


def main():
    args = parse_arguments()
    # Determine if the script is in interactive mode based on the presence of arguments
    interactive_mode = args.project_path is None and args.output_dir is None

    if interactive_mode:
        print("Entering interactive mode...")
        # Interactive prompts for project path and output directory
        args.project_path = input("Enter the path to your project: ").strip() or '.'
        default_output_dir = os.path.join("output",
                                          os.path.basename(os.path.normpath(args.project_path)) + "_combined_output")
        args.output_dir = input(f"Enter the output directory [{default_output_dir}]: ").strip() or default_output_dir

        # Ensuring the output directory exists
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        # Interactive Configuration Choice
        use_default_config = input(
            "Press 'D' to use the default configuration, or any other key to customize: ").lower() == 'd'
        if use_default_config:
            config = DEFAULT_CONFIG
            print("Using default configuration.")
        else:
            config = generate_config_interactively()
            # Optionally save the generated config to a file
            with open(args.config, 'w') as config_file:
                json.dump(config, config_file, indent=4)
    else:
        # Non-interactive mode configuration loading
        if os.path.exists(args.config):
            config = load_config(args.config)
        else:
            config = DEFAULT_CONFIG

    # Proceed with processing using the determined or default configuration
    output_file_name = os.path.basename(os.path.normpath(args.project_path)) + ".txt"
    output_file_path = os.path.join(args.output_dir, output_file_name)

    process_project(args.project_path, output_file_path, config)

    print(f"Project processing complete. Output saved to {output_file_path}")


if __name__ == "__main__":
    main()
