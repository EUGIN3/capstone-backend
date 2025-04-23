from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.RegisterViewset, basename='register')
router.register('login', views.LoginViewset, basename='login')
router.register('users', views.UserViewSet, basename='users')
router.register('set_appointments', views.SetAppointmentViewSet, basename='set_appointments')
router.register('appointments', views.AppointmentsListViewSet, basename='appointments')
urlpatterns = router.urls
