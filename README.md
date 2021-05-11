## Introduction to Microsoft Azure
### Hadoop
* Installation of Hadoop
    * Pre-requisites: Must have Java Installed
    * Download Hadoop files from apache website
    * Create a new folder called hadoop and dump the downloaded files in to the newly created folder
    * Create subfolders inside hadoop
	* data/datanode
	* data/namenode
    * Inside hadoop/etc/hadoop edit the respective files core-site.xml, mapred-site.xml, hdfs-site.xml, yarn-site.xml and hadoop-env.cmd
    * Set the environmental variables
    * Download the winutils file for the secific version of hadoop
    * Run hadoop version in cmd prompt to check whether hadoop is successfully installed
* Perform Word Count

### Spark
* Installation of Spark on Windows
   * Prerequisites: Java and Anaconda Distribution
   * Download Spark from Appache Website
   * Extract the files to new folder in C Drice called Spark
   * Download the winutils.exe according to the version u downloaded and paster it inside spark-1x/bin
   * Set the env variables
   * Run spark-shell --version in cmd prompt to check whether Spark has been successfully installed in your system
* Using RDD solve word count program
   * Open jupyet notebook and solve the program

### Azure Blob Storage
* Perform basic upload of data on Azure blob Storage
* Create a new Blob Storage in Azure:
   * From Azure Home Page Click on Create a resource and search for Storage Accounts
   * Click on create a new account
   * Enter the basic information required to create a storage account in the Basic Tab
   * Click on Review+Create, wait until vaidation is over and then cllick on Create
* References:
   * https://docs.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?tabs=azure-portal
   * https://www.youtube.com/watch?v=_Xr_SxDeub4

### Azure Data Lake Storage
* Perform basic data upload on Azure Data Lake Storage
* Create a Data Lake Storage Account
    * From Azure Home Page Click on Create a resource and search for Storage Accounts
    * Click on create a new account
    * Enter the basic information required to create a storage account in the Basic Tab
    * Go to Advanced tab and enable the Heirarchichal Namespace to make it a Data Lake Storage Gen2
    * Click on Review+Create, wait until vaidation is over and then cllick on Create
* Reference:
    * https://docs.microsoft.com/en-us/learn/modules/upload-data-to-azure-data-lake-storage/
    * https://docs.microsoft.com/en-us/learn/paths/data-processing-with-azure-adls/

### Azure SQL Database
* Perform basic operation on SQL Database
* Create a SQL Database in Azure
   * From Azure Home page click on create a resource
   * Search for SQL Database and click on create
   * Fill in all the required details under basic tab
   * Create a new serve by entering a new server name, admin id and password
   * Select the pricing tier by clicking on Compute + Storage
   * Click on reviw + create, wait till validation is over and click on Create
* References:
   * https://docs.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?tabs=azure-portal

### Azure Data Factory
* Perform Copy Data from one Container to another using Data Factory
* Prerequisites
    * Azure Storage Account
    * An Application in Azure Active Directory to get the tenant id, client id and client key	
* Create a data factory:
    * From Azure Home Portal click on create a resource and search for Data Factory and click on create
    * File on the basic details in the basic tab
    * Click on review + create, wait until validation is over and click on create
* References:
    * https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-python
    * https://docs.microsoft.com/en-us/azure/data-factory/quickstart-create-data-factory-portal
