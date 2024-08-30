import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import regex as re
from io import BytesIO
from datetime import datetime
import csv
import json
import logging

def energycsv_parser(folder_name='Downloads', last_modified_date_folder_name='Downloads'):
    class DataValidationError(Exception):
        pass

    def validate_input(df, expected_min_column_count=102, expected_row_count=19, max_missing_percentage=50.0):
        """
        Performs basic checks to validate the data input for the expected number of columns and rows.
        expected_min_column_count: The expected minimum number of columns, with a default threshold based on previous datasets.
        expected_row_count: The expected number of rows, with a default threshold based on previous datasets.
        """
        actual_column_count = df.shape[1]
        actual_row_count = df.shape[0]

        if actual_column_count < expected_min_column_count:
            error_msg = f"Error: Column count {actual_column_count} is less than the expected minimum of {expected_min_column_count}."
            logging.error(error_msg)
            raise DataValidationError(error_msg)

        if actual_row_count < expected_row_count:
            error_msg = f"Error: Row count {actual_row_count} is less than the expected {expected_row_count}."
            logging.error(error_msg)
            raise DataValidationError(error_msg)

        logging.info("Input validation passed successfully.")

        # Calculate the percentage of missing values per column
        missing_percentage_per_column = df.isna().mean() * 100

        # check against threshold
        columns_exceeding_threshold = missing_percentage_per_column[
            missing_percentage_per_column > max_missing_percentage]

        if not columns_exceeding_threshold.empty:
            error_msg = (
                f"Error: The following columns exceed the missing data threshold of {max_missing_percentage}%:\n"
                f"{columns_exceeding_threshold.to_dict()}"
            )
            logging.error(error_msg)
            raise DataValidationError(error_msg)

        logging.info("Missing values validation passed successfully.")

    # Get Request
    response = requests.get('https://www.gov.uk/government/statistics/oil-and-oil-products-section-3-energy-trends')
    soup = BeautifulSoup(response.text, 'html.parser')

    target_html = soup.find('a',
                            string=re.compile(r".*Supply and use of crude oil, natural gas liquids and feedstocks.*"))
    target_link = target_html['href']

    # Last Modfied Date
    date_modified = json.loads(soup.find('script', type='application/ld+json').string)
    date_modified = date_modified.get('dateModified')
    date_modified = datetime.fromisoformat(date_modified).replace(tzinfo=None)

    # Check if this is latest file
    downloads_path = os.path.join(os.path.expanduser('~'), last_modified_date_folder_name, 'lastmodifieddate.csv')

    # Checking if CSV Exists if not create CSV with default date.
    if not os.path.exists(downloads_path):
        default_date = datetime(1900, 1, 1, 0, 0, 0)
        # Create the CSV file with a header
        with open(downloads_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["last_download_date"])
            writer.writerow([default_date.isoformat()])

    with open(downloads_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    most_recent_date_str = rows[1][0]
    most_recent_date = datetime.fromisoformat(most_recent_date_str)

    if date_modified <= most_recent_date:
        print("Latest Data Already Published.")
    else:
        with open(downloads_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["last_download_date"])
            writer.writerow([date_modified.isoformat()])

    # Extract the file name from the URL
    original_file_name = target_link.split('/')[-1]

    # Send a GET request to download the file
    file_response = requests.get(target_link)
    file_content = BytesIO(file_response.content)

    excel_data = pd.ExcelFile(file_content)

    # Extract the 'Quarter' sheet
    quarter_data = excel_data.parse('Quarter', header=None)
    df = quarter_data
    date_pattern = r'\d{4}\s+\d+(st|nd|rd|th)\s+quarter'
    header_row = df.apply(lambda row: row.astype(str).str.match(date_pattern).any(), axis=1).idxmax()
    df.columns = df.iloc[header_row]
    df = df.iloc[header_row + 1:]

    # Unit Testing Raw Data
    try:
        validate_input(df)
    except DataValidationError as e:
        print(f"Validation failed: {e}")
    else:
        print("Validation passed.")

        # Restructuring Table
        strings_to_remove = ['Indigenous production [note 2]', 'Imports [note 4]',
                             'Exports [note 4]', 'Total supply', 'Statistical difference [note 7]',
                             'Total demand', 'Transformation', 'Energy industry use']
        SubCategory = ['Indigenous production [note 2]', 'Indigenous production [note 2]',
                       'Indigenous production [note 2]', 'Imports [note 4]', 'Imports [note 4]',
                       'Exports [note 4]', 'Exports [note 4]', 'Stock change [note 5]',
                       'Transfers [note 6]', 'Transformation', 'Energy industry use']
        Category = ['Total Supply', 'Total Supply', 'Total Supply',
                    'Total Supply', 'Total Supply', 'Total Supply',
                    'Total Supply', 'Total Supply', 'Total Supply',
                    'Total Demand', 'Total Demand']

        df = df[df.Column1.apply(lambda txt: not any(string in txt for string in strings_to_remove))]

        # Insert New Column
        df.insert(0, "EnergySubCategory", SubCategory)
        df.insert(0, "SupplyDemandCategory", Category)
        df = df.rename(columns={'Column1': 'EnergyResource'})
        df['OriginalFileName'] = original_file_name
        current_datetime = datetime.now()
        df['DataProcessedDate'] = current_datetime.date()
        df['DataProcessedTime'] = current_datetime.strftime('%H:%M:%S')

        # Unpivot the date columns
        df = df.melt(
            id_vars=['SupplyDemandCategory', 'EnergySubCategory', 'EnergyResource', 'OriginalFileName',
                     'DataProcessedDate',
                     'DataProcessedTime'],
            var_name='Quarter', value_name='Value')

        # Function to convert quarter format to yyyy-MM-dd
        def quarter_to_date(quarter_str):
            year, qtr = quarter_str.split(maxsplit=1)
            if "1" in qtr:
                return f"{year}-03-01"
            elif "2" in qtr:
                return f"{year}-06-01"
            elif "3" in qtr:
                return f"{year}-09-01"
            elif "4" in qtr:
                return f"{year}-12-01"

        df['Quarter'] = df['Quarter'].apply(quarter_to_date)

        df['EnergySubCategory: Note'] = df['EnergySubCategory'].str.extract(r'\[note (\d+)\]')
        df['EnergySubCategory'] = df['EnergySubCategory'].str.replace(r'\[note \d+\]', '', regex=True).str.strip()

        df['EnergyResource: Note'] = df['EnergyResource'].str.extract(r'\[note (\d+)\]')
        df['EnergyResource'] = df['EnergyResource'].str.replace(r'\[note \d+\]', '', regex=True).str.strip()

        df.loc[df['EnergySubCategory'] == 'Exports', 'Value'] *= -1


        downloads_path = os.path.join(os.path.expanduser('~'), folder_name, 'EnergyReport.csv')

        # Saving the DataFrame to the CSV file
        csv_file = df.to_csv(downloads_path, index=False)

    return csv_file

energycsv_parser()