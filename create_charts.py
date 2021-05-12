'''
Copyright(c) 2021 Cisco and / or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

https: // developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

import pandas as pd
import matplotlib.pyplot as plt
import glob
import gzip
import datetime
from config import path, target_column, group_by_column, group_by_value, chart_type
from config import sorted_by_target_column, ascending

''' Time variable for logging & naming output files '''
now = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))


# Main script
def main():

    df = generateDFfromFiles()

    ''' Assign header columns to the logs, following Umbrella log's format '''
    # All the default columns
    df.columns = ['Timestamp', 'Policy Identity', 'Identities', 'InternalIp', 'ExternalIp', 'Action',
                  'QueryType', 'ResponseCode', 'Domain', 'Categories', 'Policy Identity Type', 'Identity Types', 'Blocked Categories']

    ''' To show the full column names in the console output '''
    pd.set_option("display.max.columns", None)

    ''' Print the whole dataframe '''
    print('-'*25 + ' Original dataframe: ' + '-'*25)
    print(df)

    ''' Copying Timestamp column to a new date-object column '''
    df['Date'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Date'].dt.date

    ''' Group by group_by_column, getting only group_by_value values(Example: 'Action':'Blocked') '''
    filtered_df = df.groupby([group_by_column]).get_group(group_by_value)
    print('-'*25 + ' Grouped by: ' + group_by_column +
          ': ' + group_by_value + ' ' + '-'*25)
    print(filtered_df)

    ''' Checking how many times a value was occurred on a certain target_column '''
    print('-'*25 + ' Data occurred, focused on: ' + target_column + ' ' + '-'*25)
    print(filtered_df[target_column].value_counts(
    ).sort_index(ascending=ascending))

    ''' Generating a chart of number of occurrences of a specific column in a DataFrame '''
    generatePlotbyOccurrences(filtered_df)


# Generating a pandas DataFrame object by reading data from csv.gz files
def generateDFfromFiles():
    ''' Getting csv data into a dataframe, using pandas '''

    ''' 
    Reading compressed(.gz) csv files from a folder, 
    header=None is needed as there is no header column for these files/logs,
    /**/ means all direct subfolders ..

    # You can make the import faster by getting only specific columns, add the argument:( , usecols=[0, 5, 8, 9, 12])
    # And make sure you match the header columns below (in main.py) to: df.columns = ['Timestamp', 'Action', 'Domain', 'Categories', 'Blocked Categories']
    '''
    all_files = glob.glob(path + '/**/*.csv.gz')
    list_df = []

    for filename in all_files:
        with gzip.open(filename) as f:
            print('Reading log file: ' + filename)
            data_frame = pd.read_csv(f, header=None)
            list_df.append(data_frame)

    df = pd.concat(list_df)
    return df


# Generating a plot chart of number of occurrences of a specific column in a DataFrame
def generatePlotbyOccurrences(df):
    ''' Creating axis by the number of occurrences ([:50] means getting only the top 50) '''
    ax = df[target_column].value_counts()[:50]

    if(sorted_by_target_column):
        ax = ax.sort_index(ascending=ascending)

    # Vertical bar
    if(chart_type == 'Vertical Bar'):
        ax = ax.plot(kind='bar', rot=10, fontsize=9, width=0.6)
        ax.set_xlabel(target_column)
        ax.set_ylabel('Number of occurrences')
        # Annotating each bar with its value
        for i in ax.patches:
            ax.text(i.get_x()+0.15, i.get_height()+0.3, str(i.get_height()))

    # Horizontal bar
    elif(chart_type == 'Horizontal Bar'):
        ax = ax.plot(kind='barh')
        ax.set_ylabel(target_column)
        ax.set_xlabel('Number of occurrences')
        # Annotating each bar with its value
        for i in ax.patches:
            ax.text(i.get_width()+.15, i.get_y()+.3, str(i.get_width()))

    # Pie chart
    elif(chart_type == 'Pie'):
        ax = ax.plot.pie(autopct='%1.1f%%')
        ax.set_xlabel(target_column)
        ax.set_ylabel('')

    ''' Setting up chart title '''
    ax.set_title('Umbrella dnslogs Summary\nGrouped by: ' + target_column +
                 ', filtered: ' + group_by_column + ' = ' + group_by_value)

    ''' Show the plot '''
    plt.show()

    # Save the generated graphs as local files
    generateChartAsFiles(ax)


# Save the generated graphs as local files
def generateChartAsFiles(ax):
    ''' Save the graph as a PDF file'''
    pdf_filename = 'output/' + target_column + ', ' + group_by_column + '_' + group_by_value + ' - ' + now + '.pdf'
    ax.get_figure().savefig(pdf_filename)
    print('PDF file has been generated: ' + pdf_filename)

    ''' Save the graph as a PNG file'''
    pdf_filename = 'output/' + target_column + ', ' + group_by_column + '_' + group_by_value + ' - ' + now + '.png'
    ax.get_figure().savefig(pdf_filename)
    print('PNG file has been generated: ' + pdf_filename)


main()
