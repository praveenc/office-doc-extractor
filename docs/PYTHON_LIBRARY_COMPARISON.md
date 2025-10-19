# Python Libraries for Document Text Extraction

## Overview

Comparison of Python libraries for extracting text from Microsoft Office and other document formats.

## Excel Files (XLSX, XLS)

### Option 1: pandas + openpyxl (Recommended) ✓

**Currently Implemented**

```python
import pandas as pd

# Read Excel file
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# Convert to text
text = df.to_string(index=False)
```

**Pros**:

- ✓ Handles multiple sheets
- ✓ Preserves data structure
- ✓ Excellent for data analysis
- ✓ Supports both .xlsx and .xls
- ✓ Well-maintained and widely used

**Cons**:

- ✗ Large dependency (pandas)
- ✗ May lose formatting/styling

**Best for**: Data extraction, spreadsheet analysis

### Option 2: openpyxl (Direct)

```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
ws = wb.active

for row in ws.iter_rows(values_only=True):
    print(row)
```

**Pros**:

- ✓ Lighter than pandas
- ✓ Access to cell formatting
- ✓ Can read and write

**Cons**:

- ✗ Only supports .xlsx (not .xls)
- ✗ More manual processing needed

**Best for**: When you need cell-level control

### Option 3: xlrd (Legacy)

```python
import xlrd

book = xlrd.open_workbook('file.xls')
sheet = book.sheet_by_index(0)

for row in range(sheet.nrows):
    print(sheet.row_values(row))
```

**Pros**:

- ✓ Supports old .xls format
- ✓ Lightweight

**Cons**:

- ✗ No longer maintained for .xlsx
- ✗ Deprecated for modern use

**Best for**: Legacy .xls files only

### Recommendation: pandas + openpyxl ✓

**Why**: Best balance of features, maintenance, and ease of use.

## PowerPoint Files (PPTX)

### Option 1: python-pptx (Recommended) ✓

**Currently Implemented**

```python
from pptx import Presentation

prs = Presentation('file.pptx')

for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            print(shape.text)
```

**Pros**:

- ✓ Official Python library for PPTX
- ✓ Extracts text, tables, and notes
- ✓ Access to slide structure
- ✓ Well-documented
- ✓ Active maintenance

**Cons**:

- ✗ Only supports .pptx (not .ppt)
- ✗ May miss text in images/charts

**Best for**: Modern PowerPoint files

### Option 2: pptx2txt

```python
from pptx2txt import process

text = process('file.pptx')
```

**Pros**:

- ✓ Simple one-liner
- ✓ Returns plain text

**Cons**:

- ✗ Less control over structure
- ✗ Less maintained
- ✗ Wrapper around python-pptx

**Best for**: Quick text dumps

### Option 3: LibreOffice (via subprocess)

```python
import subprocess

subprocess.run([
    'libreoffice',
    '--headless',
    '--convert-to', 'txt',
    'file.pptx'
])
```

**Pros**:
- ✓ Supports .ppt and .pptx
- ✓ Handles complex layouts

**Cons**:
- ✗ Requires LibreOffice installation
- ✗ Slower (spawns process)
- ✗ Platform-dependent

**Best for**: Legacy .ppt files

### Recommendation: python-pptx ✓

**Why**: Official library, best maintained, good structure preservation.

## Word Documents (DOCX)

### Option 1: pypandoc (Recommended) ✓

**Currently Implemented**

```python
import pypandoc

text = pypandoc.convert_file('file.docx', 'plain')
```

**Pros**:

- ✓ Excellent text extraction
- ✓ Preserves structure
- ✓ Handles complex formatting
- ✓ Can convert to many formats

**Cons**:

- ✗ Requires Pandoc installation
- ✗ External dependency

**Best for**: High-quality text extraction

### Option 2: python-docx

```python
from docx import Document

doc = Document('file.docx')

for paragraph in doc.paragraphs:
    print(paragraph.text)
```

**Pros**:
- ✓ Pure Python
- ✓ Access to document structure
- ✓ Can read and write

**Cons**:
- ✗ May miss headers/footers
- ✗ Complex tables need extra handling

**Best for**: When you need document structure

### Option 3: docx2txt

```python
import docx2txt

text = docx2txt.process('file.docx')
```

**Pros**:
- ✓ Simple one-liner
- ✓ Extracts images too

**Cons**:
- ✗ Less control
- ✗ May lose formatting

**Best for**: Quick text extraction

### Recommendation: pypandoc ✓

**Why**: Best text quality, handles complex documents well.

## HTML Files

### Option 1: pypandoc (Recommended) ✓

**Currently Implemented**

```python
import pypandoc

text = pypandoc.convert_file('file.html', 'plain')
```

**Pros**:
- ✓ Clean text output
- ✓ Removes HTML tags properly
- ✓ Handles complex HTML

**Cons**:
- ✗ Requires Pandoc

**Best for**: Clean text extraction

### Option 2: BeautifulSoup

```python
from bs4 import BeautifulSoup

with open('file.html') as f:
    soup = BeautifulSoup(f, 'html.parser')
    text = soup.get_text()
```

**Pros**:
- ✓ Pure Python
- ✓ Flexible parsing
- ✓ Can extract specific elements

**Cons**:
- ✗ May need cleanup
- ✗ Whitespace handling

**Best for**: When you need HTML parsing control

### Option 3: html2text

```python
import html2text

h = html2text.HTML2Text()
text = h.handle(html_content)
```

**Pros**:
- ✓ Converts to Markdown
- ✓ Preserves links

**Cons**:
- ✗ Output is Markdown, not plain text

**Best for**: HTML to Markdown conversion

### Recommendation: pypandoc ✓

**Why**: Cleanest output, best for text extraction.

## PDF Files

### Option 1: pypandoc (For text-based PDFs)

```python
import pypandoc

text = pypandoc.convert_file('file.pdf', 'plain')
```

**Pros**:
- ✓ Works for text-based PDFs
- ✓ Clean output

**Cons**:
- ✗ Cannot handle scanned PDFs
- ✗ May lose layout

**Best for**: Digital PDFs with selectable text

### Option 2: pdfplumber

```python
import pdfplumber

with pdfplumber.open('file.pdf') as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

**Pros**:
- ✓ Excellent table extraction
- ✓ Layout preservation
- ✓ Pure Python

**Cons**:
- ✗ Cannot handle scanned PDFs

**Best for**: PDFs with tables

### Option 3: PyPDF2

```python
from PyPDF2 import PdfReader

reader = PdfReader('file.pdf')
for page in reader.pages:
    print(page.extract_text())
```

**Pros**:
- ✓ Lightweight
- ✓ Pure Python

**Cons**:
- ✗ Poor text extraction quality
- ✗ Cannot handle scanned PDFs

**Best for**: Simple PDFs only

### Option 4: AWS Textract (For scanned PDFs) ✓

**Currently Implemented**

```python
from textract_extractor import TextractExtractor

extractor = TextractExtractor()
text = extractor.extract_text('scanned.pdf')
```

**Pros**:
- ✓ Handles scanned documents
- ✓ OCR capability
- ✓ High accuracy

**Cons**:
- ✗ Costs money
- ✗ Requires AWS credentials
- ✗ API latency

**Best for**: Scanned documents, images

### Recommendation:
- **Text-based PDFs**: pypandoc or pdfplumber
- **Scanned PDFs**: AWS Textract ✓

## Summary Table

| Format | Library | Status | Pros | Cons |
|--------|---------|--------|------|------|
| DOCX | pypandoc | ✓ Implemented | Best quality | Needs Pandoc |
| HTML | pypandoc | ✓ Implemented | Clean output | Needs Pandoc |
| XLSX | pandas + openpyxl | ✓ Implemented | Full-featured | Large dependency |
| PPTX | python-pptx | ✓ Implemented | Official library | PPTX only |
| PDF (text) | pypandoc | Alternative | Good quality | No OCR |
| PDF (scanned) | AWS Textract | ✓ Implemented | OCR capable | Costs money |

## Current Implementation Status

### ✓ Fully Implemented

1. **DOCX** → pypandoc → plain text
2. **HTML** → pypandoc → plain text
3. **XLSX** → pandas → plain text
4. **PPTX** → python-pptx → markdown → plain text
5. **PDF/Images** → AWS Textract → plain text

### Test Results

```bash
# DOCX extraction
✓ Extracted 120,420 characters in 0.2s

# XLSX extraction
✓ Extracted 4,235,738 characters in 2s

# PPTX extraction
✓ Extracted 2,810 characters in 0.5s
```

## Alternative Libraries to Consider

### For Better Excel Handling

**xlwings** (if Excel is installed):
```python
import xlwings as xw

wb = xw.Book('file.xlsx')
sheet = wb.sheets[0]
data = sheet.used_range.value
```

**Pros**: Full Excel API access
**Cons**: Requires Excel installation

### For Better PowerPoint Handling

**Aspose.Slides** (commercial):
```python
from aspose.slides import Presentation

pres = Presentation('file.pptx')
```

**Pros**: Professional features
**Cons**: Commercial license required

### For Better PDF Handling

**pdfminer.six**:
```python
from pdfminer.high_level import extract_text

text = extract_text('file.pdf')
```

**Pros**: Better layout analysis
**Cons**: Complex API

## Recommendations

### Current Implementation is Optimal ✓

The current implementation uses the best libraries for each format:

1. **pypandoc**: Best for DOCX/HTML (high-quality text)
2. **pandas + openpyxl**: Best for XLSX (data handling)
3. **python-pptx**: Best for PPTX (official library)
4. **AWS Textract**: Best for scanned documents (OCR)

### No Changes Needed

The libraries chosen are:
- ✓ Well-maintained
- ✓ Widely used
- ✓ Best-in-class for their purpose
- ✓ Good documentation
- ✓ Active communities

### When to Consider Alternatives

- **Legacy .ppt files**: Use LibreOffice conversion
- **Legacy .xls files**: Use xlrd
- **Complex PDF tables**: Consider pdfplumber
- **Excel with formulas**: Consider xlwings (if Excel installed)

## Installation

All required libraries are in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or with uv:

```bash
uv pip install -r requirements.txt
```

## Conclusion

**The current implementation is production-ready and uses the best available libraries for each format.** No changes are recommended unless you have specific requirements like:

- Legacy file format support (.ppt, .xls)
- Formula evaluation in Excel
- Advanced PDF layout analysis
- Commercial support requirements
