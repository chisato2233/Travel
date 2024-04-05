import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load_data():
    data = pd.read_excel("旅游景点.xlsx")
    return data

def create_tfidf_vectorizer():
    tfidf = TfidfVectorizer(stop_words='english')
    return tfidf

def preprocess_data(data):
    data['简介'] = data['简介'].fillna('')
    return data

def calculate_tfidf_matrix(tfidf, data):
    tfidf_matrix = tfidf.fit_transform(data['简介'])
    return tfidf_matrix

def calculate_cosine_similarity(tfidf_matrix):
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim