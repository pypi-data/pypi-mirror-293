#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import requests
import os
import json
import time
from io import BytesIO
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from datetime import datetime


# In[15]:


class energy_scraper():
    ''' suggested to run methods in this order:
    check_new, download, clean_data, integrity_check, save'''

    def __init__(self) -> None:
        self.url = 'https://www.gov.uk/government/statistics/oil-and-oil-products-section-3-energy-trends'
        self.fpath = ''
        self.df = pd.DataFrame()
        self.status_code = 0

    def check_new(self):
        #parse website HTML tags

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        dic = {}
        script_tags = (soup.find_all(name='script', attrs={'type':'application/ld+json'}))

        for elem in script_tags:
            script = elem.string
            json_script = json.loads(script)
            
            if json_script.get('@type') == 'Dataset':
                dic = json_script
                break
        

        for subdic in dic['distribution']:
            if 'Supply and use of crude oil, natural gas liquids and feedstocks' in subdic['name']:
                self.fpath = subdic['contentUrl']                

        # create a json to track date modified
        dtime = {'datetime':dic['dateModified']}
        json_fpath = 'datetime.json'
        if os.path.exists(json_fpath):

            with open(json_fpath, 'r') as file:
                cur_dtime = json.load(file)
            
            dt_field = cur_dtime.get('datetime')

            if dt_field:
                dt = pd.to_datetime(dt_field)

                num_days = (pd.to_datetime(dtime['datetime']) - pd.to_datetime(dt_field))

                #overwrite the json if file date is over 1 day old
                if num_days >= timedelta(days=1):
                    with open(json_fpath, 'w') as file:
                        json.dump(dtime, file)

        # create json if does not exist
        else:
            with open(json_fpath, 'w') as file:
                json.dump(dtime, file)
    
    def download(self):
        # use a get request to the url with the excel file
        
        max_retries = 5
        retry_delay = 5
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(self.fpath)
                # Check if the request was successful
                if response.status_code == 200:
                    self.status_code = response.status_code
                    xl = pd.ExcelFile(BytesIO(response.content))
                    self.df = pd.read_excel(xl, sheet_name="Quarter", skiprows=3, header=1)
                    print("Download successful")
                    break
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")
                    retries += 1
                    time.sleep(retry_delay)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                retries += 1
                time.sleep(retry_delay)
        else:
            print("Maximum retries reached. Failed to download the file.")

    
    def clean_data(self):
        df = self.df

        #helper method
        def convert_quarter_to_date(colname):
            try:
                parts = colname.split('\n')
                year = parts[0].strip()
                quarter = int(parts[1].strip()[0])
                
                month_mapping = {
                        1: '03',
                        2: '06',
                        3: '09',
                        4: '12'
                    }
                month = month_mapping.get(quarter)  # Default to January
                return f"{year}-{month}-01"
            except:
                return colname

        #convert column labels to datetime format
        df.columns = [convert_quarter_to_date(col) for col in df.columns]
        
        df = df.set_index("Column1")
        df.columns.name = None

        #reorient table format to time series format via transpose
        df = df.T
        df.index = pd.to_datetime(df.index)

        #add suffixes to duplicate column labels 
        cols = pd.Series(df.columns)
        duplicates = cols[cols.duplicated(keep=False)]
        duplicates_dict = {}

        for dup in duplicates.unique():
            indices = cols[cols == dup].index
            for i, idx in enumerate(indices):
                new_name = f"{dup}_{i+1}"
                df.columns.values[idx] = new_name
                duplicates_dict[new_name] = dup 
        
        self.df = df

    def integrity_check(self):
        # integrity checks: number of rows, num of missing values, key columns present
        df = self.df

        print(f"{df.shape[0]} time series data points present; earliest date is {df.index[0].year} Q{df.index[0].quarter}, latest date is {df.index[-1].year} Q{df.index[-1].quarter}.")

        missing = {}
        # num missing values, by field
        for col in df.columns:
            errors = df[col].isnull().sum()
            missing[col] = errors

        for k,v in missing.items():
            if v > 0:
                print(f"\n {k} has {v} missing values")
        
        # check for key columns
        key_cols = ["Indigenous production", "Imports", "Exports","Total supply","Total demand"]

        missing_cols = 0
        for col in key_cols:
            counter = 0
            
            while counter < len(df.columns):
                if col in df.columns[counter]:
                    break
                
                else:
                    counter += 1
                    if counter == len(df.columns)-1:
                        missing_cols += 1
        
        if missing_cols == 0:
            print("\nkey columns are all present")
        else:
            print(f"\n{missing_cols} key columns are missing")

    def save(self):
        self.df.to_csv("cleaned_energy_data.csv")
        print("CSV file saved")

