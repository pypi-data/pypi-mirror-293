# README Generator

A simple Python package to generate README files for projects automatically.

## Features

- Automatically generates README files with customizable content.

## Installation

```bash
pip install readme_gen
```

## Usage

```python
from readme_gen import generate_readme

generate_readme(
    project_name="My Awesome Project",
    description="This project is awesome because...",
    installation_instructions="pip install -r requirements.txt",
    usage_instructions="python main.py",
    license_info="MIT License"
)
```

## License

MIT License
