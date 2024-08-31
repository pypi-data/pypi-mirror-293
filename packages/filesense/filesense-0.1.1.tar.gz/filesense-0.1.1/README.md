# FileSense

filesense is a Python package that generates new, descriptive names for text, PDF, DOCX, PowerPoint, and image files using Generative AI.

## Features

- Supports text, PDF, DOCX, PowerPoint, and image files.
- Automatically generates new names based on file content.
- Generative AI technique for title generation.
- renames files , preserving the original content.

## Installation

To install FileRenamer, use pip:

```bash
pip install filesense
```
# Usage
Here's how to use FileRenamer in your project:
```
from filesense import FileRenamer

# Initialize the FileRenamer
renamer = FileRenamer()

# Specify the file path and destination path
file_path = 'path/to/your/file.pdf'
dest_path = './renamed_files/'

# Rename the file
renamer.rename_file(file_path, dest_path)
```


# Contact
For any questions or inquiries, please contact mayurdabade1103@gmail.com.
