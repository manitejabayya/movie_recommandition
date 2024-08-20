# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import pickle

# Load dataset
data = pd.read_csv('dataset.csv')

# Check if necessary columns exist
required_columns = ['id', 'original_title', 'overview', 'genres']
if all(col in data.columns for col in required_columns):
    data = data[required_columns]
else:
    raise ValueError("Dataset does not have the required columns.")

# Fill NaN values to avoid issues
data['overview'] = data['overview'].fillna('')
data['genres'] = data['genres'].fillna('')

# Create 'tags' column by combining overview and genres
data['tags'] = data['overview'] + ' ' + data['genres']

# Drop unnecessary columns
new_data = data.drop(columns=['overview', 'genres'])

# Vectorize the text data
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()

# Calculate cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)

# Recommendation function
def recommend(movie_title):
    index = new_data[new_data['original_title'].str.lower() == movie_title.lower()].index
    if index.empty:
        print(f"No movie found with title '{movie_title}'")
        return

    distances = sorted(list(enumerate(similarity[index[0]])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(new_data.iloc[i[0]].original_title)

# Test the recommendation function
recommend("iron man")

# Save the data and similarity matrix for use in the Streamlit app
pickle.dump(new_data, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
