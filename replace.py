import re
import json
import sys
from pathlib import Path

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def load_markdown(filename):
    with open(filename, 'r') as file:
        return file.read()

def save_markdown(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def reformat_content(content, expressions):
    original_format = expressions.get("original_format")
    correct_format = expressions.get("correct_format")

    original_pattern = re.compile(original_format)
    correct_pattern = re.compile(correct_format)

    replacements = []

    def replacer(match):
        matched_text = match.group(0)
        if not correct_pattern.match(matched_text):
            replacements.append((matched_text, f"`{matched_text}`"))
            return f"`{matched_text}`"
        return matched_text

    updated_content = original_pattern.sub(replacer, content)
    return updated_content, replacements

def main(markdown_file, json_file):
    expressions = load_json(json_file)
    content = load_markdown(markdown_file)

    updated_content, replacements = reformat_content(content, expressions)

    output_file = Path(markdown_file).stem + "_reformatted.md"
    save_markdown(output_file, updated_content)
    print(f"Reformatted content saved to {output_file}")

    if replacements:
        print("\nReport of Matching Expressions:")
        for original, replacement in replacements:
            print(f"Matched: {original} -> Replaced with: {replacement}")
    else:
        print("\nNo matching expressions found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <markdown_file> <json_file>")
    else:
        markdown_file = sys.argv[1]
        json_file = sys.argv[2]
        main(markdown_file, json_file)