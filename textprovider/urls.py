from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('notams',views.NotamsViewSet,basename='notams-parsed-or-not')


urlpatterns = [
    path(r'', include(router.urls)),
]