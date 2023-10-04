from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .auth import adminPermOnly
import jwt

@api_view(['GET'])
@permission_classes([adminPermOnly])
def check(request):
    return Response("pong")
