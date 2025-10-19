# Contributing to Office Document Text Extractor

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Sample document (if possible)

### Suggesting Features

Feature requests are welcome! Please:

- Check existing issues first
- Describe the use case
- Explain why it would be useful
- Provide examples if possible

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/praveenc/office-doc-extractor.git
   cd office-doc-extractor
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation

4. **Test your changes**
   ```bash
   python -m pytest tests/
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

## Development Setup

### Prerequisites

- Python 3.12+
- Pandoc
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/office-doc-extractor.git
cd office-doc-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Pandoc
brew install pandoc  # macOS
sudo apt-get install pandoc  # Ubuntu
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_all_features.py

# Run with coverage
python -m pytest --cov=office_doc_extractor tests/
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small

### Example

```python
def extract_text(self, input_path: str) -> str:
    """
    Extract text from document.

    Args:
        input_path: Path to document file

    Returns:
        Extracted text as string

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If format not supported
    """
    # Implementation
```

### Formatting

Use `black` for code formatting:

```bash
pip install black
black office_doc_extractor.py
```

### Linting

Use `ruff` for linting:

```bash
pip install ruff
ruff check office_doc_extractor.py
```

## Testing Guidelines

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange
    converter = DocumentConverter()

    # Act
    result = converter.extract_text('test.docx')

    # Assert
    assert len(result) > 0
    assert 'expected text' in result
```

### Test Coverage

- Add tests for new features
- Test edge cases
- Test error handling
- Aim for >80% coverage

## Documentation

### Update Documentation

When adding features:

1. Update README.md
2. Update QUICK_START.md
3. Add docstrings
4. Update CHANGELOG.md

### Documentation Style

- Use clear, concise language
- Provide code examples
- Include use cases
- Add troubleshooting tips

## Commit Messages

### Format

```
type: brief description

Detailed explanation (optional)

Fixes #issue_number (if applicable)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Examples

```
feat: add support for ODP files

Add OpenDocument Presentation format support using python-odp library.

Fixes #42
```

```
fix: handle empty Excel sheets

Prevent crash when processing Excel files with empty sheets.
```

## Release Process

1. Update version in `__version__`
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. Create GitHub release

## Questions?

- Open an issue for questions
- Join discussions
- Check existing documentation

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
