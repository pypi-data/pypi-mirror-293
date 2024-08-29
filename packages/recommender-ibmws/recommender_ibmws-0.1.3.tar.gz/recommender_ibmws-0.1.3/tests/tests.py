import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from recommender_ibmws.recommender import Recommender  # Adjusted import for the Recommender class

class TestRecommender(unittest.TestCase):

    def setUp(self):
        # This method will run before each test. It's useful for setting up any shared state.
        self.recommender = Recommender()
        self.interactions_mock = pd.DataFrame({
            'user_id': [1, 2, 3, 4],
            'article_id': [101, 102, 103, 104],
            'interaction': [1, 1, 1, 1]
        })
        self.content_mock = pd.DataFrame({
            'article_id': [101, 102, 103, 104, 105],
            'doc_full_name': ['Article A', 'Article B', 'Article C', 'Article D', 'Article E']
        })

    @patch('recommender_ibmws.recommender.rf.load_data')
    def test_load_data(self, mock_load_data):
        # Mock the rf.load_data function
        mock_load_data.return_value = (self.interactions_mock, self.content_mock)
        
        interactions, content = self.recommender.load_data('interactions.csv', 'content.csv')
        
        mock_load_data.assert_called_once_with('interactions.csv', 'content.csv')
        pd.testing.assert_frame_equal(interactions, self.interactions_mock)
        pd.testing.assert_frame_equal(content, self.content_mock)

    @patch('recommender_ibmws.recommender.rf.create_user_item_matrix')
    @patch('recommender_ibmws.recommender.rf.get_user_articles')
    @patch('recommender_ibmws.recommender.rf.get_top_article_ids')
    @patch('recommender_ibmws.recommender.rf.get_article_names')
    def test_make_content_recs(self, mock_get_article_names, mock_get_top_article_ids, mock_get_user_articles, mock_create_user_item_matrix):
        # Mock functions
        mock_create_user_item_matrix.return_value = pd.DataFrame({
            101: [1, 0, 0, 0],
            102: [0, 1, 0, 0],
            103: [0, 0, 1, 0],
            104: [0, 0, 0, 1],
        }, index=[1, 2, 3, 4])
        
        mock_get_user_articles.return_value = ([101], ['Article A'])
        mock_get_top_article_ids.return_value = [105, 103, 104]
        mock_get_article_names.return_value = ['Article E', 'Article C', 'Article D']
        
        self.recommender.interactions = self.interactions_mock
        self.recommender.content = self.content_mock
        
        hybrid_recs, hybrid_rec_names = self.recommender.make_content_recs(1, m=3)
        
        # Test that the correct methods were called
        mock_create_user_item_matrix.assert_called_once()
        mock_get_user_articles.assert_called_once_with(1, self.interactions_mock)
        mock_get_article_names.assert_called_once()
        
        # Verify the recommendations
        self.assertEqual(hybrid_recs, [105, 103, 104])
        self.assertEqual(hybrid_rec_names, ['Article E', 'Article C', 'Article D'])

    @patch('recommender_ibmws.recommender.rf.get_top_article_ids')
    def test_cold_start_user(self, mock_get_top_article_ids):
        # Simulate cold start by testing with a new user ID (not in interactions)
        mock_get_top_article_ids.return_value = [105, 103, 104]
        
        self.recommender.interactions = self.interactions_mock
        self.recommender.content = self.content_mock
        
        hybrid_recs, hybrid_rec_names = self.recommender.make_content_recs(999, m=3)
        
        # Verify that the fallback method was used
        mock_get_top_article_ids.assert_called_once_with(3, self.interactions_mock)
        self.assertEqual(hybrid_recs, [105, 103, 104])

    @patch('recommender_ibmws.recommender.rf.create_user_item_matrix')
    def test_no_user_interactions(self, mock_create_user_item_matrix):
        # Test behavior when user has no interactions
        mock_create_user_item_matrix.return_value = pd.DataFrame({
            101: [0, 0, 0, 0],
            102: [0, 0, 0, 0],
            103: [0, 0, 0, 0],
            104: [0, 0, 0, 0],
        }, index=[1, 2, 3, 4])
        
        self.recommender.interactions = self.interactions_mock
        self.recommender.content = self.content_mock
        
        hybrid_recs, hybrid_rec_names = self.recommender.make_content_recs(1, m=3)
        
        # Since no interactions, it should fallback to top article recommendations
        self.assertEqual(len(hybrid_recs), 3)

if __name__ == '__main__':
    unittest.main()