# Recommender_ibmws

Recommender IBMWS package is a Python Package to recommend articles for users of the IBM Watson Studio platform.

This Recommender uses a hybrid approach of Content-Based Filtering and Collaborative Filtering to make recommendations.  
The content base recommendation system developed relies on a user profile, text vectorization, similarity calculation, ranking and recommendation, as well as handling of new users to deal with the cold start problem. 

### How to use:

Import the Recommender
```
from recommender_ibmws.recommender import Recommender
rec = Recommender()
```

Load data
```
rec.load_data(inter_path='user-item-interactions.csv', content_path='articles_community.csv')
```

Make recomendations
```
rec.make_content_recs(user_id=8, m=10)
```

Find number of users
```
rec.n_users
```

