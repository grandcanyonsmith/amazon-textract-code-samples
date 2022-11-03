import boto3
import time


def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print(f"Job status: {status}")

    while (status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print(f"Job status: {status}")

    return status


def get_job_results(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages = [response]
    print(f"Resultset page received: {len(pages)}")
    next_token = response['NextToken'] if 'NextToken' in response else None
    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        print(f"Resultset page received: {len(pages)}")
        next_token = response['NextToken'] if 'NextToken' in response else None
    return pages


if __name__ == "__main__":
    # Document
    s3_bucket_name = "ki-textract-demo-docs"
    document_name = "Amazon-Textract-Pdf.pdf"
    region = "us-east-1"
    client = boto3.client('textract', region_name=region)

    job_id = start_job(client, s3_bucket_name, document_name)
    print(f"Started job with id: {job_id}")
    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)

    # print(response)

    # Print detected text
    for result_page in response:
        for item in result_page["Blocks"]:
            if item["BlockType"] == "LINE":
                print('\033[94m' + item["Text"] + '\033[0m')
