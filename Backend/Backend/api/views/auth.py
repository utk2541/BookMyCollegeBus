from urllib import response
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from api.serializers import UserLoginSerializer
from api.models import User as User
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class userPerm(BasePermission):
    def has_permission(self, request, view):
        try:
            param = request.headers.get('Authorization','no')
            token = param.encode('utf-8')
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except :
            raise AuthenticationFailed('No credentials')




        id = payload.get('id')
        username = payload.get('username') 

        if float(payload.get('exp')) < datetime.utcnow().timestamp():
            raise AuthenticationFailed('invalid token')
        

        if (id is None) or (username is None):
            return False
        
        try:
            User.objects.get(id=id,username=username)
        except User.DoesNotExist:
            return False

        return True


class adminPermOnly(BasePermission):
    def has_permission(self, request, view):
        try:
            
            param = request.headers.get('Authorization','no')
            token = param.encode('utf-8')
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except :
            raise AuthenticationFailed('No credentials')

        id = payload.get('id')
        username = payload.get('username') 
        
        if float(payload.get('exp')) < datetime.utcnow().timestamp():
            raise AuthenticationFailed('invalid token')

        if (id is None) or (username is None):
            return False     
        
        try:
            User.objects.get(id=id,username=username)
        except User.DoesNotExist:
            return False

        user = User.objects.get(id=id,username=username)

        if user.isAdmin:
            return True
        
        return False




@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        serializer.isAdmin = False
        user = serializer.save()
        if user:
            response = Response({"message" : 'user created'},status = status.HTTP_201_CREATED)
            return response
        else :
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            payload = {
                'id': user.id,  
                'name': user.name,
                'username': user.username,
                'exp': (datetime.utcnow()+timedelta(minutes=180)).timestamp(),
                'iat': datetime.utcnow(),
            }
            print( datetime.utcnow())
            print( datetime.utcnow()+timedelta(minutes=180))
            
            token = jwt.encode(payload=payload, key='secret', algorithm='HS256').decode('utf-8')
            response = Response({"message" : 'user logged in','jwt' : token})
            response.set_cookie(key='jwt', value=token, httponly=True)

            return response

        else:
            return Response({"message" : 'invalid username or password'},status = status.HTTP_403_FORBIDDEN)
    return Response({'message': 'Invalid request method'},status = status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([userPerm])
def user_logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {"message": "Logout successful"}
    return response



    


