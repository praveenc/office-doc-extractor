# Text Extraction Strategy

## Overview

This document outlines the optimal strategy for extracting text from various document formats, balancing cost, speed, and accuracy.

## Key Insight: Direct Text Extraction vs Textract

**Important Discovery**: For structured documents (DOCX, HTML, XLSX, PPTX), we can extract text directly using pypandoc and Python libraries, **bypassing both PDF conversion and AWS Textract API calls**. This approach is:

- **Faster**: No PDF conversion or API calls
- **Cheaper**: No Textract API costs
- **Simpler**: Fewer dependencies and steps

**Reserve Textract for**: Scanned documents, images, and PDFs where OCR is actually needed.

## Extraction Methods by Format

### Method 1: Direct Text Extraction (Recommended)

**Supported Formats**: HTML, DOCX

**Tool**: pypandoc

**Advantages**:

- No PDF conversion needed
- No Textract API costs
- Fast processing
- Preserves text structure

**Usage**:

```bash
python doc_to_pdf_converter.py document.docx --extract-text
```

**Example Output**:

```text
✓ Extracted 120,420 characters from Example Customer Assessment Summary v2.docx
Processing time: < 1 second
Cost: $0.00
```

### Method 2: Hybrid Extraction (Excel/PowerPoint)

**Supported Formats**: XLSX, XLS, PPTX

**Tools**: pandas, python-pptx, pypandoc

**Process**:

1. Extract data/text using specialized library
2. Convert to intermediate format (HTML/Markdown)
3. Output as plain text

**Advantages**:

- No Textract needed
- Preserves table structure (Excel)
- Preserves slide structure (PowerPoint)

**Usage**:

```bash
python doc_to_pdf_converter.py spreadsheet.xlsx --extract-text
python doc_to_pdf_converter.py presentation.pptx --extract-text
```

### Method 3: PDF Conversion + Textract (When Needed)

**Use Cases**:

- Scanned documents
- Image-based PDFs
- Complex layouts requiring OCR
- Handwritten text

**Process**:

1. Convert document to PDF (if not already PDF)
2. Use AWS Textract for OCR

**Usage**:

```bash
# Convert to PDF
python doc_to_pdf_converter.py document.docx --output-dir converted/

# Extract text with Textract
python textract_extractor.py converted/document.pdf
```

## Cost Comparison

### Direct Text Extraction (Methods 1 & 2)

- **Cost per document**: $0.00
- **Processing time**: < 1 second per document
- **Requirements**: Python libraries only

### Textract API (Method 3)

- **Cost per page**: $0.0015 (first 1M pages/month)
- **Processing time**: 1-5 seconds per page
- **Requirements**: AWS credentials, API access

**Example Savings**:

- 1,000 DOCX documents (avg 10 pages each)
- Direct extraction: $0.00
- Textract: $15.00
- **Savings: $15.00 per 1,000 documents**

## Recommended Workflow

### Step 1: Identify Document Type

```python
from pathlib import Path

def get_extraction_method(file_path: str) -> str:
    """Determine optimal extraction method."""
    suffix = Path(file_path).suffix.lower()

    if suffix in {'.html', '.htm', '.docx', '.doc'}:
        return 'direct_text'
    elif suffix in {'.xlsx', '.xls', '.pptx'}:
        return 'hybrid'
    elif suffix in {'.pdf', '.png', '.jpg', '.jpeg', '.tiff'}:
        return 'textract'
    else:
        return 'unsupported'
```

### Step 2: Extract Text Using Appropriate Method

```python
from doc_to_pdf_converter import DocumentConverter
from textract_extractor import TextractExtractor

def extract_text(file_path: str) -> str:
    """Extract text using optimal method."""
    method = get_extraction_method(file_path)

    if method in {'direct_text', 'hybrid'}:
        # Use direct extraction (no Textract needed)
        converter = DocumentConverter()
        return converter.extract_text(file_path)

    elif method == 'textract':
        # Use Textract for OCR
        extractor = TextractExtractor()
        return extractor.extract_text(file_path)

    else:
        raise ValueError(f"Unsupported format: {file_path}")
```

## Performance Benchmarks

Based on test results with sample documents:

### Direct Text Extraction

| Document | Size | Characters | Time | Method |
|----------|------|------------|------|--------|
| Marshal Entry.docx | 15 KB | 1,711 | 0.1s | pypandoc |
| Example KCR.docx | 18 KB | 2,130 | 0.1s | pypandoc |
| Assessment Summary.docx | 245 KB | 120,420 | 0.2s | pypandoc |

**Average**: ~600,000 characters/second

### Textract (for comparison)

| Document | Pages | Time | Cost |
|----------|-------|------|------|
| 10-page PDF | 10 | 5-10s | $0.015 |
| 100-page PDF | 100 | 30-60s | $0.15 |

## Implementation Guide

### For DOCX/HTML Files

```python
from doc_to_pdf_converter import DocumentConverter

converter = DocumentConverter()

# Extract text directly
text = converter.extract_text('document.docx')
print(f"Extracted {len(text)} characters")

# Save to file
with open('output.txt', 'w') as f:
    f.write(text)
```

### For Excel Files

```python
from doc_to_pdf_converter import DocumentConverter

converter = DocumentConverter()

# Extract all sheets as text
text = converter.extract_text('spreadsheet.xlsx')

# Text includes sheet names and data
# Format: "Sheet: SheetName\n[data]\n\n"
```

### For PowerPoint Files

```python
from doc_to_pdf_converter import DocumentConverter

converter = DocumentConverter()

# Extract all slides as markdown
text = converter.extract_text('presentation.pptx')

# Text includes slide numbers and content
# Format: "# Slide 1\n## Title\nContent\n---\n"
```

### For PDFs/Images (Textract)

```python
from textract_extractor import TextractExtractor

extractor = TextractExtractor(
    region_name='us-east-1',
    min_confidence=80.0  # Filter low-confidence results
)

# Extract text with OCR
text = extractor.extract_text('scanned.pdf')
```

## Batch Processing

### Process Multiple Documents

```python
from pathlib import Path
from doc_to_pdf_converter import DocumentConverter
from textract_extractor import TextractExtractor

def batch_extract(input_dir: str, output_dir: str) -> None:
    """Extract text from all documents in directory."""
    converter = DocumentConverter()
    extractor = TextractExtractor()

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for file in input_path.iterdir():
        if not file.is_file():
            continue

        method = get_extraction_method(str(file))
        output_file = output_path / f"{file.stem}.txt"

        try:
            if method in {'direct_text', 'hybrid'}:
                text = converter.extract_text(str(file))
            elif method == 'textract':
                text = extractor.extract_text(str(file))
            else:
                continue

            output_file.write_text(text)
            print(f"✓ {file.name} -> {output_file.name}")

        except Exception as e:
            print(f"✗ {file.name}: {e}")
```

## Decision Tree

```text
Document File
    |
    ├─ Is it DOCX/HTML?
    |   └─ YES → Use pypandoc direct extraction (Method 1)
    |
    ├─ Is it XLSX/PPTX?
    |   └─ YES → Use pandas/python-pptx extraction (Method 2)
    |
    ├─ Is it PDF/Image?
    |   |
    |   ├─ Is it text-based PDF?
    |   |   └─ YES → Use pypandoc or pdfplumber
    |   |
    |   └─ Is it scanned/image-based?
    |       └─ YES → Use Textract (Method 3)
    |
    └─ Unsupported format
        └─ Convert to supported format first
```

## Best Practices

### 1. Always Try Direct Extraction First

```python
def smart_extract(file_path: str) -> str:
    """Try direct extraction before Textract."""
    try:
        # Try direct extraction
        converter = DocumentConverter()
        return converter.extract_text(file_path)
    except ValueError:
        # Fall back to Textract
        extractor = TextractExtractor()
        return extractor.extract_text(file_path)
```

### 2. Cache Extraction Results

```python
import hashlib
from pathlib import Path

def get_cached_text(file_path: str, cache_dir: str = '.cache') -> str:
    """Get text with caching."""
    file_hash = hashlib.md5(Path(file_path).read_bytes()).hexdigest()
    cache_file = Path(cache_dir) / f"{file_hash}.txt"

    if cache_file.exists():
        return cache_file.read_text()

    # Extract text
    text = extract_text(file_path)

    # Cache result
    cache_file.parent.mkdir(exist_ok=True)
    cache_file.write_text(text)

    return text
```

### 3. Monitor Costs

```python
class ExtractionMetrics:
    """Track extraction costs and performance."""

    def __init__(self):
        self.direct_extractions = 0
        self.textract_pages = 0

    def record_direct(self):
        self.direct_extractions += 1

    def record_textract(self, pages: int):
        self.textract_pages += pages

    def get_cost(self) -> float:
        """Calculate total Textract cost."""
        return self.textract_pages * 0.0015

    def get_savings(self) -> float:
        """Calculate savings from direct extraction."""
        # Assume avg 10 pages per document
        avoided_pages = self.direct_extractions * 10
        return avoided_pages * 0.0015
```

## Limitations

### Direct Text Extraction

- **Cannot handle**: Scanned documents, images, handwritten text
- **May lose**: Complex formatting, embedded images, annotations
- **Best for**: Digital documents with selectable text

### Textract

- **Cost**: Per-page charges apply
- **Speed**: Slower than direct extraction
- **Limits**: 10MB for sync, 500MB for async
- **Best for**: Scanned documents, images, complex layouts

## Conclusion

**Key Takeaway**: Use direct text extraction (pypandoc, pandas, python-pptx) for structured digital documents to save time and money. Reserve Textract for documents that actually require OCR.

**Estimated Savings**: 80-90% of documents can use direct extraction, saving significant API costs and processing time.
