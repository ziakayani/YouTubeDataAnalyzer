# YouTube Data Analyzer

This Python module reads videos data from AWS S3, processes it, and creates three output files for Most Viewed Videos, Most Disliked Videos, and Top Viewed Categories.

### Author Information and Metadata
- Author: Zia Kiyani
- Version: 1.0
- Email: zia_kayani@hotmail.com

## Description
The module contains a class called `YouTubeDataAnalyzer` which initializes by reading data from S3. It also provides methods to retrieve and analyze data to generate desired insights.


## Scripts
- Main script: ```data_analyzer/youtube_data_analyzer.py``` Contains the actual implementation.
- Constants: ```data_analyzer/constants.py``` Contains all the constants used.
- Test script: ```test/test_youtube_data_analyzer.py``` Contains the test scenarios.

## Parameters
It takes 3 parameters

| Parameter| Default Value |
| -------- | ------------- |
| -mv, --most_viewed | 1000 |
| -md, --most_disliked | 1000 |
| -mvc, --top_viewed_categories | 10 |

## How to run
```sh
$ python data_analyzer/youtube_data_analyzer.py
# Can also b run with parameters
$ python data_analyzer/youtube_data_analyzer.py --most_viewed 10 --most_disliked 10 -top_viewed_categories 5
```

### Output
It creates three files on s3 `s3://ispot-interview-zk/output/`
- most_viewed_videos.csv
- most_disliked_videos.csv
- top_viewed_categories.csv

## How to run test cases
```sh
$ python -m unittest tests/test_youtube_data_analyzer.py
```

## Required Libraries
`boto3`
> requirements.txt is also added. 

### Additional implementation
Also contains reading/writing from local mahcine as well.
