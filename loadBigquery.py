from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account

def authenticate_gcp(credentials_path):
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    return credentials

def load_csv_from_gcs_to_bigquery(project_id, dataset_id, table_id, bucket_name, blob_name, credentials_path):
    # Authenticate GCP
    credentials = authenticate_gcp(credentials_path)
    client = bigquery.Client(project=project_id, credentials=credentials)

    # Set the table reference
    table_ref = client.dataset(dataset_id).table(table_id)

    # Specify the job configuration
    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # Automatically detect schema
        source_format=bigquery.SourceFormat.CSV,  # Specify CSV as the source format
    )

    # Access the CSV file in Cloud Storage
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file_content = blob.download_as_text()

    # Start the load job
    job = client.load_table_from_file(file_content, table_ref, job_config=job_config)

    # Wait for the job to complete
    job.result()

    print(f"Data loaded to BigQuery table {project_id}.{dataset_id}.{table_id} from {bucket_name}/{blob_name}")

if __name__ == "__main__":
    # Replace these values with your own project, dataset, table, bucket, blob, and credentials path
    project_id = "your-project-id"
    dataset_id = "your-dataset-id"
    table_id = "your-table-id"
    bucket_name = "your-bucket-name"
    blob_name = "path/to/your/file.csv"
    credentials_path = "path/to/your/credentials.json"

    load_csv_from_gcs_to_bigquery(project_id, dataset_id, table_id, bucket_name, blob_name, credentials_path)
