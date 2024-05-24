import re
import sys
from pathlib import Path
import argparse

# Hardcoded JSON data
expressions = [
    {
        "name": "CamelCase",
        "original_format": r"(?<=\s)([a-z]+[a-zA-Z]*[A-Z][a-zA-Z]*)(?=\s)",
        "correct_format": r"`\1`"
    },
    {
        "name": "PascalCase",
        "original_format": r"(?<=\s)([A-Z][a-z]*[A-Z][a-zA-Z]*)(?=\s)",
        "correct_format": r"`\1`"
    }
]

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
                # Check if the matched text is already surrounded by backticks
                before = content[match.start() - 1] if match.start() > 0 else ""
                after = content[match.end()] if match.end() < len(content) else ""
                # Check if the matched text is the first word of a sentence
                if before != '`' and after != '`' and not before.isalnum():
                    replacements.append((matched_text, f"`{matched_text}`"))
                    return f"`{matched_text}`"
                return matched_text

            content = original_pattern.sub(replacer, content)

    return content, replacements

def main():
    parser = argparse.ArgumentParser(description="Reformat Markdown content based on hardcoded expressions.")
    parser.add_argument("markdown_file", help="The path to the Markdown file to be reformatted.")
    args = parser.parse_args()

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
