# Amazon Textract Developer Reference Guide

## Overview

Amazon Textract is a machine learning (ML) powered OCR (Optical Character Recognition) service provided by Amazon Web Services. It extracts text, tables, and forms from organized documents, including PDFs, images (JPEG, PNG), and handwritten documents [[1]](https://dev.to/honeybadger/building-an-ocr-service-with-amazon-textract-and-aws-lambda-40p2). Textract goes beyond simple text extraction by understanding the structure of documents, making it more powerful than traditional OCR technologies [[2]](https://medium.com/amazon-help-and-tutorials/how-to-read-pdf-documents-with-amazon-textract-a-step-by-step-guide-3ab54c632151).

## Prerequisites

Before using Amazon Textract, ensure you have:

1. An active AWS account [[2]](https://medium.com/amazon-help-and-tutorials/how-to-read-pdf-documents-with-amazon-textract-a-step-by-step-guide-3ab54c632151)
2. Basic knowledge of Python (if using the Python SDK) [[1]](https://dev.to/honeybadger/building-an-ocr-service-with-amazon-textract-and-aws-lambda-40p2)
3. AWS CLI v2 setup (for command-line interactions) [[1]](https://dev.to/honeybadger/building-an-ocr-service-with-amazon-textract-and-aws-lambda-40p2)
4. Appropriate IAM permissions configured [[1]](https://dev.to/honeybadger/building-an-ocr-service-with-amazon-textract-and-aws-lambda-40p2) [[3]](https://medium.com/@pysquad/amazon-textract-with-python-window-to-document-data-extraction-73c47495b1eb)

## IAM Permissions

To use Amazon Textract, you need to create an IAM role with appropriate permissions:

1. Create an IAM role specifically for Amazon Textract access [[3]](https://medium.com/@pysquad/amazon-textract-with-python-window-to-document-data-extraction-73c47495b1eb)
2. For asynchronous operations, ensure the role has permissions to:
   - Access S3 buckets where documents are stored
   - Publish to SNS topics for job completion notifications
   - Access SQS queues for polling job status [[5]](https://docs.aws.amazon.com/code-library/latest/ug/textract_example_textract_StartDocumentAnalysis_section.html)

## Using Amazon Textract with Python (Boto3)

### Setting Up Boto3 Client

```python
import boto3

# Initialize the Textract client
textract_client = boto3.client('textract')
```

### Available Methods

Amazon Textract provides several API methods through the Boto3 client [[4]](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html):

- `analyze_document`: Analyzes documents for text, forms, and tables
- `analyze_expense`: Analyzes receipts and invoices
- `analyze_id`: Analyzes identity documents
- `detect_document_text`: Detects text in documents
- `start_document_analysis`: Starts asynchronous document analysis
- `start_document_text_detection`: Starts asynchronous text detection
- `get_document_analysis`: Gets results of asynchronous document analysis
- `get_document_text_detection`: Gets results of asynchronous text detection

### Synchronous Document Analysis

For smaller documents that can be processed quickly:

```python
response = textract_client.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': 'my-bucket',
            'Name': 'my-document.pdf'
        }
    }
)

# Process the response
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print(item["Text"])
```

### Asynchronous Document Analysis

For larger documents or when you need to analyze forms and tables [[5]](https://docs.aws.amazon.com/code-library/latest/ug/textract_example_textract_StartDocumentAnalysis_section.html) [[6]](https://docs.aws.amazon.com/code-library/latest/ug/python_3_textract_code_examples.html):

```python
class TextractWrapper:
    """Encapsulates Textract functions."""

    def __init__(self, textract_client, s3_resource, sqs_resource):
        """
        :param textract_client: A Boto3 Textract client.
        :param s3_resource: A Boto3 Amazon S3 resource.
        :param sqs_resource: A Boto3 Amazon SQS resource.
        """
        self.textract_client = textract_client
        self.s3_resource = s3_resource
        self.sqs_resource = sqs_resource

    def start_analysis_job(
        self,
        bucket_name,
        document_file_name,
        feature_types,
        sns_topic_arn,
        sns_role_arn,
    ):
        """
        Starts an asynchronous job to detect text and additional elements, such as
        forms or tables, in an image stored in an Amazon S3 bucket. Textract publishes
        a notification to the specified Amazon SNS topic when the job completes.
        The image must be in PNG, JPG, or PDF format.

        :param bucket_name: The name of the Amazon S3 bucket that contains the image.
        :param document_file_name: The name of the document image stored in Amazon S3.
        :param feature_types: The types of additional document features to detect.
        :param sns_topic_arn: The Amazon Resource Name (ARN) of an Amazon SNS topic
                              where job completion notification is published.
        :param sns_role_arn: The ARN of an AWS Identity and Access Management (IAM)
                             role that can be assumed by Textract and grants permission
                             to publish to the Amazon SNS topic.
        :return: The ID of the job.
        """
        try:
            response = self.textract_client.start_document_analysis(
                DocumentLocation={
                    "S3Object": {"Bucket": bucket_name, "Name": document_file_name}
                },
                NotificationChannel={
                    "SNSTopicArn": sns_topic_arn,
                    "RoleArn": sns_role_arn,
                },
                FeatureTypes=feature_types,
            )
            job_id = response["JobId"]
            logger.info(
                "Started text analysis job %s on %s.", job_id, document_file_name
            )
        except ClientError:
            logger.exception("Couldn't analyze text in %s.", document_file_name)
            raise
        else:
            return job_id
```

## Key Features

### 1. Text Detection

Extract raw text from documents, including:

- Lines and words
- Text location (bounding boxes)
- Confidence scores for extracted text

### 2. Form Analysis

Extract key-value pairs from forms, such as:

- Form fields and their values
- Checkboxes and selection elements
- Field relationships

### 3. Table Extraction

Extract tables from documents with:

- Cell content
- Row and column structure
- Table coordinates

### 4. Document Analysis

Analyze the structure of documents:

- Identify document sections
- Recognize headers, footers, and titles
- Understand document layout

### 5. Expense Analysis

Specifically designed for financial documents:

- Extract information from receipts and invoices
- Identify vendor names, dates, amounts, etc.

### 6. ID Document Analysis

Extract information from identity documents:

- Driver's licenses
- Passports
- Other government-issued IDs

## Integration Patterns

### 1. Direct API Integration

Process documents directly through the Textract API for real-time analysis of smaller documents.

### 2. Asynchronous Processing with SNS/SQS

For larger documents or batch processing:

1. Upload documents to S3
2. Start an asynchronous Textract job
3. Receive notifications via SNS when processing completes
4. Poll SQS queue for job completion messages
5. Retrieve and process results [[7]](https://docs.aws.amazon.com/code-library/latest/ug/textract_example_cross_TextractExplorer_section.html)

### 3. Lambda Integration

Create serverless document processing workflows:

1. Trigger Lambda functions when documents are uploaded to S3
2. Process documents with Textract
3. Store or forward results as needed [[1]](https://dev.to/honeybadger/building-an-ocr-service-with-amazon-textract-and-aws-lambda-40p2)

## Limitations

- **Supported Formats**: PNG, JPEG, PDF, and TIFF formats only [[5]](https://docs.aws.amazon.com/code-library/latest/ug/textract_example_textract_StartDocumentAnalysis_section.html)
- **Document Size**:
  - Synchronous API: Documents must be less than 10MB
  - Asynchronous API: Documents must be less than 500MB
- **PDF Page Limits**:
  - Synchronous API: Limited to first 1-2 pages (depending on complexity)
  - Asynchronous API: Up to 3000 pages
- **Language Support**: Primary focus on English, with varying levels of support for other languages
- **Processing Time**: Asynchronous jobs may take several minutes for large documents
- **Handwriting Recognition**: Works best with clear, printed text; handwriting recognition has limitations
- **Image Quality**: Poor image quality, low resolution, or heavy compression can reduce accuracy

## Best Practices

1. **Image Quality**: Use high-resolution, clear images for best results
2. **Document Preparation**: Ensure documents are properly aligned and have good contrast
3. **Asynchronous Processing**: Use asynchronous APIs for large documents or batch processing
4. **Error Handling**: Implement robust error handling for API failures
5. **Confidence Thresholds**: Filter results based on confidence scores for higher accuracy
6. **Testing**: Test with a variety of document types to understand performance characteristics

## Sample Applications

- Text extraction and analysis applications
- Document digitization workflows
- Form processing automation
- Receipt and invoice processing systems
- ID verification systems
- Document explorer applications [[7]](https://docs.aws.amazon.com/code-library/latest/ug/textract_example_cross_TextractExplorer_section.html)

### mentorURLsources

[1] Title: "Building an OCR service with Amazon Textract and AWS Lambda - DEV Community"
URL: https://dev.to/honeybadger/building-an-ocr-service-with-amazon-textract-and-aws-lambda-40p2

[2] Title: "How to Read PDF Documents with Amazon Textract: A Step-by-Step Guide"
URL: <https://medium.com/amazon-help-and-tutorials/how-to-read-pdf-documents-with-amazon-textract-a-step-by-step-guide-3ab54c632151>

[3] Title: "Amazon Textract with Python: Window to Document Data Extraction"
URL: <https://medium.com/@pysquad/amazon-textract-with-python-window-to-document-data-extraction-73c47495b1eb>

[4] Title: "Textract - Boto3 1.37.31 documentation"
URL: <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html>

[5] Title: "Use StartDocumentAnalysis with an AWS SDK or CLI - AWS SDK Code Examples"
URL: <https://docs.aws.amazon.com/code-library/latest/ug/textract_example_textract_StartDocumentAnalysis_section.html>

[6] Title: "Amazon Textract examples using SDK for Python (Boto3) - AWS SDK Code Examples"
URL: <https://docs.aws.amazon.com/code-library/latest/ug/python_3_textract_code_examples.html>

[7] Title: "Create an Amazon Textract explorer application - AWS SDK Code Examples"
URL: <https://docs.aws.amazon.com/code-library/latest/ug/textract_example_cross_TextractExplorer_section.html>

## Overview

Amazon Textract is a machine learning (ML) powered OCR (Optical Character Recognition) service provided by Amazon Web Services. It extracts text, tables, and forms from organized documents, including PDFs, images (JPEG, PNG), and handwritten documents. Textract goes beyond simple text extraction by understanding the structure of documents, making it more powerful than traditional OCR technologies.

## Prerequisites

Before using Amazon Textract, ensure you have:

1. An active AWS account
2. Basic knowledge of Python (if using the Python SDK)
3. AWS CLI v2 setup (for command-line interactions)
4. Appropriate IAM permissions configured

## IAM Permissions

To use Amazon Textract, you need to create an IAM role with appropriate permissions:

1. Create an IAM role specifically for Amazon Textract access
2. For asynchronous operations, ensure the role has permissions to:
   - Access S3 buckets where documents are stored
   - Publish to SNS topics for job completion notifications
   - Access SQS queues for polling job status

## Architecture

The following diagram illustrates the Amazon Textract workflow:

![Amazon Textract Workflow](docs/images/amzn_textract_arch.png)

## Using Amazon Textract with Python (Boto3)

### Setting Up Boto3 Client

```python
import boto3

# Initialize the Textract client
textract_client = boto3.client('textract')
```

### Available Methods

Amazon Textract provides several API methods through the Boto3 client:

- `analyze_document`: Analyzes documents for text, forms, and tables
- `analyze_expense`: Analyzes receipts and invoices
- `analyze_id`: Analyzes identity documents
- `detect_document_text`: Detects text in documents
- `start_document_analysis`: Starts asynchronous document analysis
- `start_document_text_detection`: Starts asynchronous text detection
- `get_document_analysis`: Gets results of asynchronous document analysis
- `get_document_text_detection`: Gets results of asynchronous text detection

### Synchronous Document Analysis

For smaller documents that can be processed quickly:

```python
response = textract_client.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': 'my-bucket',
            'Name': 'my-document.pdf'
        }
    }
)

# Process the response
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print(item["Text"])
```

### Asynchronous Document Analysis

For larger documents or when you need to analyze forms and tables:

```python
# Start an asynchronous job
response = textract_client.start_document_analysis(
    DocumentLocation={
        'S3Object': {
            'Bucket': 'my-bucket',
            'Name': 'my-document.pdf'
        }
    },
    FeatureTypes=['TABLES', 'FORMS'],
    NotificationChannel={
        'SNSTopicArn': 'arn:aws:sns:region:account-id:topic-name',
        'RoleArn': 'arn:aws:iam::account-id:role/role-name'
    }
)

job_id = response['JobId']

# Get results after receiving notification
result = textract_client.get_document_analysis(
    JobId=job_id,
    MaxResults=1000
)

# Process results
for item in result['Blocks']:
    if item['BlockType'] == 'LINE':
        print(item['Text'])
```

## Key Features

### 1. Text Detection

Extract raw text from documents, including:

- Lines and words
- Text location (bounding boxes)
- Confidence scores for extracted text

### 2. Form Analysis

Extract key-value pairs from forms, such as:

- Form fields and their values
- Checkboxes and selection elements
- Field relationships

```python
# Extract form data
response = textract_client.analyze_document(
    Document={
        'S3Object': {
            'Bucket': 'my-bucket',
            'Name': 'my-form.pdf'
        }
    },
    FeatureTypes=['FORMS']
)

# Process key-value pairs
for block in response['Blocks']:
    if block['BlockType'] == 'KEY_VALUE_SET':
        # Process key-value pairs
        pass
```

### 3. Table Extraction

Extract tables from documents with:

- Cell content
- Row and column structure
- Table coordinates

```python
# Extract tables
response = textract_client.analyze_document(
    Document={
        'S3Object': {
            'Bucket': 'my-bucket',
            'Name': 'my-document-with-tables.pdf'
        }
    },
    FeatureTypes=['TABLES']
)

# Process tables
for block in response['Blocks']:
    if block['BlockType'] == 'TABLE':
        # Process table structure
        pass
```

### 4. Document Analysis

Analyze the structure of documents:

- Identify document sections
- Recognize headers, footers, and titles
- Understand document layout

### 5. Expense Analysis

Specifically designed for financial documents:

- Extract information from receipts and invoices
- Identify vendor names, dates, amounts, etc.

```python
# Analyze expense documents
response = textract_client.analyze_expense(
    Document={
        'S3Object': {
            'Bucket': 'my-bucket',
            'Name': 'my-receipt.jpg'
        }
    }
)

# Process expense fields
for expense_document in response['ExpenseDocuments']:
    for expense_field in expense_document['SummaryFields']:
        print(f"Type: {expense_field['Type']['Text']}, Value: {expense_field['ValueDetection']['Text']}")
```

### 6. ID Document Analysis

Extract information from identity documents:

- Driver's licenses
- Passports
- Other government-issued IDs

```python
# Analyze ID documents
response = textract_client.analyze_id(
    DocumentPages=[
        {
            'S3Object': {
                'Bucket': 'my-bucket',
                'Name': 'my-id.jpg'
            }
        }
    ]
)

# Process ID fields
for document in response['IdentityDocuments']:
    for field in document['IdentityDocumentFields']:
        print(f"Type: {field['Type']['Text']}, Value: {field['ValueDetection']['Text']}")
```

## Integration Patterns

### 1. Direct API Integration

Process documents directly through the Textract API for real-time analysis of smaller documents.

### 2. Asynchronous Processing with SNS/SQS

For larger documents or batch processing:

1. Upload documents to S3
2. Start an asynchronous Textract job
3. Receive notifications via SNS when processing completes
4. Poll SQS queue for job completion messages
5. Retrieve and process results

### 3. Lambda Integration

Create serverless document processing workflows:

1. Trigger Lambda functions when documents are uploaded to S3
2. Process documents with Textract
3. Store or forward results as needed

## Limitations

- **Supported Formats**: PNG, JPEG, PDF, and TIFF formats only
- **Document Size**:
  - Synchronous API: Documents must be less than 10MB
  - Asynchronous API: Documents must be less than 500MB
- **PDF Page Limits**:
  - Synchronous API: Limited to first 1-2 pages (depending on complexity)
  - Asynchronous API: Up to 3000 pages
- **Language Support**: Primary focus on English, with varying levels of support for other languages
- **Processing Time**: Asynchronous jobs may take several minutes for large documents
- **Handwriting Recognition**: Works best with clear, printed text; handwriting recognition has limitations
- **Image Quality**: Poor image quality, low resolution, or heavy compression can reduce accuracy
- **Rate Limits**: API request quotas apply (varies by region)
- **Cost**: Pricing based on the number of pages processed

## Best Practices

1. **Image Quality**: Use high-resolution, clear images for best results
2. **Document Preparation**: Ensure documents are properly aligned and have good contrast
3. **Asynchronous Processing**: Use asynchronous APIs for large documents or batch processing
4. **Error Handling**: Implement robust error handling for API failures
5. **Confidence Thresholds**: Filter results based on confidence scores for higher accuracy
6. **Testing**: Test with a variety of document types to understand performance characteristics
7. **Optimize S3 Access**: Use appropriate S3 bucket policies and access controls
8. **Monitor Costs**: Set up AWS Budgets to track Textract usage costs

## Sample Applications

- Text extraction and analysis applications
- Document digitization workflows
- Form processing automation
- Receipt and invoice processing systems
- ID verification systems
- Document explorer applications

## Error Handling

```python
import boto3
from botocore.exceptions import ClientError

textract_client = boto3.client('textract')

try:
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'my-bucket',
                'Name': 'my-document.pdf'
            }
        }
    )
    # Process response
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidS3ObjectException':
        print("The S3 object doesn't exist or is not accessible")
    elif e.response['Error']['Code'] == 'InvalidParameterException':
        print("Invalid parameter value")
    elif e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
        print("Provisioned throughput exceeded")
    else:
        print(f"Unexpected error: {e}")
```

## Conclusion

Amazon Textract provides powerful document processing capabilities that go beyond traditional OCR. By understanding document structure and context, it enables developers to build sophisticated document processing applications with minimal effort. Whether you need to extract text, analyze forms, or process tables, Amazon Textract offers a comprehensive set of features to meet your document processing needs.
