from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import City
from .serializers import CitySerializer

@api_view(['GET', 'POST'])
def city_list(request):
    """List cities or add a new city."""
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_city(request, city_name):
    """Deletes a city from the database."""
    try:
        city = City.objects.get(name=city_name)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except City.DoesNotExist:
        return Response({"detail": "City not found."}, status=status.HTTP_404_NOT_FOUND)
