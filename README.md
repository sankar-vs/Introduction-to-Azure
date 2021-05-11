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

