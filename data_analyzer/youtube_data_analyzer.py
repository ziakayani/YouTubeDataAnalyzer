#!/usr/bin/env python

""" This module read the videos data from s3
    Creates three files for Most Viewed, Most Disliked and Top Viewed Categories
"""

# Author information and metadata
__author__ = "Zia Kiyani"
__version__ = "1.0"
__email__ = "zia_kayani@hotmail.com"

# Import required libraries
import io
import sys
import json
import boto3
import logging
import argparse
import pandas as pd
from constants import *

# Setting basic format of logger
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    stream=sys.stdout, level=logging.INFO)


# Create a class for YouTubeDataAnalyzer
class YouTubeDataAnalyzer:
    """
    Initialize the YouTubeDataAnalyzer instance.
    Load all the required data from s3 or local.
    """
    def __init__(self):
        # self.categories, self.data = self.read_from_local()
        self.categories, self.data = self.read_from_s3()

    def read_from_local(self):
        """
        Read categories and video data from Local Directory.

        Returns:
        tuple: A tuple containing a dictionary of categories and a pandas DataFrame of video data.
        """
        try:
            logging.info("Starting reading data")
            # Open and read categories JSON file
            file_categories = open(CATEGORIES_PATH, "r")
            json_categories = json.load(file_categories)
            # Create a dictionary of category IDs and titles
            categories = {int(item['id']): item['snippet']['title'] for item in json_categories['items']}
            # Read CSV data into a pandas DataFrame
            data = pd.read_csv(DATA_PATH)
            # Map category IDs to category titles
            data.insert(loc=5, column="category", value=data["category_id"].map(categories))
            file_categories.close()
            logging.info("Data read successfully")
            return categories, data
        except Exception as e:
            logging.error("An error occurred while reading from local:" + str(e))
            return None, None

    def read_from_s3(self):
        """
        Read categories and video data from AWS S3.

        Returns:
        tuple: A tuple containing a dictionary of categories and a pandas DataFrame of video data.
        """
        try:
            logging.info("Starting reading data")
            # Initialize S3 client
            s3 = boto3.client(CLIENT)
            # Get categories JSON object from S3
            obj_categories = s3.get_object(Bucket=BUCKET, Key=CATEGORIES_PATH)
            json_categories = json.loads(obj_categories[BODY].read().decode(ENCODING))
            # Create a dictionary of category IDs and titles
            categories = {int(item['id']): item['snippet']['title'] for item in json_categories['items']}
            obj_data = s3.get_object(Bucket=BUCKET, Key=DATA_PATH)
            # Read CSV data into a pandas DataFrame
            data = pd.read_csv(io.BytesIO(obj_data[BODY].read()))
            # Map category IDs to category titles
            data.insert(loc=5, column="category", value=data["category_id"].map(categories))
            logging.info("Data read successfully")
            return categories, data
        except Exception as e:
            logging.error("An error occurred while reading data from S3:" + str(e))
            return None, None

    def get_most_viewed_videos(self, n=DEFAULT_MOST_VIEWED_COUNT):
        """
        Get the most viewed videos.

        Parameters:
        n (int): Number of most viewed videos to retrieve (default is Declared in Constants).

        Returns:
        pandas.DataFrame: DataFrame containing the most viewed videos.
        """
        logging.info("Calculating {0} Most Viewed Videos".format(n))
        # Get and Return the top N most viewed videos
        return self.data.nlargest(n, 'views')

    def get_most_disliked_videos(self, n=DEFAULT_MOST_DISLIKED_COUNT):
        """
        Get the most disliked videos.

        Parameters:
        n (int): Number of most disliked videos to retrieve (default is Declared in Constants).

        Returns:
        pandas.DataFrame: DataFrame containing the most disliked videos.
        """
        logging.info("Calculating {0} Most Disliked Videos".format(n))
        # Get and Return the top N most disliked videos
        return self.data.nlargest(n, 'dislikes')

    def get_top_viewed_categories(self, n=DEFAULT_TOP_VIEWED_CATEGORIES_COUNT):
        """
        Get the top viewed categories.

        Parameters:
        n (int): Number of top viewed categories to retrieve (default is Declared in Constants).

        Returns:
        pandas.DataFrame: DataFrame containing the top viewed categories.
        """
        logging.info("Calculating Top {0} Viewed Videos Categories".format(n))
        # Group video data by category and sum up views for each category
        categories = self.data.groupby(['category_id', 'category']).sum()[ATTRIBUTES_IN_TOP_VIEWED]
        # Get the top N viewed categories
        return categories.nlargest(n, 'views')

    def save_to_s3(self, data_frame, path, index):
        """
        Save a pandas DataFrame to AWS S3.

        Parameters:
        data_frame (pandas.DataFrame): The DataFrame to be saved.
        key (str): The S3 key to use for the object.

        Returns:
        bool: True if successful, False otherwise.
        """
        try:
            logging.info("Starting writing {0}".format(path))
            csv_buffer = io.StringIO()
            data_frame.to_csv(csv_buffer, index=index)
            s3 = boto3.client(CLIENT)
            response = s3.put_object(Bucket=BUCKET, Key=path, Body=csv_buffer.getvalue())
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except Exception as e:
            logging.error("An error occurred while saving to S3:" + str(e))
            return False

    def save_to_local(self, data_frame, path, index):
        """
        Save a pandas DataFrame to Local Directory.

        Parameters:
        data_frame (pandas.DataFrame): The DataFrame to be saved.
        path (str): The path to use for the dataframe.

        Returns:
        bool: True if successful, False otherwise.
        """
        try:
            logging.info("Starting writing {0}".format(path))
            data_frame.to_csv(path, index=index)
            return True
        except Exception as e:
            logging.error("An error occurred while saving to S3:" + str(e))
            return False


# MAIN Function
def main():
    try:
        # initialize variables
        # Use argparse to handle command-line arguments
        logging.info("Parsing arguments")
        parser = argparse.ArgumentParser()
        parser.add_argument("-mv", "--most_viewed",
                            help="Number of Most Viewed Videos Required",
                            type=int, required=False, default=DEFAULT_MOST_VIEWED_COUNT)
        parser.add_argument("-md", "--most_disliked",
                            help="Number of Most disliked Videos Required",
                            type=int, required=False, default=DEFAULT_MOST_DISLIKED_COUNT)
        parser.add_argument("-mvc", "--top_viewed_categories",
                            help="Top Viewed Videos Categories Required",
                            type=int, required=False, default=DEFAULT_TOP_VIEWED_CATEGORIES_COUNT)

        args = parser.parse_args()
        # Get command-line arguments
        most_viewed_count = args.most_viewed
        most_disliked_count = args.most_disliked
        top_viewed_categories_count = args.top_viewed_categories
        logging.info("Arguments successfully parsed")
    except Exception as e:
        logging.error("An error occurred while parsing the arguments: " + str(e))

    # Create an instance of YouTubeDataAnalyzer
    data_analyzer = YouTubeDataAnalyzer()
    try:
        # Get and save most viewed videos
        most_viewed_videos = data_analyzer.get_most_viewed_videos(most_viewed_count)
        # data_analyzer.save_to_local(most_viewed_videos, MOST_VIEWED_FILE_NAME, index=False)
        data_analyzer.save_to_s3(most_viewed_videos, OUTPUT_PATH + MOST_VIEWED_FILE_NAME, index=False)
    except Exception as e:
        logging.error("An error occurred while getting and saving most viewed videos:" + str(e))

    try:
        # Get and save most disliked videos
        most_disliked_videos = data_analyzer.get_most_disliked_videos(most_disliked_count)
        # data_analyzer.save_to_local(most_disliked_videos, MOST_DISLIKED_FILE_NAME, index=False)
        data_analyzer.save_to_s3(most_disliked_videos, OUTPUT_PATH + MOST_DISLIKED_FILE_NAME, index=False)
    except Exception as e:
        logging.error("An error occurred while getting and saving most disliked videos:" + str(e))

    try:
        # Get and save top viewed categories
        top_viewed_categories = data_analyzer.get_top_viewed_categories(top_viewed_categories_count)
        # data_analyzer.save_to_local(top_viewed_categories, TOP_VIEWED_CATEGORIES_FILE_NAME, index=True)
        data_analyzer.save_to_s3(top_viewed_categories, OUTPUT_PATH + TOP_VIEWED_CATEGORIES_FILE_NAME, index=True)
    except Exception as e:
        logging.error("An error occurred while getting and saving top viewed categories:" + str(e))

    logging.info("Successfully completed")


# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()

