#!/usr/bin/env python3

import sys
import os
from markdown import markdown
from rich.console import Console
from rich.markdown import Markdown

def preview_markdown(file_path):
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    md_content = Markdown(content)
    console = Console()
    console.print(md_content)

def main():
    if len(sys.argv) < 2:
        print("Usage: mdm <path_to_markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    preview_markdown(file_path)

if __name__ == "__main__":
    main()
