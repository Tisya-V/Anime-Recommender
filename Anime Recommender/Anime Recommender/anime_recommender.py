#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from fileReaders import *


# # Read tables

# In[4]:

def checkpoint(num):
    print(num)

def generate_recommendations():
    print("Generating Recommendations...")
    ratings = pd.read_csv("rating2.csv")
    animes = pd.read_csv("anime3.csv",delimiter="^")
    anime_dataset = pd.merge(ratings,animes).drop(["genre", "type", "episodes", "members", "movie_rating"], axis=1)

    checkpoint(1)
    #anime_dataset['rating'] = pd.to_numeric(anime_dataset['rating'], errors='ignore', downcast='integer')
    #anime_dataset.head()        


    # # Create Pivot Table

    # In[5]:


    anime_data = anime_dataset.pivot_table(index=['user_id'], columns=['name'], values='rating')
    anime_data = anime_data.fillna(0)
    checkpoint(2)
    #anime_data.head()


    # # Build Similarity Matrix

    # In[6]:


    item_similarity_df = anime_data.corr(method='pearson')
    checkpoint(3)
    #item_similarity_df.head(10)


    # # Method to generate similar animes to recommend

    # In[7]:


    def get_similar_animes(anime_name, user_rating):
        similar_score = item_similarity_df[anime_name]*(user_rating - 5)
        similar_score = similar_score.sort_values(ascending=False)

        return similar_score

    


    # In[8]:


    read_my_ratings("my_ratings.txt")


    # In[9]:


    me = read_my_ratings("my_ratings.txt")

    similar_animes = pd.DataFrame()

    for anime,rating in me:
        similar_animes = similar_animes.append(get_similar_animes(anime,rating), ignore_index=False)

    similar_animes = similar_animes.sum().sort_values(ascending=False)
    checkpoint(4)
    #similar_animes.head()

    similar_animes.to_csv("recommendations.csv",sep="^")
    checkpoint(5)


#generate_recommendations()
# In[10]:


#recommendations_file = "Recommendations.csv"
#similar_animes.to_csv(recommendations_file,sep="^")


# In[15]:


#my_recommendations = read_my_recommendations(recommendations_file,me,100)
#print(my_recommendations)


# 

# In[ ]:





# 

# 
