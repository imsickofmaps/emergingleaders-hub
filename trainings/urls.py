from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'attendees', views.AttendeeViewSet)
router.register(r'feedback', views.FeedbackViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
