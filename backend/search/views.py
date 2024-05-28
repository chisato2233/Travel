from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Attraction
from .serializers import AttractionSerializer

@api_view(['GET'])
def get_attraction(request, item_id):
    try:
        attraction = Attraction.objects.get(id=item_id)
        serializer = AttractionSerializer(attraction)
        return Response(serializer.data)
    except Attraction.DoesNotExist:
        return Response({"error": "Attraction not found"}, status=404)
