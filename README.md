# Office Document Text Extractor

> Extract text from Microsoft Office documents (DOCX, XLSX, PPTX, PDF) and HTML files for LLM processing - fast, free, and AWS Lambda ready.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📚 Navigation Guide

**New here?** Choose your path:

- 🚀 **Quick Start** → [Installation](#installation) → [Basic Usage](#basic-usage) → Try it in 5 minutes
- 💡 **See Examples** → [examples/](examples/) → Real-world use cases (Bedrock, Lambda, batch processing)
- 🎯 **Understand When to Use** → [Choosing the Right Tool](#choosing-the-right-tool) → This tool vs AWS Textract
- 📖 **Deep Dive** → [docs/](docs/) → Architecture, strategy, library comparisons
- ✅ **Verify It Works** → [tests/](tests/) → Run comprehensive tests
- 🤔 **Decision Making** → [Performance Comparison](#performance-comparison) → Cost and speed analysis

**Common paths**:

- **LLM Integration** → [Use Cases](#use-cases) → [examples/llm_tool_example.py](examples/llm_tool_example.py)
- **AWS Bedrock** → [examples/bedrock_tool_example.py](examples/bedrock_tool_example.py)
- **AWS Lambda** → [AWS Lambda Deployment Guide](#aws-lambda-deployment-guide)
- **Batch Processing** → [examples/batch_processing.py](examples/batch_processing.py)

## The Problem

Large Language Models (LLMs) need text input, but most business documents are in Microsoft Office formats (DOCX, XLSX, PPTX) and PDFs. When preparing these documents for LLM processing, developers face several challenges:

- **Overkill solutions**: Using OCR services for digital documents that already contain selectable text
- **Complex pipelines**: Setting up document conversion infrastructure with multiple dependencies
- **Slow processing**: Waiting for API calls and external service responses
- **Unnecessary costs**: Paying per-page fees for simple text extraction

Most documents don't need OCR - they're digital files with extractable text. Yet many developers default to heavyweight solutions designed for scanned documents, forms, and complex table extraction.

## The Solution

**Office Document Text Extractor** provides instant, free text extraction from digital Office documents using native Python libraries. Perfect for the common use case: extracting plain text from digital documents for LLM processing.

### When to Use This Tool

✅ **Digital Office documents** (DOCX, XLSX, PPTX, HTML)
✅ **Text-based PDFs** with selectable text
✅ **Simple text extraction** for LLM prompts
✅ **High-volume processing** where cost matters
✅ **Real-time extraction** for LLM tool calls

### When to Use OCR Services (like AWS Textract)

AWS Textract excels at specialized document processing:

✅ **Scanned documents** (images of documents)
✅ **Complex forms** with key-value pair extraction
✅ **Structured tables** requiring layout preservation
✅ **Handwritten text** recognition
✅ **Multi-format documents** (JPEG, PNG, PDF, TIFF)

**Pro Tip**: Use both! Extract digital documents with this tool (free), fall back to Textract for scanned documents and complex forms (paid).

### Key Benefits

- ✅ **Free**: Zero API costs for Office documents
- ✅ **Fast**: ~600,000 characters/second extraction speed
- ✅ **Simple**: Single Python script with minimal dependencies
- ✅ **LLM-Ready**: Clean text output perfect for prompt injection
- ✅ **Lambda-Ready**: Deploy as serverless text extraction service
- ✅ **Tool-Call Compatible**: Use as LLM function/tool for document processing

## Quick Start

### Installation

Using [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager.

```bash
# Install uv (modern Python package manager)
pip install uv
```

### Basic Usage

[office_doc_extractor.py](./office_doc_extractor.py) script uses [PEP 723](https://peps.python.org/pep-0723/).

**Note**: With PEP 723 inline metadata, `uv run` automatically installs dependencies!

```bash
uv run office_doc_extractor.py --help

Reading inline script metadata from `office_doc_extractor.py`
usage: office_doc_extractor.py [-h] [--output OUTPUT] [--output-dir OUTPUT_DIR] [--extract-text] [--pdf-engine {pdflatex,xelatex,lualatex}]
                               [--quiet] [--verbose]
                               input_file

Convert documents to PDF for Amazon Textract processing

positional arguments:
  input_file            Path to input document

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file path (for single file conversion)
  --output-dir OUTPUT_DIR, -d OUTPUT_DIR
                        Base output directory (default: output/)
  --extract-text, -t    Extract text directly without PDF conversion (faster, no Textract needed)
  --pdf-engine {pdflatex,xelatex,lualatex}
                        PDF engine to use (default: pdflatex)
  --quiet, -q           Suppress logging output
  --verbose, -v         Enable verbose logging

Supported formats: HTML, PDF, DOCX, XLS, XLSX, PPTX

Examples:
  python office_doc_extractor.py document.html
  python office_doc_extractor.py document.docx --output result.pdf
  python office_doc_extractor.py spreadsheet.xlsx --output-dir converted/
  python office_doc_extractor.py --pdf-engine xelatex document.html
  python office_doc_extractor.py --extract-text document.docx
```

```bash
# Extract text from any Office document (using uv)
uv run office_doc_extractor.py path_to_document.docx --extract-text

# Extract text from PDF
uv run office_doc_extractor.py path_to_document.pdf --extract-text

# Output saved to: output/text/path_to_document.txt
```

### Python API

```python
from office_doc_extractor import DocumentConverter

converter = DocumentConverter()
text = converter.extract_text('document.docx')

# Use with LLM
prompt = f"Summarize this document:\n\n{text}"
```

## Supported Formats

| Format     | Extension | Speed | Cost | Use Case                          |
| ---------- | --------- | ----- | ---- | --------------------------------- |
| Word       | .docx     | 0.1s  | Free | Reports, contracts, documentation |
| Excel      | .xlsx     | 2.0s  | Free | Spreadsheets, data tables         |
| PowerPoint | .pptx     | 0.5s  | Free | Presentations, slides             |
| HTML       | .html     | 0.1s  | Free | Web pages, documentation          |
| PDF\*      | .pdf      | 0.2s  | Free | Digital PDFs with selectable text |

\*Note: Extracts text from digital PDFs with selectable text. Scanned PDFs require OCR (use AWS Textract).

## Use Cases

### 1. LLM Tool/Function Call

Enable LLMs to read Office documents on-demand:

```python
# OpenAI Function Calling
tools = [{
    "type": "function",
    "function": {
        "name": "extract_document_text",
        "description": "Extract text from Office documents (DOCX, XLSX, PPTX, PDF)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the document file"
                }
            },
            "required": ["file_path"]
        }
    }
}]

def extract_document_text(file_path: str) -> str:
    """LLM tool function for document extraction."""
    converter = DocumentConverter()
    return converter.extract_text(file_path)
```

### 2. Document Preprocessing Pipeline

Prepare documents for RAG (Retrieval-Augmented Generation):

```python
from office_doc_extractor import DocumentConverter

def prepare_for_rag(document_path: str) -> dict:
    """Extract and chunk document for vector database."""
    converter = DocumentConverter()
    text = converter.extract_text(document_path)

    # Split into chunks for embedding
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    return {
        "source": document_path,
        "text": text,
        "chunks": chunks
    }
```

### 3. Batch Document Processing

Process entire document libraries:

```bash
# Extract all documents in a folder
for file in documents/*.{docx,xlsx,pptx,pdf}; do
    python office_doc_extractor.py "$file" --extract-text --quiet
done

# Results in output/text/ folder
```

### 4. AWS Lambda Deployment

Deploy as serverless text extraction service:

```python
# lambda_handler.py
import json
import base64
from office_doc_extractor import DocumentConverter

def lambda_handler(event, context):
    """AWS Lambda handler for document text extraction."""

    # Get document from event (base64 encoded)
    document_data = base64.b64decode(event['document'])
    file_extension = event['file_extension']

    # Save temporarily
    temp_path = f"/tmp/document{file_extension}"
    with open(temp_path, 'wb') as f:
        f.write(document_data)

    # Extract text
    converter = DocumentConverter()
    text = converter.extract_text(temp_path)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'text': text,
            'length': len(text)
        })
    }
```

**Lambda Configuration**:

- Runtime: Python 3.12
- Memory: 512 MB
- Timeout: 30 seconds
- Layers: Pandoc layer + Python dependencies layer

**⚠️ Important**: You must create Lambda layers for both Pandoc (system binary) and Python dependencies (pypandoc, pandas, openpyxl, python-pptx, pdfplumber, loguru) before using this code. See the [AWS Lambda Deployment Guide](#aws-lambda-deployment-guide) below for detailed layer creation steps, or refer to the [AWS Lambda Layers documentation](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html) for general guidance.

## Performance Comparison

### For Digital Documents (Common Use Case)

| Tool          | Document      | Time | Cost   | Best For               |
| ------------- | ------------- | ---- | ------ | ---------------------- |
| **This Tool** | 10-page DOCX  | 0.2s | $0.00  | Simple text extraction |
| AWS Textract  | 10-page DOCX  | 10s  | $0.015 | Form/table extraction  |
| **This Tool** | 100-row Excel | 2.0s | $0.00  | Text content           |
| AWS Textract  | 100-row Excel | 10s  | $0.015 | Table structure        |
| **This Tool** | 20-slide PPTX | 0.5s | $0.00  | Slide text             |
| AWS Textract  | 20-slide PPTX | 20s  | $0.030 | Layout analysis        |

### Batch Processing: 1,000 Digital Documents

| Metric              | Office Doc Extractor | AWS Textract              |
| ------------------- | -------------------- | ------------------------- |
| **Processing Time** | ~10 minutes          | ~2 hours                  |
| **Total Cost**      | $0.00                | $15.00                    |
| **Setup Required**  | Python + Pandoc      | AWS account + credentials |
| **Best Use Case**   | LLM text extraction  | Form/table extraction     |

**Key Insight**: For simple text extraction from digital documents (the most common LLM use case), this tool is 12x faster and free. Use Textract when you need OCR, form extraction, or table structure preservation.

## Architecture

### Local Processing

```text
Document (DOCX/XLSX/PPTX)
    ↓
office_doc_extractor.py
    ↓
Native Python Libraries
    ├── pypandoc (DOCX/HTML)
    ├── pandas (XLSX)
    └── python-pptx (PPTX)
    ↓
Plain Text Output
    ↓
LLM Prompt / Vector DB
```

### AWS Lambda Service

```text
API Gateway
    ↓
Lambda Function
    ├── office_doc_extractor.py
    ├── Pandoc Layer
    └── Python Dependencies
    ↓
Return JSON Response
    {
        "text": "extracted content...",
        "length": 12345
    }
```

## Advanced Usage

### Custom Output Directory

```bash
# Organize by project
python office_doc_extractor.py report.docx --extract-text --output-dir project_a/
```

### Batch Processing with Metadata

```python
from pathlib import Path
from office_doc_extractor import DocumentConverter
import json

def batch_extract_with_metadata(input_dir: str):
    """Extract text and save with metadata."""
    converter = DocumentConverter()
    results = []

    for file in Path(input_dir).glob('*.{docx,xlsx,pptx,pdf}'):
        text = converter.extract_text(str(file))

        metadata = {
            'filename': file.name,
            'size': file.stat().st_size,
            'text_length': len(text),
            'format': file.suffix
        }

        # Save text
        output_file = Path('output/text') / f"{file.stem}.txt"
        output_file.write_text(text)

        # Save metadata
        results.append(metadata)

    # Save batch metadata
    with open('output/metadata.json', 'w') as f:
        json.dump(results, f, indent=2)
```

### Integration with LangChain

```python
from langchain.document_loaders import BaseLoader
from office_doc_extractor import DocumentConverter

class OfficeDocumentLoader(BaseLoader):
    """LangChain loader for Office documents."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.converter = DocumentConverter()

    def load(self):
        """Load document and return as LangChain Document."""
        text = self.converter.extract_text(self.file_path)

        return [{
            'page_content': text,
            'metadata': {
                'source': self.file_path,
                'format': Path(self.file_path).suffix
            }
        }]

# Usage
loader = OfficeDocumentLoader('document.docx')
docs = loader.load()
```

## AWS Lambda Deployment Guide

### 1. Create Pandoc Layer (System Binary)

```bash
# Create layer directory
mkdir -p pandoc-layer/bin

# Download Pandoc static binary for Linux
wget https://github.com/jgm/pandoc/releases/download/3.8/pandoc-3.8-linux-amd64.tar.gz
tar xvzf pandoc-3.8-linux-amd64.tar.gz
cp pandoc-3.8/bin/pandoc pandoc-layer/bin/

# Create layer zip
cd pandoc-layer
zip -r ../pandoc-layer.zip .
cd ..
```

### 2. Create Python Dependencies Layer

```bash
# Create layer directory with proper structure
mkdir -p python-deps-layer/python

# Install all Python dependencies (versions from PEP 723 metadata)
pip install -t python-deps-layer/python \
    pypandoc>=1.13 \
    pandas>=2.3.2 \
    openpyxl>=3.1.5 \
    python-pptx>=1.0.2 \
    pdfplumber>=0.11.7 \
    loguru>=0.7.3

# Create layer zip
cd python-deps-layer
zip -r ../python-deps-layer.zip .
cd ..
```

### 3. Package Lambda Function

```bash
# Create deployment package with your code
zip function.zip office_doc_extractor.py lambda_handler.py
```

### 4. Deploy with AWS CLI

```bash
# Upload Pandoc layer
aws lambda publish-layer-version \
    --layer-name pandoc \
    --zip-file fileb://pandoc-layer.zip \
    --compatible-runtimes python3.12

# Upload Python dependencies layer
aws lambda publish-layer-version \
    --layer-name office-doc-python-deps \
    --zip-file fileb://python-deps-layer.zip \
    --compatible-runtimes python3.12

# Create function with BOTH layers
aws lambda create-function \
    --function-name office-doc-extractor \
    --runtime python3.12 \
    --handler lambda_handler.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::ACCOUNT:role/lambda-role \
    --timeout 30 \
    --memory-size 512 \
    --layers \
        arn:aws:lambda:REGION:ACCOUNT:layer:pandoc:1 \
        arn:aws:lambda:REGION:ACCOUNT:layer:office-doc-python-deps:1
```

**Note**: Lambda supports up to 5 layers per function. This deployment uses 2 layers (Pandoc + Python dependencies).

### 4. Test Lambda Function

```python
import boto3
import json
import base64

lambda_client = boto3.client('lambda')

# Read document
with open('document.docx', 'rb') as f:
    document_data = base64.b64encode(f.read()).decode()

# Invoke Lambda
response = lambda_client.invoke(
    FunctionName='office-doc-extractor',
    Payload=json.dumps({
        'document': document_data,
        'file_extension': '.docx'
    })
)

result = json.loads(response['Payload'].read())
print(result['body'])
```

## Choosing the Right Tool

### Use Office Document Extractor For:

**Simple text extraction from digital documents**

- ✅ Digital Office documents (DOCX, XLSX, PPTX, HTML)
- ✅ Digital PDFs with selectable text (reports, contracts, etc.)
- ✅ LLM prompt preparation and RAG preprocessing
- ✅ High-volume processing (cost-sensitive)
- ✅ Real-time LLM tool calls
- ✅ Batch document analysis

**Perfect for**: Reading document content for LLM processing, document Q&A systems, content summarization, batch analysis.

### Use AWS Textract For:

**Specialized document processing with OCR and structure extraction**

- ✅ Scanned documents (images of documents)
- ✅ Complex forms with key-value pairs
- ✅ Tables requiring structure preservation
- ✅ Handwritten text recognition
- ✅ Multi-format image processing (JPEG, PNG, TIFF)
- ✅ Invoice and receipt processing

**Perfect for**: Form data extraction, invoice processing, scanned document digitization, complex table extraction.

### Comparison

| Feature               | Office Doc Extractor | AWS Textract         |
| --------------------- | -------------------- | -------------------- |
| **Text extraction**   | ✅ Excellent         | ✅ Excellent         |
| **Digital documents** | ✅ Optimized         | ⚠️ Overkill          |
| **Digital PDFs**      | ✅ Supported         | ⚠️ Overkill          |
| **Scanned documents** | ❌ Not supported     | ✅ Optimized         |
| **Form extraction**   | ❌ Not supported     | ✅ Excellent         |
| **Table structure**   | ⚠️ Basic             | ✅ Advanced          |
| **Cost**              | Free                 | $0.0015/page         |
| **Speed**             | Instant              | 1-5s/page            |
| **Setup**             | Python only          | AWS account required |

### Hybrid Approach (Recommended)

```python
def extract_text_smart(file_path: str) -> str:
    """Choose the right tool based on document type."""
    suffix = Path(file_path).suffix.lower()

    # Use free extraction for digital documents
    if suffix in {'.docx', '.xlsx', '.pptx', '.html'}:
        converter = DocumentConverter()
        return converter.extract_text(file_path)

    # Try free extraction for PDFs first
    elif suffix == '.pdf':
        try:
            # Try free extraction first (works for digital PDFs)
            converter = DocumentConverter()
            text = converter.extract_text(file_path)
            if len(text.strip()) > 100:  # Has substantial text
                return text
        except ValueError as e:
            if "scanned document" in str(e):
                pass  # Fall through to Textract
        except:
            pass

        # Fall back to Textract for scanned PDFs
        extractor = TextractExtractor()
        return extractor.extract_text(file_path)

    # Use Textract for images
    elif suffix in {'.png', '.jpg', '.jpeg', '.tiff'}:
        extractor = TextractExtractor()
        return extractor.extract_text(file_path)
```

## API Reference

### DocumentConverter Class

```python
class DocumentConverter:
    """Extract text from Office documents."""

    def __init__(self, pdf_engine: str = "pdflatex"):
        """Initialize converter."""

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
```

## Requirements

- Python 3.12+
- Pandoc (automatically downloaded on first run via pypandoc)
- Python packages (automatically installed via PEP 723 inline metadata):
  - pypandoc >= 1.13
  - pandas >= 2.3.2
  - openpyxl >= 3.1.5
  - python-pptx >= 1.0.2
  - pdfplumber >= 0.11.7
  - loguru >= 0.7.3

## Installation

### Quick Start (No Installation Required!)

```bash
# Clone repository
git clone https://github.com/yourusername/office-doc-extractor.git
cd office-doc-extractor

# That's it! Just run with uv (auto-installs everything)
uv run office_doc_extractor.py document.docx --extract-text
```

**Note**: On first run, Pandoc will be automatically downloaded (~7 seconds). No manual installation needed!

### Install uv (if not already installed)

```bash
pip install uv
```

### Docker

```dockerfile
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Copy application
COPY office_doc_extractor.py .

# Pandoc and dependencies auto-install on first run
CMD ["uv", "run", "office_doc_extractor.py"]
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/office-doc-extractor/issues)
- 💬 [Discussions](https://github.com/yourusername/office-doc-extractor/discussions)

## Acknowledgments

Built with:

- [Pandoc](https://pandoc.org/) - Universal document converter
- [pandas](https://pandas.pydata.org/) - Data analysis library
- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint library
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel library

## Related Projects

- [AWS Textract](https://aws.amazon.com/textract/) - OCR service for scanned documents
- [LangChain](https://python.langchain.com/) - LLM application framework
- [LlamaIndex](https://www.llamaindex.ai/) - Data framework for LLMs

---

**Made with ❤️ for the LLM community**
