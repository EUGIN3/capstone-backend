# from . import views
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('register', views.RegisterViewset, basename='register')
# router.register('login', views.LoginViewset, basename='login')
# router.register('users', views.UserViewSet, basename='users')
# router.register('profile', views.UserProfileViewSet, basename='profile')
# router.register('set_appointments', views.SetAppointmentViewSet, basename='set_appointments')
# router.register('appointments', views.AppointmentsListViewSet, basename='appointments')
# urlpatterns = router.urls


from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Authentication routes (signup, login)
router.register('signup', views.RegisterViewset, basename='signup')  # renamed from 'register'
router.register('login', views.LoginViewset, basename='login')

# User-related routes
router.register('users', views.UserViewSet, basename='users')  # This could handle user-specific actions (list, retrieve, etc.)
router.register('profile', views.UserProfileViewSet, basename='profile')
# router.register('users/<int:user_id>/profile/', views.UserProfileViewSet.as_view({'get': 'retrieve'}), name='user_profile_detail')

# Appointment routes
router.register('appointments', views.AppointmentsListViewSet, basename='appointments')  # List of all appointments
router.register('appointments/set', views.SetAppointmentViewSet, basename='set_appointments')  # Creating new appointments

# Ensure the URLs are organized logically
urlpatterns = router.urls
