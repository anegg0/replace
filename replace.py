import re
import json
import sys
from pathlib import Path
import argparse

def load_json():
    script_dir = Path(__file__).parent
    json_path = script_dir / "expressions.json"
    with open(json_path, 'r') as file:
        return json.load(file)

def load_markdown(filename):
    with open(filename, 'r') as file:
        return file.read()

def save_markdown(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def reformat_content(content, expressions):
    replacements = []

    for expression in expressions:
        original_format = expression.get("original_format")
        correct_format = expression.get("correct_format")

        if original_format and correct_format:
            original_pattern = re.compile(original_format)

            def replacer(match):
                matched_text = match.group(0)
                # Use string comparison instead of regex for correct_format
                if matched_text != correct_format.strip('`'):
                    replacements.append((matched_text, f"`{matched_text}`"))
                    return f"`{matched_text}`"
                return matched_text

            content = original_pattern.sub(replacer, content)

    return content, replacements

def main():
    parser = argparse.ArgumentParser(description="Reformat Markdown content based on expressions from a hardcoded JSON file.")
    parser.add_argument("markdown_file", help="The path to the Markdown file to be reformatted.")
    args = parser.parse_args()

    expressions = load_json()
    content = load_markdown(args.markdown_file)

    updated_content, replacements = reformat_content(content, expressions)

    output_file = Path(args.markdown_file).stem + "_reformatted.md"
    save_markdown(output_file, updated_content)
    print(f"Reformatted content saved to {output_file}")

    if replacements:
        print("\nReport of Matching Expressions:")
        for original, replacement in replacements:
            print(f"Matched: {original} -> Replaced with: {replacement}")
    else:
        print("\nNo matching expressions found.")

if __name__ == "__main__":
    main()
