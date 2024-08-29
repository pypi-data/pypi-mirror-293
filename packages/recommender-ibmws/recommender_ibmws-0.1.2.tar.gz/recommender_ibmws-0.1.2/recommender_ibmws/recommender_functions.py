import numpy as np
import pandas as pd
import importlib.resources as pkg_resources
from recommender_ibmws import data

def load_data(inter_path, content_path):
    """
	Loads interaction and content data from CSV files, maps email addresses to unique user IDs, 
	and returns the processed interaction and content dataframes.

	Parameters:
		inter_path (str): The filepath to the interactions CSV file.
		content_path (str): The filepath to the content CSV file.

	Returns:
		tuple: A tuple containing the processed interaction and content dataframes.
	"""
    #interactions = pd.read_csv(inter_path)
    #content = pd.read_csv(content_path)
    with pkg_resources.open_text(data, inter_path) as inter_file:
        interactions = pd.read_csv(inter_file)

    with pkg_resources.open_text(data, content_path) as content_file:
        content = pd.read_csv(content_file)
    
    del interactions['Unnamed: 0']
    del content['Unnamed: 0']
    
    email_encoded = email_mapper(interactions)
    del interactions['email']
    interactions['user_id'] = email_encoded
    
    print(interactions.head())
    print(content.head())
    
    return interactions, content

def email_mapper(interactions):
    """
    Maps email addresses to unique user IDs.

    Parameters:
        interactions (pandas DataFrame): Interaction data.

    Returns:
        list: A list of user IDs corresponding to the input email addresses.
    """
    
    coded_dict = dict()
    cter = 1
    email_encoded = []
    
    for val in interactions['email']:
        if val not in coded_dict:
            coded_dict[val] = cter
            cter+=1
        
        email_encoded.append(coded_dict[val])
    return email_encoded

def get_top_articles(n, interactions):
    """
    Returns the top 'n' article titles based on their view numbers.
    Parameters:
        n (int): The number of top articles to return.
        interactions (pandas dataframe): The dataframe containing article view numbers.
    Returns:
        list: A list of the top 'n' article titles.
    """
    article_view_number_ranked = interactions['title'].value_counts().sort_values(ascending=False)
    
    top_articles = article_view_number_ranked.index[:n].tolist()
    top_articles =[str(i) for i in top_articles]
    
    return top_articles # Return the top article titles from df (not df_content)

def get_top_article_ids(n, interactions):
    """
    Returns the top 'n' article IDs based on their view numbers.
    Parameters:
        n (int): The number of top articles to return.
        interactions (pandas dataframe, optional): The dataframe containing article view numbers. Defaults to the global variable 'df'.
    Returns:
        list: A list of the top 'n' article IDs.
    """
    article_view_number_ranked = interactions['title'].value_counts().sort_values(ascending=False)
    
    top_articles = article_view_number_ranked.index.values[:n]
    top_articles =[str(i) for i in top_articles]
    
    return top_articles # Return the top article ids


def create_user_item_matrix(interactions):
    """
    Creates a user-item matrix from a given DataFrame.
    Parameters:
        interactions (pandas DataFrame): A DataFrame containing user and article interactions.
    Returns:
        pandas DataFrame: A user-item matrix where rows represent users, columns represent articles, and cell values indicate interaction presence.
    """
    # Get unique user and article ids
    users = interactions['user_id'].unique()
    articles = interactions['article_id'].unique()
    
    # Create a dictionary to map a article_ids to column indices
    article_to_idx = {article: idx for idx, article in enumerate(articles)}
    
    # Create and initializa a user-article matrix with zeros
    user_item = np.zeros((len(users), len(articles)))
    
    # Fill the matrix with 1s when interactions happen
    for i, row in interactions.iterrows():
        user_idx = np.where(users == row['user_id'])[0][0]
        article_idx = article_to_idx[row['article_id']]
        user_item[user_idx, article_idx] = 1
        
    # Create a DataFrame from the numpy array
    user_item = pd.DataFrame(user_item, index=users, columns=articles)
    
    return user_item # return the user_item matrix 

def get_article_names(article_ids, interactions):
    """
    Retrieves a list of article names corresponding to the given article IDs.
    
    Parameters:
        article_ids (list): A list of article IDs.
        interactions (pandas DataFrame, optional): A DataFrame containing article information. Defaults to the global variable 'df'.
    
    Returns:
        list: A list of article names.
    """
    # Filter the df to include the requested article ids only
    interactions_filtered = interactions[interactions['article_id'].isin(article_ids)]
    
    # Get the titles for the filteresd article_ids
    article_names = interactions_filtered['title'].unique().tolist()
    
    # Sort the article names in descending order based on the index of article ids
    article_names = interactions_filtered['title'].unique().tolist()
    #article_names = interactions_filtered[interactions_filtered['article_id'].isin(article_ids)].sort_values(by='article_id')['title'].unique().tolist()
    
    return article_names # Return the article names associated with list of article ids


def get_user_articles(user_id, interactions):
    """
    Retrieves a list of article IDs and their corresponding names that a given user has interacted with.
    
    Parameters:
        user_id (int): The ID of the user to retrieve articles for.
        interactions (pandas DataFrame): A DataFrame containing user and article interactions.
    
    Returns:
        tuple: A tuple containing a list of article IDs and a list of article names.
    """
    user_item = create_user_item_matrix(interactions)
    # Get article ids that user_id has interacted
    article_ids = user_item.columns[user_item.loc[user_id] == 1].tolist()
    
    # Sort the article_ids based on their order in the user_item DataFrame
    article_ids.sort(key=lambda x: list(user_item.loc[user_id]).index(1))
    
    # Get article titles corresponding to the article ids retrieved
    article_names = get_article_names(article_ids, interactions)
    
    article_ids=[str(i) for i in article_ids]
    
    return article_ids, article_names # return the ids and names