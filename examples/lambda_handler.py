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
AWS Lambda Handler for Office Document Text Extraction.

Deploy this as an AWS Lambda function to create a serverless
text extraction service.
"""

import base64
import json
import tempfile
from pathlib import Path

from office_doc_extractor import DocumentConverter


def lambda_handler(event, context):
    """
    AWS Lambda handler for document text extraction.

    Expected event format:
    {
        "document": "base64_encoded_document_data",
        "file_extension": ".docx",  # or .xlsx, .pptx, .html
        "options": {
            "return_metadata": true  # optional
        }
    }

    Returns:
    {
        "statusCode": 200,
        "body": {
            "text": "extracted text content",
            "length": 12345,
            "filename": "document.docx"
        }
    }

    """
    try:
        # Parse event
        document_data = base64.b64decode(event["document"])
        file_extension = event.get("file_extension", ".docx")
        options = event.get("options", {})

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            suffix=file_extension,
            delete=False,
        ) as temp_file:
            temp_file.write(document_data)
            temp_path = temp_file.name

        try:
            # Extract text
            converter = DocumentConverter()
            text = converter.extract_text(temp_path)

            # Prepare response
            response_body = {
                "text": text,
                "length": len(text),
                "format": file_extension,
            }

            # Add metadata if requested
            if options.get("return_metadata"):
                response_body["metadata"] = {
                    "file_size": len(document_data),
                    "word_count": len(text.split()),
                    "line_count": len(text.splitlines()),
                }

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(response_body),
            }

        finally:
            # Clean up temporary file
            Path(temp_path).unlink(missing_ok=True)

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing required field: {e!s}"}),
        }

    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Invalid input: {e!s}"}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal error: {e!s}"}),
        }


# For local testing
if __name__ == "__main__":
    # Test event
    with Path.open("test_document.docx", "rb") as f:
        document_data = base64.b64encode(f.read()).decode()

    test_event = {
        "document": document_data,
        "file_extension": ".docx",
        "options": {"return_metadata": True},
    }

    result = lambda_handler(test_event, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
