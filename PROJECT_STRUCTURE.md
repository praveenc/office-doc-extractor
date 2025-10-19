# Project Structure

```bash
office-doc-extractor/
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history
├── PROJECT_STRUCTURE.md           # This file
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
│
├── office_doc_extractor.py        # Main extraction script
├── textract_extractor.py          # AWS Textract integration (optional)
│
├── docs/                          # Detailed documentation
│   ├── AMZN_TEXTRACT_PYTHON.md   # Textract reference
│   ├── PYPANDOC_HOWTO.md          # Pypandoc guide
│   ├── TEXT_EXTRACTION_STRATEGY.md # Strategy guide
│   └── PYTHON_LIBRARY_COMPARISON.md # Library comparison
│
├── examples/                      # Example scripts
│   ├── llm_tool_example.py        # LLM function calling
│   ├── lambda_handler.py          # AWS Lambda deployment
│   └── batch_processing.py        # Batch processing
│
└── tests/                         # Test suite
    ├── README.md                  # Test documentation
    ├── test_all_features.py       # Comprehensive tests (recommended)
    ├── test_converter.py          # Basic conversion tests
    └── test_converter_final.py    # Integration tests
```

## Core Files

### office_doc_extractor.py

Main extraction script with `DocumentConverter` class.

**Key Features**:

- Extract text from PDF, DOCX, XLSX, PPTX, HTML
- Organized output directories
- Command-line interface
- Python API

**Usage**:
```bash
ur run office_doc_extractor.py document.docx --extract-text
```

### textract_extractor.py

AWS Textract integration for scanned documents (optional).

**Key Features**:

- OCR for scanned PDFs and images
- Confidence score filtering
- AWS integration

**Usage**:
```bash
python textract_extractor.py scanned.pdf
```

## Documentation

### README.md

Main project documentation covering:

- Problem statement
- Installation
- Usage examples
- API reference
- AWS Lambda deployment
- Performance benchmarks

### QUICK_START.md

5-minute quick start guide with:

- Installation steps
- Basic usage
- Common use cases
- Troubleshooting

### CONTRIBUTING.md

Guidelines for contributors:

- How to contribute
- Development setup
- Code style
- Testing guidelines

### CHANGELOG.md

Version history and release notes.

## Examples

### llm_tool_example.py

Shows how to use the extractor as an LLM tool/function.

**Demonstrates**:

- OpenAI function calling integration
- Function definition format
- Error handling

### lambda_handler.py

AWS Lambda deployment example.

**Demonstrates**:

- Lambda handler implementation
- Base64 document encoding
- Error handling
- Response format

### batch_processing.py

Batch document processing script.

**Demonstrates**:

- Directory processing
- Metadata generation
- Progress reporting
- Error handling

## Output Structure

When running the extractor, files are organized as:

```
output/
├── text/                          # Extracted text files
│   ├── document1.txt
│   ├── document2.txt
│   └── spreadsheet.txt
│
└── converted_pdfs/                # PDF conversions (optional)
    ├── document1.pdf
    └── document2.pdf
```

## Dependencies

### Python Packages

- **pypandoc** (>= 1.13): Document conversion
- **pandas** (>= 2.0.0): Excel processing
- **openpyxl** (>= 3.0.0): Excel file support
- **python-pptx** (>= 0.6.0): PowerPoint processing
- **loguru** (>= 0.7.0): Logging
- **boto3** (>= 1.26.0): AWS integration (optional)

### System Dependencies

- **Pandoc**: Universal document converter (required)
- **LaTeX**: PDF generation (optional, not needed for text extraction)

## Testing

### Test Suite

The `tests/` directory contains comprehensive test scripts. See [tests/README.md](tests/README.md) for detailed documentation.

**Quick test**:
```bash
# Comprehensive test (recommended)
python tests/test_all_features.py

# Basic functionality test
python tests/test_converter_final.py
```

### Test Files

- **test_all_features.py**: Comprehensive test suite (recommended)
- **test_converter_final.py**: Integration tests
- **test_converter.py**: Basic conversion tests

See [tests/README.md](tests/README.md) for detailed test documentation.

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/office-doc-extractor.git
cd office-doc-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Pandoc
brew install pandoc  # macOS
```

### Running Tests

```bash
# Run comprehensive tests
python tests/test_all_features.py

# Run specific test
python tests/test_converter_final.py

# Run example scripts
python examples/batch_processing.py sample_docs/
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions focused

## Deployment

### Local Deployment

```bash
# Install and run
pip install -r requirements.txt
python office_doc_extractor.py document.docx --extract-text
```

### Docker Deployment

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y pandoc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY office_doc_extractor.py .
CMD ["python", "office_doc_extractor.py"]
```

### AWS Lambda Deployment

See `examples/lambda_handler.py` and README.md for detailed instructions.

## Support

- 📖 Documentation: `docs/`
- 💡 Examples: `examples/`
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## License

MIT License - see LICENSE file for details.
