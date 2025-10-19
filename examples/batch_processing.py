#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pypandoc>=1.13",
#   "pandas>=2.0.0",
#   "openpyxl>=3.0.0",
#   "python-pptx>=0.6.0",
#   "pdfplumber>=0.10.0",
#   "loguru>=0.7.0",
# ]
# ///
"""
Example: Batch Processing Multiple Documents.

Process entire directories of Office documents and save extracted text.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from office_doc_extractor import DocumentConverter


def batch_extract(input_dir: str, output_dir: str = "output"):
    """
    Extract text from all Office documents in a directory.

    Args:
        input_dir: Directory containing documents
        output_dir: Directory for extracted text files

    """
    converter = DocumentConverter()

    input_path = Path(input_dir)
    output_path = Path(output_dir) / "text"
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported formats
    patterns = ["*.docx", "*.xlsx", "*.pptx", "*.pdf", "*.html"]

    results = {
        "timestamp": datetime.now().isoformat(),
        "input_directory": str(input_path),
        "output_directory": str(output_path),
        "files": [],
    }

    print(f"\n{'=' * 70}")
    print(f"Batch Processing: {input_path}")
    print(f"{'=' * 70}\n")

    # Process each file type
    for pattern in patterns:
        for file in input_path.glob(pattern):
            print(f"Processing: {file.name}...", end=" ")

            try:
                # Extract text
                text = converter.extract_text(str(file))

                # Save to output
                output_file = output_path / f"{file.stem}.txt"
                output_file.write_text(text, encoding="utf-8")

                # Record result
                file_result = {
                    "filename": file.name,
                    "format": file.suffix,
                    "size": file.stat().st_size,
                    "text_length": len(text),
                    "output_file": str(output_file),
                    "status": "success",
                }

                results["files"].append(file_result)
                print(f"✓ ({len(text):,} chars)")

            except Exception as e:
                file_result = {
                    "filename": file.name,
                    "format": file.suffix,
                    "status": "failed",
                    "error": str(e),
                }
                results["files"].append(file_result)
                print(f"✗ Error: {e}")

    # Save metadata
    metadata_file = Path(output_dir) / "extraction_metadata.json"
    with Path.open(metadata_file, "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print(f"\n{'=' * 70}")
    print("Summary")
    print(f"{'=' * 70}")

    successful = sum(1 for f in results["files"] if f["status"] == "success")
    failed = sum(1 for f in results["files"] if f["status"] == "failed")
    total_chars = sum(f.get("text_length", 0) for f in results["files"])

    print(f"Total files: {len(results['files'])}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total characters extracted: {total_chars:,}")
    print(f"\nOutput directory: {output_path}")
    print(f"Metadata saved to: {metadata_file}")

    return results


def main():
    """Example usage."""
    parser = argparse.ArgumentParser(
        description="Batch extract text from Office documents",
    )
    parser.add_argument("input_dir", help="Directory containing documents")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory (default: output)",
    )

    args = parser.parse_args()

    batch_extract(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
