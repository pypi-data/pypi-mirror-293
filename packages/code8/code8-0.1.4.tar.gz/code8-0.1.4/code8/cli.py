import sys
import argparse
from code8.test_generator import generate_tests
from code8.config_ui import run_config_ui

def main():
    parser = argparse.ArgumentParser(description="Generate unit tests for Python files and more, or configure settings.")
    parser.add_argument('file', nargs='?', help="The Python file to generate tests for")

    args = parser.parse_args()

    if args.file:
        generate_tests(args.file)
    else:
        run_config_ui()

if __name__ == "__main__":
    main()