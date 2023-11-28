
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
from decouple import config

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
    userbookings = Booking.objects.select_related(
        'scheduleId',
        'scheduleId__busId'
    ).filter(id=user).values(
        'bookingTime',
        'scheduleId__departure',
        'scheduleId__busId__busNumber'
    )
    return Response(userbookings.all())

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
    openingList = Schedule.objects.select_related('busId').filter(
        BookingStart__lte = currTime,
        BookingEnd__gte = currTime
    ).values(
        'scheduleId',
        'busId__busNumber',
        'availableSeats',
        'BookingStart',
        'BookingEnd',
        'departure'
    ).order_by('BookingEnd')
    
    return Response(openingList.all())


@api_view(['POST'])
@permission_classes([userPerm])
@transaction.atomic
def book(request):
    openingId = request.data['scheduleId']
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
    payload = jwt.decode(token, config('SECRET_KEY'), algorithms=['HS256'])
    param = payload.get(p)
    return param 


    




    
    
