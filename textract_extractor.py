#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "boto3>=1.26.0",
#   "loguru>=0.7.0",
# ]
# ///
"""
Amazon Textract Document Text Extractor.

Extracts text from documents using Amazon Textract service.
Supports: PDF, PNG, JPG, JPEG, TIFF formats.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Final

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from loguru import logger


class TextractExtractor:
    """Amazon Textract document text extractor."""

    SUPPORTED_FORMATS: Final[set[str]] = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".tif",
    }
    MAX_SYNC_SIZE_MB: Final[int] = 10  # Textract synchronous API limit

    def __init__(
        self,
        region_name: str = "us-west-2",
        min_confidence: float = 0.0,
    ) -> None:
        try:
            self.textract = boto3.client("textract", region_name=region_name)
            self.min_confidence = max(0.0, min(100.0, min_confidence))
            logger.info(f"Initialized Textract client in region: {region_name}")
        except NoCredentialsError as e:
            logger.error("AWS credentials not found")
            msg = "AWS credentials not found. Configure AWS CLI or set environment variables."
            raise RuntimeError(msg) from e

    def validate_file(self, file_path: str) -> Path:
        path = Path(file_path)

        if not path.exists():
            logger.error(f"File not found: {file_path}")
            msg = f"File not found: {file_path}"
            raise FileNotFoundError(msg)

        if not path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            msg = f"Path is not a file: {file_path}"
            raise ValueError(msg)

        suffix = path.suffix.lower()
        if suffix not in self.SUPPORTED_FORMATS:
            logger.error(f"Unsupported format: {suffix}")
            supported = ", ".join(sorted(self.SUPPORTED_FORMATS))
            msg = f"Unsupported format: {suffix}. Supported: {supported}"
            raise ValueError(msg)

        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.MAX_SYNC_SIZE_MB:
            logger.warning(
                f"File size ({file_size_mb:.2f}MB) exceeds {self.MAX_SYNC_SIZE_MB}MB limit",
            )
            msg = (
                f"File too large ({file_size_mb:.2f}MB). "
                f"Maximum size for synchronous processing is {self.MAX_SYNC_SIZE_MB}MB."
            )
            raise ValueError(msg)

        logger.info(f"Validated file: {path.name} ({file_size_mb:.2f}MB)")
        return path

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from document using Amazon Textract.

        Args:
            file_path: Path to document file

        Returns:
            Extracted text content

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported or file is too large
            RuntimeError: If Textract API call fails

        """
        path = self.validate_file(file_path)

        try:
            logger.info(f"Reading document: {path.name}")
            document_bytes = path.read_bytes()

            logger.info("Calling Textract detect_document_text API")
            response = self.textract.detect_document_text(
                Document={"Bytes": document_bytes},
            )

            logger.success("Successfully received Textract response")
            return self._extract_text_from_response(response)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_msg = e.response["Error"]["Message"]
            logger.error(f"Textract API error: {error_code} - {error_msg}")

            match error_code:
                case "InvalidS3ObjectException":
                    msg = "S3 object doesn't exist or is not accessible"
                    raise RuntimeError(msg) from e
                case "InvalidParameterException":
                    msg = f"Invalid parameter: {error_msg}"
                    raise ValueError(msg) from e
                case "UnsupportedDocumentException":
                    msg = f"Document format not supported by Textract: {path.suffix}"
                    raise ValueError(msg) from e
                case "DocumentTooLargeException":
                    msg = (
                        f"Document too large. Maximum size is {self.MAX_SYNC_SIZE_MB}MB"
                    )
                    raise ValueError(msg) from e
                case "ProvisionedThroughputExceededException":
                    msg = "Textract throughput exceeded. Please retry later."
                    raise RuntimeError(msg) from e
                case "ThrottlingException":
                    msg = "Request throttled. Please reduce request rate."
                    raise RuntimeError(msg) from e
                case _:
                    msg = f"Textract error: {error_msg}"
                    raise RuntimeError(msg) from e

    def _extract_text_from_response(self, response: dict) -> str:
        """
        Extract text content from Textract response with confidence filtering.

        Args:
            response: Textract API response dictionary

        Returns:
            Extracted and filtered text content

        """
        text_blocks = []
        total_blocks = 0
        filtered_blocks = 0

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                total_blocks += 1
                confidence = block.get("Confidence", 0.0)

                if confidence >= self.min_confidence:
                    text_blocks.append(block.get("Text", ""))
                else:
                    filtered_blocks += 1
                    logger.debug(
                        f"Filtered low confidence text: {block.get('Text', '')} "
                        f"(confidence: {confidence:.2f}%)",
                    )

        logger.info(
            f"Extracted {len(text_blocks)} text blocks "
            f"(filtered {filtered_blocks} low confidence blocks)",
        )

        return "\n".join(text_blocks)


def main() -> int:
    """Main function to handle command line arguments and execute text extraction."""
    parser = argparse.ArgumentParser(
        description="Extract text from documents using Amazon Textract",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats: PDF, PNG, JPG, JPEG, TIFF

Examples:
  python textract_extractor.py document.pdf
  python textract_extractor.py --region us-west-2 image.png
  python textract_extractor.py --output extracted.txt document.pdf
  python textract_extractor.py --min-confidence 80 document.pdf
  python textract_extractor.py --quiet document.pdf
        """,
    )

    parser.add_argument("document_path", help="Path to the document file")
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.0,
        help="Minimum confidence score 0-100 for text extraction (default: 0.0)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress logging output",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    logger.remove()  # Remove default handler
    if not args.quiet:
        log_level = "DEBUG" if args.verbose else "INFO"
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level=log_level,
        )

    try:
        extractor = TextractExtractor(
            region_name=args.region,
            min_confidence=args.min_confidence,
        )
        extracted_text = extractor.extract_text(args.document_path)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(extracted_text, encoding="utf-8")
            logger.success(f"Text extracted and saved to: {args.output}")
            if not args.quiet:
                print(f"✓ Text extracted and saved to: {args.output}")
        else:
            if not args.quiet:
                print("\n" + "=" * 60)
                print("EXTRACTED TEXT")
                print("=" * 60)
            print(extracted_text)

        return 0

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(str(e))
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
