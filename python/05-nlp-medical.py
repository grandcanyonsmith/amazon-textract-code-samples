import boto3

# Document
documentName = "medical-notes.png"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.detect_document_text(
        Document={
            'Bytes': document.read(),
        }
    )

#print(response)

# Print text
print("\nText\n========")
text = ""
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[94m' +  item["Text"] + '\033[0m')
        text = f"{text} " + item["Text"]

# Amazon Comprehend client
comprehend = boto3.client('comprehendmedical')

# Detect medical entities
entities =  comprehend.detect_entities(Text=text)
print("\nMedical Entities\n========")
for entity in entities["Entities"]:
    print(f'- {entity["Text"]}')
    print(f'   Type: {entity["Type"]}')
    print(f'   Category: {entity["Category"]}')
    if entity["Traits"]:
        print("   Traits:")
        for trait in entity["Traits"]:
            print(f'    - {trait["Name"]}')
    print("\n")
