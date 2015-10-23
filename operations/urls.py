from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'trainers', views.TrainerViewSet)
router.register(r'participants', views.ParticipantViewSet)
router.register(r'locations', views.LocationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
