from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.RegisterViewset, basename='register')
router.register('login', views.LoginViewset, basename='login')
router.register('users', views.UserViewSet, basename='users')
urlpatterns = router.urls
