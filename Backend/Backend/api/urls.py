from django.urls import path

from api.views import auth , random, data


urlpatterns = [

    path('user/registration', auth.user_registration, name='user-registration'),

    path('user/login', auth.user_login, name='user-login'),

    path('user/logout', auth.user_logout, name='user-logout'),

    path('app/allbuses', data.allbuses, name = 'allbuses'),

    path('app/allSchedules', data.allSchedules, name = 'allSchedules'),

    path('app/userBookings', data.userBookings, name = 'userBookings'),

    path('app/addBus', data.addbus, name = 'addbus'),
    
    path('app/addSchedule', data.addschedule, name = 'addschedules'),

    path('app/currentBus', data.currentBuses, name = 'currentbuses'),

     path('app/bookSeat', data.book, name = 'bookSeat')

]