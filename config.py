''' 
Update the path having Cisco Umbrella's generated dnslogs folder,
or keep it as is if you're running the script in the same directory having the dnslogs folder
'''
path = 'dnslogs'

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

''' 
Select the type of chart: 
    'Vertical Bar', 'Horizontal Bar', or 'Pie'
'''
chart_type = 'Vertical Bar'

''' 
Choose to sort the results by value of occurrences: True (for example: Sorting by time, when target_column: Date), 
or leave it be default order: False (for example: When wanting to see top domains, when target_column: Domain)
'''
sorted_by_target_column = True
ascending = True
