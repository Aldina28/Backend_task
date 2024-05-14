from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import CreateUserSerializer, UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser 
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Endpoint for user registration
@api_view(['POST'])
def register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user) #Creation of token for authentication of the user
        return Response({'token': token.key, 'user': serializer.data, 'message': 'User registered successfully'})
    return Response(serializer.errors, status=status.HTTP_200_OK)

# Endpoint for user login
@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("Wrong Password", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data, 'message': 'User is logged in successfully'})  

# Endpoint to test authentication token
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
