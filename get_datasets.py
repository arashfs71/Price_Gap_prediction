import wget, os, zipfile
import time
from datetime import datetime, timedelta
from calendar import monthrange
from dateutil.relativedelta import relativedelta

# Query format URL?queryname=<A>&startdatetime=<D>&enddatetime=<D>&market_run_id=<A>&version=<A>&varParameters

website = 'oasis.caiso.com'
api_name = 'oasisapi'
result_format = '6'  # For CSV response.
version = '1'
node = 'MURRAY_6_N015'  # Node closest to SDSU
query_name = 'PRC_LMP'
market_run_id = 'DAM'
path = 'caiso_downloads/'


def convert_to_datetime(start_year, start_month, start_day, duration):
    """
    Function to calculate end_date and to format dates.
    :return: A list of start_date(str) followed by an end_date(str)
    """
    dates = []
    # date_time_str = start_year+'-'+start_month+'-'+start_day+' '+'08:00:00'
    if len(start_day) != 2:
        start_day = start_day.zfill(2)
    if len(start_month) != 2:
        start_month = start_month.zfill(2)
    start_datetime = datetime(int(start_year), int(start_month), int(start_day))
    end_datetime = start_datetime + timedelta(days=int(duration))
    start_datetime_str = start_datetime.strftime('%Y%m%d')
    end_datetime_str = end_datetime.strftime('%Y%m%d')
    dates.append(start_datetime_str)
    dates.append(end_datetime_str)
    return dates


def construct_query(node, query_name,  start_year, start_month, start_day, duration, market_run_id):
    """
    Function to construct a query for a DAM market for CASIO OASIS API.
   :param node: (string)
   :param query_name: (string)
   :param start_year: (string)
   :param start_month: (string)
   :param start_day: (string)
   :param duration: (int) Number of days until the end date of the query
   :param market_run_id:
   :return: query(string)
   """
    url = f'http://{website}/{api_name}/SingleZip'

    dates = convert_to_datetime(start_year, start_month, start_day, duration)
    start_date = dates[0]
    end_date = dates[1]
    start_date = f'{start_date}T08:00-0000'
    end_date = f'{end_date}T08:00-0000'

    query = f'{url}?resultformat={result_format}&queryname={query_name}&version={version}&startdatetime={start_date}&enddatetime={end_date}&market_run_id={market_run_id}&node={node}'
    return query


def execute_query(node, query_name,  start_year, start_month, start_day, duration, market_run_id, path):
    """
    Executes a query to get a zip file containing a CSV file with information about the specified node.
    :param node: string
    :param query_name: (string)
    :param start_year: (string)
    :param start_month: (string)
    :param start_day: (string)
    :param duration: (int) Data can be requested for maximum period of 31 days, for a single request.
    :param market_run_id: (string) Specifies a market.
    :return: Saves a ZIP file in a 'path' location, which contains a CSV file.
    """
    url = construct_query(node, query_name, start_year, start_month, start_day, duration, market_run_id)
    wget.download(url, path)


def unzip_dir(download_dir, unzipped_target_dir):
    """
    Unzips all zip files in a directory.
    :param download_dir: (string) Relative path to a directory.
    :param unzipped_target_dir: (string)
    :return:
    """
    for item in os.listdir(download_dir):           # loop through items in dir
        if item.split('.')[-1] == 'zip':            # check for zip extension
            file_name = f'{download_dir}{item}'     # get relative path of files
            print(f'unzipping... {file_name}')
            zip_ref = zipfile.ZipFile(file_name)    # create zipfile object
            with zip_ref as target:
                target.extractall(unzipped_target_dir)
        else:
            continue

def get_data(years, download_dir, node, query_name, start_year, start_month, start_day, market_run_id):
    """
    Downloads years of data
    :param years:
    :return:
    """

    for i in range(12*years):
        start_datetime = datetime(int(start_year), int(start_month), int(start_day))
        date_after_month = start_datetime + relativedelta(months=1)
        duration = (date_after_month - start_datetime)
        duration = int(duration.days) - 1
        execute_query(node, query_name, start_year, start_month, start_day, duration, market_run_id, download_dir)
        time.sleep(10)
        if int(start_month) < 12:
            start_month = str(1 + int(start_month))
        else:
            start_year = str(1 + int(start_year))
            start_month = '01'
        print(start_year)
        print(start_month)
        print(duration)


# get_data(1, path, node, query_name, '2015', '01', '01', market_run_id)
start_year = '2017'
start_month = '01'
start_day = '01'

get_data(3, path, node, query_name, start_year, start_month, start_day, market_run_id)
