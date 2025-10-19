# Test Suite Documentation

This directory contains test scripts for validating the Office Document Text Extractor functionality.

**Quick Start**: Run `uv run tests/test_extractor.py` to verify all formats work (DOCX, XLSX, PPTX, PDF).

**Note**: With PEP 723 metadata, `uv run` automatically installs dependencies!

## Test Files

### test_extractor.py (Main Test Suite)

**Purpose**: Comprehensive test suite covering all supported formats including PDF.

**What it tests**:

- ✅ DOCX text extraction
- ✅ XLSX text extraction
- ✅ PPTX text extraction
- ✅ PDF text extraction (NEW!)
- ✅ PDF page markers
- ✅ Output directory structure
- ✅ Filename preservation
- ✅ Error handling

**How to run**:

```bash
# From project root (using uv - recommended)
uv run tests/test_extractor.py

# Or using python directly
python tests/test_extractor.py

# Clean up test outputs
rm -rf output
```

**Expected output**:

```bash
======================================================================
OFFICE DOCUMENT EXTRACTOR - COMPREHENSIVE TEST SUITE
Including PDF Support
======================================================================

======================================================================
COMPREHENSIVE FORMAT TEST (Including PDFs)
======================================================================

📄 DOCX   Marshal Entry.docx
----------------------------------------------------------------------
✓ Extracted: 1,711 characters
✓ Saved to: output/text/Marshal Entry.txt

📄 XLSX   Questions, Actions, and Scores Spreadsheet.xlsx
----------------------------------------------------------------------
✓ Extracted: 175,315 characters
✓ Saved to: output/text/Questions, Actions, and Scores Spreadsheet.txt

📄 PPTX   Example Customer Assessment Summary.pptx
----------------------------------------------------------------------
✓ Extracted: 2,810 characters
✓ Saved to: output/text/Example Customer Assessment Summary.txt

📄 PDF    Example Customer Assessment Summary v2.pdf
----------------------------------------------------------------------
✓ Extracted: 47,877 characters
✓ Saved to: output/text/Example Customer Assessment Summary v2.txt

📄 PDF    Example SIP Workshop Summary_ppt.pdf
----------------------------------------------------------------------
✓ Extracted: 42,299 characters
✓ Saved to: output/text/Example SIP Workshop Summary_ppt.txt

======================================================================
TEST SUMMARY
======================================================================
Total files tested: 5
✓ Successful: 5
✗ Failed: 0

======================================================================
ALL TESTS PASSED ✓
======================================================================

======================================================================
PDF-SPECIFIC TESTS
======================================================================
✓ Extracted 47,877 characters
✓ Found 53 page markers
✓ PDF extraction working correctly

======================================================================
🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉
======================================================================

Verified:
  ✓ DOCX extraction
  ✓ XLSX extraction
  ✓ PPTX extraction
  ✓ PDF extraction (NEW!)
  ✓ Page markers in PDFs
  ✓ Output directory structure
  ✓ File naming preservation
```

**What it validates**:

- Text extraction works for all supported formats including PDF
- PDF page markers are correctly added
- Output directories are created automatically
- Filenames are preserved correctly
- Text content is non-empty and substantial
- Error handling works properly

---

## Quick Test Guide

### Run Test Suite

```bash
# Run comprehensive test (recommended - using uv)
uv run tests/test_extractor.py

# Or using python directly
python tests/test_extractor.py

# Clean up after testing
rm -rf output
```

### Test Specific Features

#### Test Text Extraction Only

```bash
# Test DOCX extraction
python -c "
from office_doc_extractor import DocumentConverter
converter = DocumentConverter()
text = converter.extract_text('sample_input_docs/Marshal Entry.docx')
print(f'✓ Extracted {len(text)} characters')
"
```

#### Test PDF Extraction

```bash
# Test PDF extraction
python -c "
from office_doc_extractor import DocumentConverter
converter = DocumentConverter()
text = converter.extract_text('sample_input_docs/Example Customer Assessment Summary v2.pdf')
print(f'✓ Extracted {len(text)} characters from PDF')
print(f'✓ Page markers: {text.count(\"--- Page\")}')
"
```

#### Test Batch Processing

```bash
# Process all documents in a directory (including PDFs)
for file in sample_input_docs/*.{docx,xlsx,pptx,pdf}; do
    python office_doc_extractor.py "$file" --extract-text --quiet
done

# Verify outputs
ls -lh output/text/
```

#### Test Custom Output Directory

```bash
# Extract to custom location
python office_doc_extractor.py sample_input_docs/Marshal\ Entry.docx \
    --extract-text --output-dir my_test_output

# Verify
ls -lh my_test_output/text/
```

---

## Test Requirements

### Required Files

Tests expect these sample documents in `sample_input_docs/`:

- `Marshal Entry.docx` (DOCX test file)
- `Questions, Actions, and Scores Spreadsheet.xlsx` (XLSX test file)
- `Example Customer Assessment Summary.pptx` (PPTX test file)
- `Example Customer Assessment Summary v2.pdf` (PDF test file)
- `Example SIP Workshop Summary_ppt.pdf` (PDF test file)

### Required Dependencies

All tests require:

```bash
pip install pypandoc pandas openpyxl python-pptx pdfplumber loguru

# Or install from requirements.txt
pip install -r requirements.txt
```

System dependencies:

```bash
# Pandoc (required for all tests)
brew install pandoc  # macOS
sudo apt-get install pandoc  # Ubuntu

# LaTeX (optional, only for PDF conversion tests)
brew install --cask mactex  # macOS
sudo apt-get install texlive-latex-base  # Ubuntu
```

---

## Test Output Cleanup

After running tests, clean up generated files:

```bash
# Remove all test outputs
rm -rf output/ results/ batch_output/ my_output/ my_results/
rm -f custom_output.txt

# Or use a cleanup script
cat > cleanup_tests.sh << 'EOF'
#!/bin/bash
echo "Cleaning up test outputs..."
rm -rf output/ results/ batch_output/ my_output/ my_results/
rm -f custom_output.txt
echo "✓ Cleanup complete"
EOF

chmod +x cleanup_tests.sh
./cleanup_tests.sh
```

---

## Troubleshooting Tests

### "Pandoc not found"

**Solution**: Install Pandoc

```bash
brew install pandoc  # macOS
sudo apt-get install pandoc  # Ubuntu
```

### "pdflatex not found"

**Solution**: Either:

1. Install LaTeX (if you want to test PDF conversion)
2. Skip PDF conversion tests (text extraction will still work)

```bash
# Install LaTeX
brew install --cask mactex  # macOS
sudo apt-get install texlive-latex-base  # Ubuntu
```

### "Module not found"

**Solution**: Install Python dependencies

```bash
pip install pypandoc pandas openpyxl python-pptx loguru
```

### "File not found: sample_input_docs/..."

**Solution**: Tests expect sample documents. Either:

1. Create `sample_input_docs/` with test documents
2. Modify test scripts to use your own documents
3. Skip tests that require missing files

### Tests fail with "No such file or directory"

**Solution**: Run tests from project root directory

```bash
# Correct
cd /path/to/office-doc-extractor
python tests/test_all_features.py

# Incorrect
cd tests
python test_all_features.py  # Will fail - wrong directory
```

---

## Adding New Tests

### Test Template

```python
"""
Test description.
"""

from pathlib import Path
from office_doc_extractor import DocumentConverter

def test_new_feature():
    """Test new feature description."""
    print("\n" + "=" * 70)
    print("TEST: New Feature")
    print("=" * 70)

    converter = DocumentConverter()

    # Test logic
    result = converter.extract_text('test_file.docx')

    # Assertions
    assert len(result) > 0, "Text should not be empty"
    assert "expected content" in result, "Should contain expected content"

    print("✓ Test passed")

if __name__ == "__main__":
    test_new_feature()
```

### Running Custom Tests

```python
# test_custom.py
from office_doc_extractor import DocumentConverter

def test_my_documents():
    """Test with my own documents."""
    converter = DocumentConverter()

    my_docs = [
        'my_docs/report.docx',
        'my_docs/data.xlsx',
        'my_docs/slides.pptx'
    ]

    for doc in my_docs:
        try:
            text = converter.extract_text(doc)
            print(f"✓ {doc}: {len(text)} characters")
        except Exception as e:
            print(f"✗ {doc}: {e}")

if __name__ == "__main__":
    test_my_documents()
```

---

## Test Coverage

### What's Tested

- ✅ Text extraction from DOCX files
- ✅ Text extraction from XLSX files
- ✅ Text extraction from PPTX files
- ✅ Text extraction from PDF files (NEW!)
- ✅ PDF page markers
- ✅ Text extraction from HTML files
- ✅ Default output directory creation
- ✅ Custom output directory support
- ✅ Specific output file support
- ✅ Batch processing
- ✅ Filename preservation
- ✅ Error handling

### What's Not Tested

- ❌ AWS Textract integration (requires AWS credentials)
- ❌ Scanned PDF detection
- ❌ Legacy formats (.doc, .xls, .ppt)
- ❌ Corrupted file handling
- ❌ Very large files (>100MB)
- ❌ Network/API failures

---

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'

    - name: Install Pandoc
      run: sudo apt-get install -y pandoc

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run tests
      run: python tests/test_all_features.py
```

---

## Summary

**Recommended test workflow**:

1. **Quick validation**: `python tests/test_converter_final.py`
2. **Comprehensive test**: `python tests/test_all_features.py`
3. **Full test suite**: `python tests/test_converter.py` (if LaTeX installed)

**All tests should pass** if:

- Pandoc is installed
- Python dependencies are installed
- Sample documents are available
- Tests are run from project root directory

For questions or issues with tests, please open an issue on GitHub.
