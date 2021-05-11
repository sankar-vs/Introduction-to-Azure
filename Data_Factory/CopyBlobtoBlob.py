'''
 @Author: Sankar
 @Date: 2021-05-07 09:15:10
 @Last Modified by: Sankar
 @Last Modified time: 2021-05-08 08:15:38  
 @Title : Copy data from one container to another container
'''
from azure.identity import ClientSecretCredential 
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta
import time
from decouple import config

def print_item(group):
    '''
    Description:
        Print an Azure object instance.
    Parameter:
        group
    Return:
        None
    '''
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    if hasattr(group, 'location'):
        print("\tLocation: {}".format(group.location))
    if hasattr(group, 'tags'):
        print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)

def print_properties(props):
    '''
    Description:
        Print a ResourceGroup properties instance.
    Parameter:
        props
    Return:
        None
    '''
    if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")

def print_activity_run_details(activity_run):
    '''
    Description:
        Print activity run details.
    Parameter:
        activity_run
    Return:
        None
    '''
    print("\n\tActivity run details\n")
    print("\tActivity run status: {}".format(activity_run.status))
    if activity_run.status == 'Succeeded':
        print("\tNumber of bytes read: {}".format(activity_run.output['dataRead']))
        print("\tNumber of bytes written: {}".format(activity_run.output['dataWritten']))
        print("\tCopy duration: {}".format(activity_run.output['copyDuration']))
    else:
        print("\tErrors: {}".format(activity_run.error['message']))

def main():
    '''
    Description:
        Copies data from one container to another.
    Parameter:
        None
    Return:
        None
    '''
    # Azure subscription ID
    subscription_id = config('subscription_ID')

    # This program creates this resource group. If it's an existing resource group, comment out the code that creates the resource group
    rg_name = config('resource_group')

    # The data factory name. It must be globally unique.
    df_name = config('factory_name')

    # Specify your Active Directory client ID, client secret, and tenant ID
    credentials = ClientSecretCredential(client_id=config('service_principal_ID'), client_secret=config('service_principal_key'), tenant_id=config('tenant_ID')) 

    # Specify following for Soverign Clouds, import right cloud constant and then use it to connect.
    # from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD as CLOUD
    # credentials = DefaultAzureCredential(authority=CLOUD.endpoints.active_directory, tenant_id=tenant_id)

    resource_client = ResourceManagementClient(credentials, subscription_id)
    adf_client = DataFactoryManagementClient(credentials, subscription_id)

    rg_params = {'location':'eastus'}
    df_params = {'location':'eastus'}

    # create the resource group
    # comment out if the resource group already exits
    resource_client.resource_groups.create_or_update(rg_name, rg_params)

    #Create a data factory
    df_resource = Factory(location='westus')
    df = adf_client.factories.create_or_update(rg_name, df_name, df_resource)
    print_item(df)
    while df.provisioning_state != 'Succeeded':
        df = adf_client.factories.get(rg_name, df_name)
        time.sleep(1)

    # Create an Azure Storage linked service
    ls_name = config('ls_name')

    # IMPORTANT: specify the name and key of your Azure Storage account.
    storage_string = SecureString(value=config('df_value'))

    ls_azure_storage = LinkedServiceResource(properties=AzureStorageLinkedService(connection_string=storage_string)) 
    ls = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name, ls_azure_storage)
    print_item(ls)

    # Create an Azure blob dataset (input)
    ds_name = config('ds_name')
    ds_ls = LinkedServiceReference(reference_name=ls_name)
    blob_path = config('blob_path')
    blob_filename = config('blob_filename')
    ds_azure_blob = DatasetResource(properties=AzureBlobDataset(
        linked_service_name=ds_ls, folder_path=blob_path, file_name=blob_filename)) 
    ds = adf_client.datasets.create_or_update(
        rg_name, df_name, ds_name, ds_azure_blob)
    print_item(ds)

    # Create an Azure blob dataset (output)
    dsOut_name = config('dsOut_name')
    output_blobpath = config('output_blobpath')
    dsOut_azure_blob = DatasetResource(properties=AzureBlobDataset(linked_service_name=ds_ls, folder_path=output_blobpath))
    dsOut = adf_client.datasets.create_or_update(
        rg_name, df_name, dsOut_name, dsOut_azure_blob)
    print_item(dsOut)

    # Create a copy activity
    act_name = config('act_name')
    blob_source = BlobSource()
    blob_sink = BlobSink()
    dsin_ref = DatasetReference(reference_name=ds_name)
    dsOut_ref = DatasetReference(reference_name=dsOut_name)
    copy_activity = CopyActivity(name=act_name,inputs=[dsin_ref], outputs=[dsOut_ref], source=blob_source, sink=blob_sink)

    #Create a pipeline with the copy activity
    
    #Note1: To pass parameters to the pipeline, add them to the json string params_for_pipeline shown below in the format { “ParameterName1” : “ParameterValue1” } for each of the parameters needed in the pipeline.
    #Note2: To pass parameters to a dataflow, create a pipeline parameter to hold the parameter name/value, and then consume the pipeline parameter in the dataflow parameter in the format @pipeline().parameters.parametername.

    p_name = config('p_name')
    params_for_pipeline = {}
    p_obj = PipelineResource(activities=[copy_activity], parameters=params_for_pipeline)
    p = adf_client.pipelines.create_or_update(rg_name, df_name, p_name, p_obj)
    print_item(p)

    # Create a pipeline run
    run_response = adf_client.pipelines.create_run(rg_name, df_name, p_name, parameters={})

    # Monitor the pipeline run
    time.sleep(30)
    pipeline_run = adf_client.pipeline_runs.get(
        rg_name, df_name, run_response.run_id)
    print("\n\tPipeline run status: {}".format(pipeline_run.status))
    filter_params = RunFilterParameters(
        last_updated_after=datetime.now() - timedelta(1), last_updated_before=datetime.now() + timedelta(1))
    query_response = adf_client.activity_runs.query_by_pipeline_run(
        rg_name, df_name, pipeline_run.run_id, filter_params)
    print_activity_run_details(query_response.value[0])

# Start the main method
if __name__ == '__main__':
    main()