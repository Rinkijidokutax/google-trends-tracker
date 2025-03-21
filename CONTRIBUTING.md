# Contributing to Google Trends Tracker

Thank you for considering contributing to the Google Trends Tracker project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate when interacting with other contributors. We aim to maintain a welcoming environment for everyone.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- Use the bug report template if available
- Include detailed steps to reproduce the bug
- Include any error messages or logs
- Specify your operating system and Python version

### Suggesting Enhancements

- Check if the enhancement has already been suggested
- Provide a clear description of the feature
- Explain why this enhancement would be useful
- Consider how it would integrate with existing functionality

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests if available
5. Commit your changes with clear commit messages
6. Push to your branch
7. Submit a pull request

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/google-trends-tracker.git
cd google-trends-tracker
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Create necessary directories
```bash
mkdir -p output logs
```

## Style Guide

- Follow PEP 8 coding standards
- Use docstrings to document functions and classes
- Keep functions small and focused on a single task
- Use meaningful variable and function names

## Testing

When adding new features, please include appropriate tests. Run existing tests to ensure your changes don't break existing functionality.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
