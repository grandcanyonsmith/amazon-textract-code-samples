import boto3
from trp import Document

# Document
documentName = "employmentapp.png"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            'Bytes': document.read(),
        },
        FeatureTypes=["FORMS"])

#print(response)

doc = Document(response)

for page in doc.pages:
    # Print fields
    print("Fields:")
    for field in page.form.fields:
        print(f"Key: {field.key}, Value: {field.value}")

    # Get field by key
    print("\nGet Field by Key:")
    key = "Phone Number:"
    if field := page.form.getFieldByKey(key):
        print(f"Key: {field.key}, Value: {field.value}")

    # Search fields by key
    print("\nSearch Fields:")
    key = "address"
    fields = page.form.searchFieldsByKey(key)
    for field in fields:
        print(f"Key: {field.key}, Value: {field.value}")
