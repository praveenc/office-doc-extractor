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
Example: Using Office Document Extractor as an LLM Tool/Function.

This example shows how to integrate the extractor with OpenAI's function calling.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from office_doc_extractor import DocumentConverter


def extract_document_text(file_path: str) -> dict:
    """
    Extract text from Office document.

    This function can be called by an LLM to read document content.

    Args:
        file_path: Path to the document file

    Returns:
        Dictionary with extracted text and metadata

    """
    try:
        converter = DocumentConverter()
        text = converter.extract_text(file_path)

        return {
            "success": True,
            "text": text,
            "length": len(text),
            "filename": Path(file_path).name,
        }
    except Exception as e:
        return {"success": False, "error": str(e), "filename": Path(file_path).name}


# OpenAI Function Definition
FUNCTION_DEFINITION = {
    "type": "function",
    "function": {
        "name": "extract_document_text",
        "description": "Extract text content from Microsoft Office documents (DOCX, XLSX, PPTX) and HTML files. Use this when you need to read the contents of a document file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the document file (e.g., 'report.docx', 'data.xlsx')",
                },
            },
            "required": ["file_path"],
        },
    },
}


def main():
    """Example usage."""
    print("=" * 70)
    print("LLM Tool Example: Document Text Extraction")
    print("=" * 70)

    # Example 1: Direct function call
    print("\n[Example 1] Direct Function Call")
    print("-" * 70)

    result = extract_document_text("sample_document.docx")
    print(json.dumps(result, indent=2))

    # Example 2: Simulated LLM function call
    print("\n[Example 2] Simulated LLM Function Call")
    print("-" * 70)

    # This is what the LLM would send
    function_call = {
        "name": "extract_document_text",
        "arguments": json.dumps({"file_path": "report.docx"}),
    }

    print(f"LLM requests: {function_call['name']}")
    print(f"With arguments: {function_call['arguments']}")

    # Execute the function
    args = json.loads(function_call["arguments"])
    result = extract_document_text(**args)

    print("\nFunction returns:")
    print(json.dumps(result, indent=2))

    # Example 3: Integration with OpenAI (pseudo-code)
    print("\n[Example 3] OpenAI Integration (Pseudo-code)")
    print("-" * 70)

    integration_code = """
import openai

# Define tools
tools = [FUNCTION_DEFINITION]

# Chat with function calling
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Summarize the document report.docx"}
    ],
    tools=tools
)

# If LLM wants to call function
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]

    # Execute function
    args = json.loads(tool_call.function.arguments)
    result = extract_document_text(**args)

    # Send result back to LLM
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Summarize the document report.docx"},
            response.choices[0].message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        ],
        tools=tools
    )

    print(response.choices[0].message.content)
"""

    print(integration_code)


if __name__ == "__main__":
    main()
