#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "boto3>=1.26.0",
#   "pypandoc>=1.13",
#   "pandas>=2.0.0",
#   "openpyxl>=3.0.0",
#   "python-pptx>=0.6.0",
#   "pdfplumber>=0.10.0",
#   "loguru>=0.7.0",
# ]
# ///
"""
Example: Using Office Document Extractor with Amazon Bedrock Converse API.

This example shows how to integrate the document extractor as a tool
for Amazon Bedrock's Converse API, allowing Claude or other models to
read and analyze Office documents.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import boto3

from office_doc_extractor import DocumentConverter

# Tool definition for Bedrock Converse API
TOOL_DEFINITION = {
    "toolSpec": {
        "name": "extract_document_text",
        "description": "Extract text content from Office documents (DOCX, XLSX, PPTX, PDF) and HTML files. Use this when you need to read the contents of a document file to answer questions or analyze content.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the document file (e.g., 'report.docx', 'data.xlsx', 'slides.pptx', 'document.pdf')",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
}


def extract_document_text(file_path: str) -> dict:
    """
    Tool function to extract text from documents.

    Args:
        file_path: Path to the document file

    Returns:
        Dictionary with extraction results

    """
    try:
        converter = DocumentConverter()
        text = converter.extract_text(file_path)

        return {
            "success": True,
            "text": text,
            "length": len(text),
            "filename": Path(file_path).name,
            "format": Path(file_path).suffix,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File not found: {file_path}",
            "filename": Path(file_path).name,
        }
    except ValueError as e:
        return {"success": False, "error": str(e), "filename": Path(file_path).name}
    except Exception as e:
        return {
            "success": False,
            "error": f"Extraction failed: {e!s}",
            "filename": Path(file_path).name,
        }


def converse_with_tools(
    bedrock_client,
    model_id: str,
    messages: list,
    tools: list,
    max_iterations: int = 5,
) -> dict:
    """
    Converse with Bedrock using tools, handling tool use iterations.

    Args:
        bedrock_client: Boto3 Bedrock Runtime client
        model_id: Model identifier (e.g., 'us.anthropic.claude-sonnet-4-20250514-v1:0')
        messages: Conversation messages
        tools: Tool definitions
        max_iterations: Maximum tool use iterations

    Returns:
        Final response from the model

    """
    conversation_messages = messages.copy()

    for iteration in range(max_iterations):
        print(f"\n{'=' * 70}")
        print(f"Iteration {iteration + 1}")
        print(f"{'=' * 70}")

        # Call Bedrock Converse API
        response = bedrock_client.converse(
            modelId=model_id,
            messages=conversation_messages,
            toolConfig={"tools": tools},
        )

        # Get the response
        stop_reason = response["stopReason"]
        output_message = response["output"]["message"]

        print(f"Stop reason: {stop_reason}")

        # Add assistant's response to conversation
        conversation_messages.append(output_message)

        # Check if model wants to use a tool
        if stop_reason == "tool_use":
            # Process tool use requests
            tool_results = []

            for content_block in output_message["content"]:
                if "toolUse" in content_block:
                    tool_use = content_block["toolUse"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]
                    tool_use_id = tool_use["toolUseId"]

                    print(f"\nTool requested: {tool_name}")
                    print(f"Tool input: {json.dumps(tool_input, indent=2)}")

                    # Execute the tool
                    if tool_name == "extract_document_text":
                        result = extract_document_text(**tool_input)

                        if result["success"]:
                            print(
                                f"✓ Extracted {result['length']:,} characters from {result['filename']}",
                            )
                            tool_result_content = result["text"]
                        else:
                            print(f"✗ Extraction failed: {result['error']}")
                            tool_result_content = f"Error: {result['error']}"

                        tool_results.append(
                            {
                                "toolUseId": tool_use_id,
                                "content": [{"text": tool_result_content}],
                            },
                        )

            # Add tool results to conversation
            if tool_results:
                conversation_messages.append(
                    {
                        "role": "user",
                        "content": [{"toolResult": tr} for tr in tool_results],
                    },
                )

                # Continue conversation
                continue

        # If we get here, the model has finished (no more tool use)
        return response

    raise RuntimeError(f"Maximum iterations ({max_iterations}) reached")


def example_document_qa():
    """Example: Ask questions about a document."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Document Q&A")
    print("=" * 70)

    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Model to use
    model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"

    # User question
    user_question = "Read the document 'tests/sample_docs/file-sample_100kB.docx' and summarize the key points."

    print(f"\nUser: {user_question}")

    # Initial messages
    messages = [{"role": "user", "content": [{"text": user_question}]}]

    # Converse with tools
    try:
        response = converse_with_tools(
            bedrock_client=bedrock,
            model_id=model_id,
            messages=messages,
            tools=[TOOL_DEFINITION],
        )

        # Extract final answer
        final_message = response["output"]["message"]
        for content_block in final_message["content"]:
            if "text" in content_block:
                print(f"\nClaude: {content_block['text']}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_multi_document_analysis():
    """Example: Analyze multiple documents."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Multi-Document Analysis")
    print("=" * 70)

    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Model to use
    model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"

    # User question
    user_question = """
    Please analyze these documents:
    1. tests/sample_docs/file-sample_100kB.docx
    2. tests/sample_docs/WhatIsEntropy.pdf.pdf

    Compare the content and identify common themes.
    """

    print(f"\nUser: {user_question}")

    # Initial messages
    messages = [{"role": "user", "content": [{"text": user_question}]}]

    # Converse with tools
    try:
        response = converse_with_tools(
            bedrock_client=bedrock,
            model_id=model_id,
            messages=messages,
            tools=[TOOL_DEFINITION],
        )

        # Extract final answer
        final_message = response["output"]["message"]
        for content_block in final_message["content"]:
            if "text" in content_block:
                print(f"\nClaude: {content_block['text']}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_data_extraction():
    """Example: Extract specific data from a spreadsheet."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Data Extraction from Spreadsheet")
    print("=" * 70)

    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Model to use
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    # User question
    user_question = """
    Read the PDF document 'tests/sample_docs/WhatIsEntropy.pdf.pdf'
    and tell me:
    1. What is the main topic?
    2. How many pages does it have?
    3. Summarize the key concepts.
    """

    print(f"\nUser: {user_question}")

    # Initial messages
    messages = [{"role": "user", "content": [{"text": user_question}]}]

    # Converse with tools
    try:
        response = converse_with_tools(
            bedrock_client=bedrock,
            model_id=model_id,
            messages=messages,
            tools=[TOOL_DEFINITION],
        )

        # Extract final answer
        final_message = response["output"]["message"]
        for content_block in final_message["content"]:
            if "text" in content_block:
                print(f"\nClaude: {content_block['text']}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Run examples."""
    parser = argparse.ArgumentParser(
        description="Amazon Bedrock Converse API with Document Extraction Tool",
    )
    parser.add_argument(
        "--example",
        choices=["qa", "multi", "data", "all"],
        default="qa",
        help="Which example to run (default: qa)",
    )
    parser.add_argument(
        "--model",
        default="anthropic.claude-3-sonnet-20240229-v1:0",
        help="Bedrock model ID",
    )
    parser.add_argument("--region", default="us-east-1", help="AWS region")

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("AMAZON BEDROCK + OFFICE DOCUMENT EXTRACTOR")
    print("=" * 70)
    print(f"\nModel: {args.model}")
    print(f"Region: {args.region}")

    # Check AWS credentials
    try:
        boto3.client("sts").get_caller_identity()
        print("✓ AWS credentials configured")
    except Exception as e:
        print(f"✗ AWS credentials not configured: {e}")
        print("\nPlease configure AWS credentials:")
        print("  aws configure")
        return 1

    # Run examples
    if args.example == "qa" or args.example == "all":
        example_document_qa()

    if args.example == "multi" or args.example == "all":
        example_multi_document_analysis()

    if args.example == "data" or args.example == "all":
        example_data_extraction()

    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
