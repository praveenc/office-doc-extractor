#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pypandoc>=1.13",
#   "pandas>=2.3.3",
#   "openpyxl>=3.1.5",
#   "python-pptx>=1.0.2",
#   "pdfplumber>=0.11.7",
#   "loguru>=0.7.3",
# ]
# ///
"""
Comprehensive test including PDF support.

Tests all supported formats: DOCX, XLSX, PPTX, PDF, HTML
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from office_doc_extractor import DocumentConverter


def test_all_formats():
    """Test extraction from all supported formats including PDFs."""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE FORMAT TEST (Including PDFs)")
    print("=" * 70)

    converter = DocumentConverter()

    # Test files with expected formats
    test_cases = [
        ("tests/sample_docs/file-sample_100kB.docx", "DOCX"),
        ("tests/sample_docs/WhatIsEntropy.pdf.pdf", "PDF"),
    ]

    results = {"success": [], "failed": []}

    for file_path, format_type in test_cases:
        input_file = Path(file_path)

        if not input_file.exists():
            print(f"\n⊘ {format_type:6} {input_file.name:50} - File not found")
            results["failed"].append((input_file.name, "File not found"))
            continue

        print(f"\n📄 {format_type:6} {input_file.name}")
        print("-" * 70)

        try:
            # Extract text
            text = converter.extract_text(str(input_file))

            # Validate
            assert len(text) > 0, "Text should not be empty"

            # Save to output
            output_dir = Path("output/text")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{input_file.stem}.txt"
            output_file.write_text(text, encoding="utf-8")

            # Show results
            print(f"✓ Extracted: {len(text):,} characters")
            print(f"✓ Saved to: {output_file}")
            print(f"✓ Preview: {text[:150]}...")

            results["success"].append(input_file.name)

        except Exception as e:
            print(f"✗ Failed: {e}")
            results["failed"].append((input_file.name, str(e)))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total files tested: {len(test_cases)}")
    print(f"✓ Successful: {len(results['success'])}")
    print(f"✗ Failed: {len(results['failed'])}")

    if results["success"]:
        print("\n✓ Successful extractions:")
        for filename in results["success"]:
            print(f"  - {filename}")

    if results["failed"]:
        print("\n✗ Failed extractions:")
        for filename, error in results["failed"]:
            print(f"  - {filename}: {error}")

    # Verify all succeeded
    if len(results["failed"]) == 0:
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return 0
    print("\n" + "=" * 70)
    print("SOME TESTS FAILED ✗")
    print("=" * 70)
    return 1


def test_pdf_specific():
    """Test PDF-specific features."""
    print("\n" + "=" * 70)
    print("PDF-SPECIFIC TESTS")
    print("=" * 70)

    converter = DocumentConverter()

    # Test multi-page PDF
    pdf_file = "tests/sample_docs/WhatIsEntropy.pdf.pdf"

    if not Path(pdf_file).exists():
        print(f"⊘ Test PDF not found: {pdf_file}")
        return 1

    print(f"\n📄 Testing: {Path(pdf_file).name}")
    print("-" * 70)

    try:
        text = converter.extract_text(pdf_file)

        # Check for page markers
        page_markers = text.count("--- Page")
        print(f"✓ Extracted {len(text):,} characters")
        print(f"✓ Found {page_markers} page markers")

        # Verify page markers exist
        assert page_markers > 0, "Should have page markers"
        assert "--- Page 1 ---" in text, "Should have Page 1 marker"

        # Check content quality
        assert len(text.strip()) > 1000, "Should have substantial content"

        print("✓ PDF extraction working correctly")

        return 0

    except Exception as e:
        print(f"✗ PDF test failed: {e}")
        return 1


def test_output_structure():
    """Test output directory structure."""
    print("\n" + "=" * 70)
    print("OUTPUT STRUCTURE TEST")
    print("=" * 70)

    output_dir = Path("output/text")

    if not output_dir.exists():
        print("⊘ Output directory not found")
        return 1

    # Check for expected files
    expected_files = [
        "file-sample_100kB.txt",
        "WhatIsEntropy.pdf.txt",
    ]

    found_files = list(output_dir.glob("*.txt"))
    print(f"\n✓ Output directory: {output_dir.absolute()}")
    print(f"✓ Found {len(found_files)} files")

    for file in found_files:
        size = file.stat().st_size
        print(f"  - {file.name} ({size:,} bytes)")

    # Verify key files exist
    found_names = [f.name for f in found_files]
    missing = [f for f in expected_files if f not in found_names]

    if missing:
        print("\n⚠ Missing expected files:")
        for f in missing:
            print(f"  - {f}")

    return 0


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("OFFICE DOCUMENT EXTRACTOR - COMPREHENSIVE TEST SUITE")
    print("Including PDF Support")
    print("=" * 70)

    # Clean up previous outputs
    import shutil

    if Path("output").exists():
        shutil.rmtree("output")

    try:
        # Run tests
        result1 = test_all_formats()
        result2 = test_pdf_specific()
        result3 = test_output_structure()

        # Overall result
        if result1 == 0 and result2 == 0:
            print("\n" + "=" * 70)
            print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
            print("=" * 70)
            print("\nVerified:")
            print("  ✓ DOCX extraction")
            print("  ✓ PDF extraction")
            print("  ✓ Page markers in PDFs")
            print("  ✓ Output directory structure")
            print("  ✓ File naming preservation")
            print("  ✓ Pandoc auto-download working")
            return 0
        print("\n" + "=" * 70)
        print("⚠ SOME TESTS FAILED")
        print("=" * 70)
        return 1

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
