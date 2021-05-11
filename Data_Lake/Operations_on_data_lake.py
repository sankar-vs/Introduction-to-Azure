'''
 @Author: Sankar
 @Date: 2021-05-06 09:15:10
 @Last Modified by: Sankar
 @Last Modified time: 2021-05-08 11:15:38  
 @Title : Simple Operations on DataLake
'''
import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from log import logger
from decouple import config

class DataLakeOperations:
    '''
    Class:
        DataLakeOperations
    Description:
        To perform Simple Operations on Data Lake Storage Account
    Functions:
        initialize_storage_account(storage_account_name, storage_account_key)
        create_file_system()
        create_directory()
        rename_directory()
        delete_directory()
        upload_file_to_directory()
        download_file_from_directory()
        list_directory_contents()
    Variable:
        None
    '''
    def __init__(self):
        self.storage_account_name = config("account_name")
        self.storage_account_key = config("account_key")
        self.initialize_storage_account(self.storage_account_name,self.storage_account_key)

    def initialize_storage_account(self, storage_account_name, storage_account_key):
        '''
        Description:
            To Create Connection to the Data Lake Server Client
        Parameter:
            None
        Return:
            None
        '''
        try:  
            client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
                "https", storage_account_name), credential=storage_account_key)
            self.service_client = client
            logger.info("Storage Account Connected")
        except Exception:
            logger.exception("Server Client Not Connected")

    def create_file_system(self):
        '''
        Description:
            To Create File System in Data Lake Storage
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.create_file_system(file_system="my-file-system")
            logger.info("File System Created")
        except Exception:
            logger.exception("File System Not Created")

    def create_directory(self):
        '''
        Description:
            To Create Directory in the File System
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.get_file_system_client(file_system="my-file-system")
            file_system_client.create_directory("my-directory")
            logger.info("Directory Created")
        except Exception:
            logger.exception("Directory Not Created")

    def rename_directory(self):
        '''
        Description:
            To Rename the created Directory
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.get_file_system_client(file_system="my-file-system")
            directory_client = file_system_client.get_directory_client("my-directory")
       
            new_dir_name = "my-directory-renamed"
            new_directory = directory_client.rename_directory(new_name=directory_client.file_system_name + '/' + new_dir_name)
            logger.info("New Directory Created")
        except Exception:
            logger.exception("Rename Directory Aborted")

    def delete_directory(self):
        '''
        Description:
            To Delete the directory in the File System
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.get_file_system_client(file_system="my-file-system")
            directory_client = file_system_client.get_directory_client("my-directory-renamed")

            directory_client.delete_directory()
            logger.info("Directory Deleted")
        except Exception:
            logger.exception("Directory Failed to Delete")

    def upload_file_to_directory(self):
        '''
        Description:
            To Upload a file to the Directory
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.get_file_system_client(file_system="my-file-system")
            directory_client = file_system_client.get_directory_client("my-directory") 
            file_client = directory_client.get_file_client("uploaded-file.txt")
            local_file = open("D:\\file-to-upload.txt",'r')
            file_contents = local_file.read()
            file_client.upload_data(file_contents, overwrite=True)
            logger.info("File Uploaded")
        except Exception:
            logger.exception("File Not Uploaded")

    def download_file_from_directory(self):
        '''
        Description:
            To Download a file from the Directory
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.get_file_system_client(file_system="my-file-system")
            directory_client = file_system_client.get_directory_client("my-directory")
            local_file = open("D:\\file-to-download.txt",'wb')
            file_client = directory_client.get_file_client("uploaded-file.txt")
            download = file_client.download_file()
            downloaded_bytes = download.readall()
            local_file.write(downloaded_bytes)
            local_file.close()
        except Exception:
            logger.exception("File Not Downloaded")

    def list_directory_contents(self):
        '''
        Description:
            To list the Directory contents
        Parameter:
            None
        Return:
            None
        '''
        try:
            file_system_client = self.service_client.get_file_system_client(file_system="my-file-system")
            paths = file_system_client.get_paths(path="my-directory")

            for path in paths:
                print(path.name + '\n')
        except Exception:
            logger.exception("Listing Directory Failed")

if __name__ == '__main__':
    obj = DataLakeOperations()
    obj.create_file_system()
    obj.create_directory()
    obj.rename_directory()
    obj.delete_directory()
    obj.upload_file_to_directory()
    obj.download_file_from_directory()
    obj.list_directory_contents()
