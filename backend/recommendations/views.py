
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import load_data, create_tfidf_vectorizer, preprocess_data, calculate_tfidf_matrix, calculate_cosine_similarity
from .serializers import RecommendationSerializer


# 首次登陆 随机推荐
# 记录用户点击的
@api_view(['GET'])
def recommend_items(request, item_id):
    data = load_data()
    tfidf = create_tfidf_vectorizer()
    data = preprocess_data(data)
    tfidf_matrix = calculate_tfidf_matrix(tfidf, data)
    cosine_sim = calculate_cosine_similarity(tfidf_matrix)

    if item_id in data['名称'].values:
        idx = data[data['名称'] == item_id].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        item_indices = [i[0] for i in sim_scores]
        recommended_items = data['名称'].iloc[item_indices]
    else:
        recommended_items = "暂无此景点信息"

    serializer = RecommendationSerializer(data={'item_id': item_id, 'recommended_items': recommended_items})
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)