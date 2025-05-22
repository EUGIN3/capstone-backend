from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.RegisterViewset, basename='register')
router.register('login', views.LoginViewset, basename='login')
router.register('users', views.UserViewSet, basename='users')
router.register('profile', views.UserProfileViewSet, basename='profile')
router.register('set_appointments', views.SetAppointmentViewSet, basename='set_appointments')
router.register('appointments', views.AppointmentsListViewSet, basename='appointments')
router.register('user_appointments', views.UserAppointmentsViewSet, basename='user_appointments')

router.register('unavailability', views.UnavailabilityViewSet, basename='unavailability')    
urlpatterns = router.urls

