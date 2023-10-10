#!/usr/bin/env python

"""This module defines all the project-level constants."""

CLIENT = "s3"
BUCKET = "ispot-interview-zk"
DATA_PATH = "USvideos.csv"
CATEGORIES_PATH = "US_category_id.json"
ENCODING = 'utf-8'
BODY = 'Body'

OUTPUT_PATH = "output/"
MOST_VIEWED_FILE_NAME = "most_viewed_videos.csv"
MOST_DISLIKED_FILE_NAME = "most_disliked_videos.csv"
TOP_VIEWED_CATEGORIES_FILE_NAME = "top_viewed_categories.csv"

DEFAULT_MOST_VIEWED_COUNT = 1000
DEFAULT_MOST_DISLIKED_COUNT = 1000
DEFAULT_TOP_VIEWED_CATEGORIES_COUNT = 10

ATTRIBUTES_IN_TOP_VIEWED = ["views", "likes", "dislikes", "comment_count", "comments_disabled", "ratings_disabled", "video_error_or_removed"]