# GVE DevNet Umbrella logs to charts
This prototype is showing how to generate sample charts summarizing the events that are generated in Umbrella dnslogs. Whether they are stored locally, or in a Cisco-managed S3 Bucket.


## Contacts
* Rami Alfadel (ralfadel@cisco.com)

## Solution Components

* Cisco Umbrella
* AWS S3 Bucket
* Python 
    * Library for data analysis: [Pandas](https://pandas.pydata.org/)
    * Library for creating static, animated, and interactive visualizations: [Matplotlib](https://matplotlib.org/)

## Installation/Configuration

 - Make sure you have [Python](https://www.python.org/downloads/) installed
 - Clone this Github repository into the virtual environment folder:  
   ```git clone [add github link here]```
   - For Github link: 
        In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
        ![/IMAGES/giturl.png](/IMAGES/giturl.png)

 - Access the folder **GVE_DevNet_Umbrella_logs_to_charts**:  
   ```cd GVE_DevNet_Umbrella_logs_to_charts```

 6. Install the solution requirments:  
   ```pip install -r requirments.txt```


## Usage

1. Make sure you have the **dnslogs** folder in the same device you're running the script from.
- (Optional) If the **dnslogs** folder is not in the same device, but in [Cisco-managed S3 Bucket](https://docs.umbrella.com/deployment-umbrella/docs/cisco-managed-s3-bucket): 
  - Edit the bash script to have the right AWS S3 credentials to download the log files locally:
  ```bash
    AWS_ACCESS_KEY_ID=<aws_access_key> 
    AWS_SECRET_ACCESS_KEY=<aws_secret_access_key> 
    aws s3 sync s3://<data_path> .
  ```
  - Run the bash script to sync the folder from AWS S3 Bucket to the local folder:  
  ```./pull-umbrella-logs.sh```
2. Configure the configuration variables in ```config.py``` file:     
    1. Start with setting up the path to the *dnslogs* folder:
        
        ```python
        ''' 
        Update the path having Cisco Umbrella's generated dnslogs folder,
        or keep it as is if you're running the script in the same directory having the dnslogs folder
        '''
        path = 'dnslogs'
        ```
    2. The logs are following the format of [Cisco Umbrella DNS logs](https://docs.umbrella.com/deployment-umbrella/docs/log-formats-and-versioning#section-dns-logs).  
    Select the main column to identify the results with, and the column to group the results by, in the following variables:

        ```python
        ''' 
        Select the target column to identify the results with, and the column to group the results by.
        Can be any of the following:
            'Timestamp', 'Policy Identity', 'Identities', 'InternalIp', 'ExternalIp',
            'Action', 'QueryType', 'ResponseCode', 'Domain', 'Categories', 
            'Policy Identity Type', 'Identity Types', 'Blocked Categories'
        '''
        target_column = 'Date'
        group_by_column = 'Action'
        group_by_value = 'Blocked'
        ```
    3. Select the type of chart to show the results in: 
        
        ```python
        '''
        'Vertical Bar', 'Horizontal Bar', or 'Pie'
        '''
        chart_type = 'Vertical Bar'
        ```
    4. Choose to how to sort the results, if needed:

        ```python
        ''' 
        Choose to sort the results by value of occurrences: True (for example: Sorting by time, when target_column: Date), 
        or leave it be default order: False (for example: When wanting to see top domains, when target_column: Domain)
        '''
        sorted_by_target_column = True
        ascending = True
        ```
 3. Run the script to read the data and generate the charts:  
      ```python create_charts.py```
 
 4. You will also see the chart being generated to *output* folder, as PDF and PNG files. 
   - You can customize the naming of the generated files inside the function:
       - *create_charts.py*: ```def generateChartAsFiles(ax)```


# Screenshots

- Sample Vertical Bar chart:
  - (target_column: Date, group_by_column: 'Action', group_by_value = 'Blocked')
    ![/IMAGES/Sample_hBar_Domain.png](/IMAGES/Sample_vBar_Date.png)

- Sample Horizontal Bar chart:
  - (target_column: Categories, group_by_column: 'Action', group_by_value = 'Allowed')
    ![/IMAGES/Sample_hBar_Category.png](/IMAGES/Sample_hBar_Category.png)

- Sample Pie chart:
  - (target_column: Blocked Categories, group_by_column: 'Action', group_by_value = 'Blocked')
    ![/IMAGES/Sample_Pie_Blocked_Categories.png](/IMAGES/Sample_Pie_Blocked_Categories.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
