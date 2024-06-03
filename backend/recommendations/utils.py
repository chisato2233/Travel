# recommendations/utils.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.models import Attraction

def recommend_attractions(attraction_id, top_n=5):
    attractions = Attraction.objects.all()
    descriptions = [attraction.description for attraction in attractions]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 获取当前景点的索引
    idx = list(attractions).index(Attraction.objects.get(id=attraction_id))

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # 排除自身

    attraction_indices = [i[0] for i in sim_scores]
    recommended_attractions = [attractions[i] for i in attraction_indices]

    return recommended_attractions
