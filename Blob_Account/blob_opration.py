'''
@Author: Sankar
@Date: 2021-05-08 09:51:25
@Last Modified by: Sankar
@Last Modified time: 2021-05-08 11:38:09
@Title : Operations on Blob Account
'''
import os
from decouple import config
from azure.storage.blob import BlobServiceClient 
from log import logger

# set up
SOURCE_FILE = 'D:/emp.txt'
DEST_FILE = 'D:/BlockDestination.txt'


class BlobSamples(object):

    def __init__(self):
        self.connection_string = config("AZURE_STORAGE_CONNECTION_STRING")
        # Instantiate a BlobServiceClient using a connection string
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def create_container_sample(self):
        # Instantiate a new ContainerClient
        container_client = self.blob_service_client.get_container_client("mycontainer")

        try:
            # Create new container in the service
            container_client.create_container()
            logger.info("Container Created")

            # List containers in the storage account
            list_response = self.blob_service_client.list_containers()

            logger.info(list_response)

        finally:
            # Delete the container
            container_client.delete_container()
            logger.info("Container Deleted")

    def block_blob_sample(self):
        # Instantiate a new ContainerClient
        container_client = self.blob_service_client.get_container_client("myblockcontainersync")

        try:
            # Create new Container in the service
            container_client.create_container()
            logger.info("Container Created")
            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client("myblockblob")

            # [START upload_a_blob]
            # Upload content to block blob
            with open(SOURCE_FILE, "rb") as data:
                blob_client.upload_blob(data, blob_type="BlockBlob")
            # [END upload_a_blob]

            # [START download_a_blob]
            with open(DEST_FILE, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())
            # [END download_a_blob]

            # [START delete_blob]
            blob_client.delete_blob()
            # [END delete_blob]

        finally:
            # Delete the container
            container_client.delete_container()

    def stream_block_blob(self):

        import uuid
        # Instantiate a new BlobServiceClient using a connection string - set chunk size to 1MB
        from azure.storage.blob import BlobServiceClient, BlobBlock
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string,
                                                                       max_single_get_size=1024*1024,
                                                                       max_chunk_get_size=1024*1024)

        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client("containersync")
        # Generate 4MB of data
        data = b'a'*4*1024*1024

        try:
            # Create new Container in the service
            container_client.create_container()

            # Instantiate a new source blob client
            source_blob_client = container_client.get_blob_client("source_blob")
            # Upload content to block blob
            source_blob_client.upload_blob(data, blob_type="BlockBlob")

            destination_blob_client = container_client.get_blob_client("destination_blob")
            # [START download_a_blob_in_chunk]
            # This returns a StorageStreamDownloader.
            stream = source_blob_client.download_blob()
            block_list = []

            # Read data in chunks to avoid loading all into memory at once
            for chunk in stream.chunks():
                # process your data (anything can be done here really. `chunk` is a byte array).
                block_id = str(uuid.uuid4())
                destination_blob_client.stage_block(block_id=block_id, data=chunk)
                block_list.append(BlobBlock(block_id=block_id))

            # [END download_a_blob_in_chunk]

            # Upload the whole chunk to azure storage and make up one blob
            destination_blob_client.commit_block_list(block_list)

        finally:
            # Delete container
            container_client.delete_container()

    def page_blob_sample(self):

        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client("mypagecontainersync")

        try:
            # Create new Container in the Service
            container_client.create_container()

            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client("mypageblob")

            # Upload content to the Page Blob
            data = b'abcd'*128
            blob_client.upload_blob(data, blob_type="PageBlob")

            # Download Page Blob
            with open(DEST_FILE, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())

            # Delete Page Blob
            blob_client.delete_blob()

        finally:
            # Delete container
            container_client.delete_container()

    def append_blob_sample(self):

        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client("myappendcontainersync")

        try:
            # Create new Container in the Service
            container_client.create_container()

            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client("myappendblob")

            # Upload content to the Page Blob
            with open(SOURCE_FILE, "rb") as data:
                blob_client.upload_blob(data, blob_type="AppendBlob")

            # Download Append Blob
            with open(DEST_FILE, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())

            # Delete Append Blob
            blob_client.delete_blob()

        finally:
            # Delete container
            container_client.delete_container()


if __name__ == '__main__':
    sample = BlobSamples()
    sample.create_container_sample()
    sample.block_blob_sample()
    sample.append_blob_sample()
    sample.page_blob_sample()
    sample.stream_block_blob()