
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Schedule, Booking, Bus,User
from ..serializers import ScheduleSerializer, BookingSerializer, BusSerializer
import jwt 
from .auth import userPerm, adminPermOnly
from datetime import datetime
from django.db import transaction
from django.utils import timezone

@api_view(['GET'])
@permission_classes([userPerm])
def allbuses(request):
    buslist = Bus.objects.all()
    return Response(BusSerializer(buslist,many = True).data)

@api_view(['GET'])
@permission_classes([userPerm])
def allSchedules(request):
    schedulelist = Schedule.objects.all()
    return Response(ScheduleSerializer(schedulelist,many = True).data)

@api_view(['GET'])
@permission_classes([userPerm])
def userBookings(request):
    id = getUserfromReq(request=request,p="id")
    user = User.objects.get(id=id)
    userbookings = Booking.objects.filter(id=user)
    return Response(BookingSerializer(userbookings,many = True).data)

@api_view(['POST'])
@permission_classes([adminPermOnly])
def addbus(request):
    bus = BusSerializer(data=request.data)
    if bus.is_valid():
        bus.save()
        return Response("added",status=status.HTTP_201_CREATED)
    else : 
        return Response("invalid",status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([adminPermOnly])
def addschedule(request):
    schedule = ScheduleSerializer(data=request.data)
    if schedule.is_valid():
        schedule.save()
        return Response("schedule added",status=status.HTTP_201_CREATED)
    else : 
        return Response("invalid",status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([userPerm])
def currentBuses(request):
    currTime = timezone.now()
    openingList = Schedule.objects.filter(BookingStart__lte = currTime,BookingEnd__lte = currTime)
    return Response(ScheduleSerializer(openingList,many = True).data)


@api_view(['POST'])
@permission_classes([userPerm])
@transaction.atomic
def book(request):
    openingId = request.data['id']
    id = getUserfromReq(request=request,p="id")
    user = User.objects.get(id=id)
    opening = Schedule.objects.select_for_update().get(scheduleId = openingId)
    if opening is None:
        return Response("Bad request",status=status.HTTP_400_BAD_REQUEST)

    if opening.availableSeats > 0:
        Booking.objects.create(id = user,bookingTime = datetime.utcnow(),scheduleId = opening)
        opening.availableSeats -= 1
        opening.save()
    else:
        return Response("No Seat Available",status=status.HTTP_409_CONFLICT)
    
    return Response("Booked",status=status.HTTP_201_CREATED)

def getUserfromReq(request,p):
    tokenS = request.headers.get('Authorization','no')
    token = tokenS.encode('utf-8')
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    param = payload.get(p)
    return param 


    




    
    