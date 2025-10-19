# Pypandoc How-To Guide

## Overview

Pypandoc is a Python wrapper for Pandoc, a universal document converter. It enables conversion between various document formats programmatically from Python code.

- **Version**: 1.15
- **Pandoc Version**: 3.8
- **GitHub**: <https://github.com/JessicaTegner/pypandoc>
- **License**: MIT

## Key Capabilities

### Supported Input Formats

Pypandoc supports a wide range of input formats including:

- **Documents**: docx, odt, rtf
- **Markup**: html, markdown, rst, textile, mediawiki, org
- **Academic**: latex, bibtex, biblatex, jats
- **Data**: json, csv, tsv
- **E-books**: epub, fb2
- **Other**: ipynb, xml, opml

### Supported Output Formats

Key output formats include:

- **PDF**: pdf (requires LaTeX installation)
- **Documents**: docx, odt, rtf
- **Markup**: html, markdown, rst
- **Presentations**: pptx, beamer, revealjs, slidy
- **Academic**: latex, jats, tei
- **Plain text**: plain, asciidoc

### Format Limitations

**Not Supported as Input**:

- Excel files (xlsx, xls) - Pandoc cannot read spreadsheet formats
- PowerPoint files (pptx) - Pandoc can only write PPTX, not read it

**Workarounds Required**:

- For Excel: Use libraries like `openpyxl` or `pandas` to extract data first
- For PowerPoint: Use `python-pptx` to extract text, then convert to supported format

## Installation

### Basic Installation

```bash
pip install pypandoc
```

### Installing Pandoc

Pypandoc requires Pandoc to be installed on the system:

**macOS**:

```bash
brew install pandoc
```

**Ubuntu/Debian**:

```bash
sudo apt-get install pandoc
```

**Windows**:

Download from <https://pandoc.org/installing.html>

### PDF Support

For PDF output, install LaTeX:

**macOS**:

```bash
brew install --cask mactex
```

**Ubuntu/Debian**:

```bash
sudo apt-get install texlive-latex-base texlive-fonts-recommended
```

## Core Functions

### convert_file()

Convert a file from one format to another.

```python
import pypandoc

# Basic conversion
output = pypandoc.convert_file('input.html', 'pdf', outputfile='output.pdf')

# With format specification
output = pypandoc.convert_file(
    source_file='document.docx',
    to='pdf',
    format='docx',  # Optional, inferred from extension
    outputfile='output.pdf'
)
```

**Parameters**:

- `source_file`: File path, list of paths, or file pattern (e.g., `dir/*.md`)
- `to`: Target format (e.g., 'pdf', 'html', 'docx')
- `format`: Source format (optional, auto-detected from extension)
- `outputfile`: Output file path (if None, returns string)
- `extra_args`: List of additional pandoc arguments
- `filters`: List of pandoc filters to apply
- `encoding`: Input encoding (default: 'utf-8')
- `sandbox`: Run in sandbox mode for untrusted input (pandoc >= 2.15)
- `cworkdir`: Set working directory for conversion

**Returns**: Converted content as string, or empty string if outputfile specified

### convert_text()

Convert text string from one format to another.

```python
import pypandoc

html_text = "<h1>Hello World</h1><p>This is a test.</p>"
markdown = pypandoc.convert_text(html_text, 'markdown', format='html')
print(markdown)
# Output: # Hello World\n\nThis is a test.
```

### get_pandoc_formats()

Get lists of supported input and output formats.

```python
import pypandoc

input_formats, output_formats = pypandoc.get_pandoc_formats()
print(f"Can read: {', '.join(input_formats)}")
print(f"Can write: {', '.join(output_formats)}")
```

### get_pandoc_version()

Get installed Pandoc version.

```python
import pypandoc

version = pypandoc.get_pandoc_version()
print(f"Pandoc version: {version}")
```

## Common Use Cases

### HTML to PDF

```python
import pypandoc

pypandoc.convert_file(
    'document.html',
    'pdf',
    outputfile='document.pdf',
    extra_args=['--pdf-engine=pdflatex']
)
```

### DOCX to PDF

```python
import pypandoc

pypandoc.convert_file(
    'document.docx',
    'pdf',
    outputfile='document.pdf'
)
```

### Markdown to HTML

```python
import pypandoc

html = pypandoc.convert_file('README.md', 'html')
print(html)
```

### Multiple Files to Single PDF

```python
import pypandoc

pypandoc.convert_file(
    ['chapter1.md', 'chapter2.md', 'chapter3.md'],
    'pdf',
    outputfile='book.pdf',
    extra_args=['--toc', '--toc-depth=2']
)
```

### Using File Patterns

```python
import pypandoc

# Convert all markdown files in a directory
pypandoc.convert_file(
    'docs/*.md',
    'pdf',
    outputfile='combined.pdf'
)
```

## Advanced Features

### Extra Arguments

Pass additional Pandoc command-line arguments:

```python
import pypandoc

pypandoc.convert_file(
    'document.html',
    'pdf',
    outputfile='output.pdf',
    extra_args=[
        '--pdf-engine=xelatex',
        '--variable=geometry:margin=1in',
        '--toc',
        '--toc-depth=3',
        '--highlight-style=tango'
    ]
)
```

### Using Filters

Apply Pandoc filters for custom processing:

```python
import pypandoc

pypandoc.convert_file(
    'document.md',
    'html',
    outputfile='output.html',
    filters=['pandoc-citeproc']
)
```

### Sandbox Mode

For processing untrusted input (Pandoc >= 2.15):

```python
import pypandoc

pypandoc.convert_file(
    'untrusted.html',
    'pdf',
    outputfile='output.pdf',
    sandbox=True
)
```

### Custom Working Directory

Set working directory for relative paths:

```python
import pypandoc

pypandoc.convert_file(
    'document.md',
    'pdf',
    outputfile='output.pdf',
    cworkdir='/path/to/project'
)
```

## Error Handling

```python
import pypandoc
from pathlib import Path

try:
    pypandoc.convert_file('input.html', 'pdf', outputfile='output.pdf')
except RuntimeError as e:
    print(f"Conversion failed: {e}")
except OSError as e:
    print(f"Pandoc not found: {e}")
except FileNotFoundError as e:
    print(f"Input file not found: {e}")
```

## Best Practices

### 1. Verify Format Support

```python
import pypandoc

def can_convert(from_format: str, to_format: str) -> bool:
    """Check if conversion is supported."""
    input_formats, output_formats = pypandoc.get_pandoc_formats()
    return from_format in input_formats and to_format in output_formats
```

### 2. Use Pathlib

```python
from pathlib import Path
import pypandoc

input_file = Path('documents/input.html')
output_file = Path('output/result.pdf')

pypandoc.convert_file(
    str(input_file),
    'pdf',
    outputfile=str(output_file)
)
```

### 3. Validate Input Files

```python
from pathlib import Path
import pypandoc

def safe_convert(input_path: str, output_path: str) -> bool:
    """Safely convert file with validation."""
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    pypandoc.convert_file(
        str(input_file),
        'pdf',
        outputfile=output_path
    )
    return True
```

### 4. Handle Large Files

For large files, use outputfile parameter instead of returning string:

```python
import pypandoc

# Good: Write directly to file
pypandoc.convert_file('large.html', 'pdf', outputfile='large.pdf')

# Avoid: Loading entire output in memory
# output = pypandoc.convert_file('large.html', 'pdf')
```

### 5. Set Appropriate PDF Engine

```python
import pypandoc

# For Unicode support
pypandoc.convert_file(
    'document.html',
    'pdf',
    outputfile='output.pdf',
    extra_args=['--pdf-engine=xelatex']
)

# For faster processing
pypandoc.convert_file(
    'document.html',
    'pdf',
    outputfile='output.pdf',
    extra_args=['--pdf-engine=pdflatex']
)
```

## Limitations and Workarounds

### Excel Files (XLSX, XLS)

Pandoc cannot read Excel files. Use alternative approach:

```python
import pandas as pd
import pypandoc

# Read Excel and convert to HTML
df = pd.read_excel('data.xlsx')
html = df.to_html()

# Convert HTML to PDF
pypandoc.convert_text(html, 'pdf', format='html', outputfile='output.pdf')
```

### PowerPoint Files (PPTX)

Pandoc can write PPTX but not read it. Use python-pptx:

```python
from pptx import Presentation
import pypandoc

# Extract text from PPTX
prs = Presentation('presentation.pptx')
text_content = []

for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            text_content.append(shape.text)

markdown = '\n\n'.join(text_content)

# Convert to PDF
pypandoc.convert_text(markdown, 'pdf', format='markdown', outputfile='output.pdf')
```

### Complex Layouts

Pandoc may not preserve complex layouts perfectly. For pixel-perfect conversions, consider:

- Using native tools (e.g., LibreOffice for DOCX to PDF)
- Adjusting extra_args for better formatting
- Post-processing the output

## Performance Considerations

### 1. Batch Processing

Process multiple files efficiently:

```python
import pypandoc
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def convert_file_wrapper(input_file: Path) -> None:
    """Convert single file."""
    output_file = input_file.with_suffix('.pdf')
    pypandoc.convert_file(str(input_file), 'pdf', outputfile=str(output_file))

# Process files in parallel
input_files = list(Path('documents').glob('*.html'))
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(convert_file_wrapper, input_files)
```

### 2. Caching

Cache conversion results for repeated conversions:

```python
import pypandoc
from pathlib import Path
import hashlib

def get_file_hash(file_path: Path) -> str:
    """Get file content hash."""
    return hashlib.md5(file_path.read_bytes()).hexdigest()

def convert_with_cache(input_file: Path, output_file: Path) -> None:
    """Convert with caching."""
    cache_file = output_file.with_suffix('.cache')

    current_hash = get_file_hash(input_file)

    if cache_file.exists() and output_file.exists():
        cached_hash = cache_file.read_text()
        if cached_hash == current_hash:
            print(f"Using cached version: {output_file}")
            return

    pypandoc.convert_file(str(input_file), 'pdf', outputfile=str(output_file))
    cache_file.write_text(current_hash)
```

## Troubleshooting

### Pandoc Not Found

```python
import pypandoc

try:
    version = pypandoc.get_pandoc_version()
except OSError:
    print("Pandoc not installed. Install with: brew install pandoc")
```

### PDF Engine Not Found

If you get "pdflatex not found" error:

```bash
# macOS
brew install --cask mactex

# Ubuntu
sudo apt-get install texlive-latex-base
```

### Unicode Issues

Use XeLaTeX for better Unicode support:

```python
pypandoc.convert_file(
    'unicode.html',
    'pdf',
    outputfile='output.pdf',
    extra_args=['--pdf-engine=xelatex']
)
```

### Memory Issues

For large files, ensure output goes to file:

```python
# Good
pypandoc.convert_file('large.html', 'pdf', outputfile='output.pdf')

# Bad - may cause memory issues
content = pypandoc.convert_file('large.html', 'pdf')
```

## References

- Pypandoc GitHub: <https://github.com/JessicaTegner/pypandoc>
- Pandoc Documentation: <https://pandoc.org/MANUAL.html>
- Pandoc Filters: <https://pandoc.org/filters.html>
- PDF Engines: <https://pandoc.org/MANUAL.html#option--pdf-engine>
