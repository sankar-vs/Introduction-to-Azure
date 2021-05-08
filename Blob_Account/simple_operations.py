'''
@Author: Sankar
@Date: 2021-05-06 07:51:25
@Last Modified by: Sankar
@Last Modified time: 2021-05-08 08:38:09
@Title : Operations on Blob Account
'''
import os
from decouple import config
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
from azure.storage.blob import BlobServiceClient
from log import logger

class BlobServiceSamples(object):

    def __init__(self):
        self.connection_string = config("AZURE_STORAGE_CONNECTION_STRING")
        # Instantiate a BlobServiceClient using a connection string
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
    
    def get_storage_account_information(self):  

        # [START get_blob_service_account_info]
        account_info = self.blob_service_client.get_account_information()
        logger.info('Using Storage SKU: {}'.format(account_info['sku_name']))
        # [END get_blob_service_account_info]

    def blob_service_stats(self):
        # [START get_blob_service_stats]
        stats = self.blob_service_client.get_service_stats()
        logger.info("Service Stats:\n{}".format(stats))
        # [END get_blob_service_stats]

    def container_operations(self):

        try:
            # [START bsc_create_container]
            try:
                new_container = self.blob_service_client.create_container("containerfromblobservice")
                properties = new_container.get_container_properties()
                logger.info(properties)
            except ResourceExistsError:
                logger.error("Container already exists.")
            # [END bsc_create_container]

            # [START bsc_list_containers]
            # List all containers
            all_containers = self.blob_service_client.list_containers(include_metadata=True)
            for container in all_containers:
                logger.info(container['name'])
                print(container['metadata'])

            # Filter results with name prefix
            test_containers = self.blob_service_client.list_containers(name_starts_with='test-')
            for container in test_containers:
                self.blob_service_client.delete_container(container)
            # [END bsc_list_containers]

        finally:
            # [START bsc_delete_container]
            # Delete container if it exists
            try:
                self.blob_service_client.delete_container("containerfromblobservice")
            except ResourceNotFoundError:
                logger.error("Container already deleted.")
            # [END bsc_delete_container]

    def get_blob_and_container_clients(self):

        # [START bsc_get_container_client]
        # Get a client to interact with a specific container - though it may not yet exist
        container_client = self.blob_service_client.get_container_client("containertest")
        try:
            for blob in container_client.list_blobs():
                logger.info("Found blob: {}".format(blob.name))
        except ResourceNotFoundError:
            logger.error("Container not found.")
        # [END bsc_get_container_client]
        try:
            # Create new Container in the service
            container_client.create_container()

            # [START bsc_get_blob_client]
            blob_client = self.blob_service_client.get_blob_client(container="containertest", blob="my_blob")
            try:
                stream = blob_client.download_blob()
                logger.info("Stream Downloaded")
            except ResourceNotFoundError:
                logger.error("No blob found.")
            # [END bsc_get_blob_client]

        finally:
            # Delete the container
            self.blob_service_client.delete_container("containertest")
            logger.info("Container Deleted")

if __name__ == '__main__':
    sample = BlobServiceSamples()
    sample.get_storage_account_information()
    sample.blob_service_stats()
    sample.container_operations()
    sample.get_blob_and_container_clients()