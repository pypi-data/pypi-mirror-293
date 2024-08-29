import numpy as np
import pandas as pd
import csv
import recommender_ibmws.recommender_functions as rf
import sys as sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity


class Recommender():
    '''
    This Recommender uses hybrid approach ofContent-Based Filtering and Collaborative Filtering to 
    make recommendations.  
    The content base recommendation system developed relies on a user profile, text vectorization, 
    similarity calculation, ranking and recommendation, as well as handling of new users. 
    '''

    def __init__(self):
        
        self.interactions = None
        self.content = None
        
    def load_data(self,inter_path, content_path):
        """
        Loads interaction and content data from CSV files, maps email addresses to unique user IDs, 
        and returns the processed interaction and content dataframes.

        Parameters:
            inter_path (str): The filepath to the interactions CSV file.
            content_path (str): The filepath to the content CSV file.

        Returns:
            tuple: A tuple containing the processed interaction and content dataframes.
        """
        
        self.interactions, self.content = rf.load_data(inter_path, content_path)
        return self.interactions, self.content

    def make_content_recs(self, user_id, m=10):
        """
        Makes content-based recommendations for a given user.

        Parameters:
            user_id (int): The ID of the user for whom to make recommendations.
            m (int): The number of recommendations to make.

        Returns:
            tuple: A tuple containing the hybrid recommendations and their names.
            This function stores the following as attributes:
            n_users - the number of users (int)
            n_articles - the number of articles (int)
            num_interactions - the number of interactions (int)
            user_item - the user-item matrix (pandas dataframe)
            user_id - the user ID (int)
            m - the number of recommendations (int)
            user_profile - the user profile (str)
            interactions - the interaction dataframe (pandas dataframe)
            content - the content dataframe (pandas dataframe)
            hybrid_recs - the recommendations (list)
            hybrid_rec_names - the recommended article names (list)
        """
        # Create user-item matrix
        self.user_item = rf.create_user_item_matrix(self.interactions)
        
        # Store more inputs
        self.user_id = user_id
        self.m = m
        
        # Set up useful values to be used through the rest of the function
        self.n_users = self.user_item.shape[0]
        self.n_articles = self.user_item.shape[1]
        self.num_interactions = np.count_nonzero(~np.isnan(self.user_item))
        
        # Create user-item matrix only once
        user_item = rf.create_user_item_matrix(self.interactions)
        # Group articles by interaction count
        article_interactions = self.interactions.groupby('article_id').count()['user_id']

        # Check if user has any interactions
        if user_id in user_item.index:
            user_articles = rf.get_user_articles(user_id, self.interactions)[0]
            
            if user_articles:
                # Build user profile based on the content of articles the user has interacted with
                user_profile = ' '.join(self.content[self.content['article_id'].isin(user_articles)]['doc_full_name'])
                
                tfidf = TfidfVectorizer(stop_words='english')
                tfidf_matrix = tfidf.fit_transform(self.content['doc_full_name'])
                user_profile_vector = tfidf.transform([user_profile])
                
                # Calculate content-based recommendations
                cosine_sim_content = cosine_similarity(user_profile_vector, tfidf_matrix)
                content_based_rec_indices = cosine_sim_content.argsort()[0][::-1]
                
                # Filter out articles the user has already interacted with
                content_based_recs = [self.content.iloc[i]['article_id'] for i in content_based_rec_indices 
                                    if self.content.iloc[i]['article_id'] not in user_articles][:m]
            else:
                content_based_recs = rf.get_top_article_ids(m, self.interactions)
        else:
            content_based_recs = rf.get_top_article_ids(m, self.interactions)

        # Collaborative Filtering
        if user_id in user_item.index:
            user_interactions = user_item.loc[user_id]
            similar_users = user_item.drop(user_id).apply(
                lambda row: cosine_similarity([user_interactions], [row])[0][0], axis=1)
            similar_users = similar_users.sort_values(ascending=False)
            
            collaborative_recs = []
            for sim_user in similar_users.index:
                new_recs = np.setdiff1d(rf.get_user_articles(sim_user, self.interactions)[0], 
                                        rf.get_user_articles(user_id, self.interactions)[0], 
                                        assume_unique=True)
                
                # Sort recommendations based on article popularity/interaction count
                recs_to_add = article_interactions.loc[new_recs].sort_values(ascending=False)
                collaborative_recs.extend(recs_to_add.index)
                if len(collaborative_recs) >= m:
                    break
            collaborative_recs = collaborative_recs[:m]
        else:
            collaborative_recs = rf.get_top_article_ids(m, self.interactions)

        # Hybrid Recommendations
        hybrid_recs = list(set(content_based_recs) | set(collaborative_recs))[:m]
        hybrid_recs = article_interactions.loc[hybrid_recs].sort_values(ascending=False).index.tolist()[:m]
        hybrid_rec_names = rf.get_article_names(hybrid_recs, self.interactions)
        
        return hybrid_recs, hybrid_rec_names

if __name__ == '__main__':
    import recommender as r

    #instantiate recommender
    rec = r.Recommender()
    
    # load data
    rec.load_data(inter_path='data/user-item-interactions.csv', content_path= 'data/articles_community.csv')

    # make recommendations
    rec.make_recommendations(8, m=10) # user in the dataset
    rec.make_recommendations(5150, m=10)# user not in dataset
    rec.n_users
    rec.n_articles