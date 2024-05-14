from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Toy
from .serializers import ToyModelSerializer
from rest_framework.response import Response
from django.db import DatabaseError

#API endpoint to create a new toy.
class ToyCreateAPI(APIView):
    def post(self, request):
        toy_serializer = ToyModelSerializer(data=request.data)
        try:
            if toy_serializer.is_valid():
                toy_serializer.save()
                return Response(toy_serializer.data, status=status.HTTP_201_CREATED)
            return Response(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            error_message = "Failed to create toy: Toy Model exists"
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to update an existing toy.
class ToyUpdateAPI(APIView):
    def put(self, request):
        model = request.data.get("model")
        try:
            toy_obj = Toy.objects.get(model=model)
        except Toy.DoesNotExist:
            return Response({"msg": f"No toy found with model {model}"}, status=status.HTTP_404_NOT_FOUND)
        toy_serializer = ToyModelSerializer(toy_obj, data=request.data, partial=True)
        if toy_serializer.is_valid():
            toy_serializer.save()
            return Response(toy_serializer.data)
        return Response(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#API endpoint to delete an existing toy.
class ToyDeleteAPI(APIView):
    def delete(self, request):
        model = request.data.get("model")
        try:
            toy_obj = Toy.objects.get(model=model)
        except Toy.DoesNotExist:
            return Response({"msg": f"No toy found with model {model}"}, status=status.HTTP_404_NOT_FOUND)

        toy_obj.delete()
        return Response({"msg": "Toy deleted successfully"})

#API endpoint to retrieve details of all toy or a specific toy.
class AllToyDetailsAPI(APIView):
    def get(self, request):
        model = request.data.get("model")
        if model:
            try:
                toy_obj = Toy.objects.get(model=model)
                toy_serializer = ToyModelSerializer(toy_obj)
                return Response(toy_serializer.data)
            except Toy.DoesNotExist:
                return Response({"msg": f"No toy found with model {model}"}, status=status.HTTP_404_NOT_FOUND)
        else:
            toys = Toy.objects.all()
            toy_serializer = ToyModelSerializer(toys, many=True)
            return Response(toy_serializer.data)

#API endpoint to retrieve details of a specific toy.
class ToyDetailsAPI(APIView):
    def get(self, request, model):
        try:
            toy_obj = Toy.objects.get(model=model)
            toy_serializer = ToyModelSerializer(toy_obj)
            return Response(toy_serializer.data)
        except Toy.DoesNotExist:
            return Response({"msg": f"No toy found with model {model}"}, status=status.HTTP_404_NOT_FOUND)