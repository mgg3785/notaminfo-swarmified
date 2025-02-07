from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('notams',views.NotamsViewSet,basename='notams-parsed-or-not')


notams_router = routers.NestedDefaultRouter(router,'notams',lookup='notam')
notams_router.register('parsed',views.ParsedNotamsViewset,basename='notams-parsed')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(notams_router.urls)),
]