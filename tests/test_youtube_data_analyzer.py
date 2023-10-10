#!/usr/bin/env python

import unittest
from data_analyzer.youtube_data_analyzer import YouTubeDataAnalyzer


class TestYouTubeDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.data_analyzer = YouTubeDataAnalyzer()

    def test_get_most_viewed_videos(self):
        most_viewed = self.data_analyzer.get_most_viewed_videos(10)
        self.assertEqual(len(most_viewed), 10)

    def test_get_most_disliked_videos(self):
        most_disliked = self.data_analyzer.get_most_disliked_videos(10)
        self.assertEqual(len(most_disliked), 10)

    def test_get_top_viewed_categories(self):
        top_categories = self.data_analyzer.get_top_viewed_categories(5)
        self.assertEqual(len(top_categories), 5)


if __name__ == '__main__':
    unittest.main()
