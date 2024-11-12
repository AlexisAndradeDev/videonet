from azure.storage.blob import BlobServiceClient

def delete_blob(blob_name: str, connection_string: str):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(
        container="videos", blob=blob_name
    )

    try:
        blob_client.delete_blob()
    finally:
        blob_client.close()
        blob_service_client.close()