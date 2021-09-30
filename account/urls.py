from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views import UserViewSet, LoginView, RoleViewSet
from tech_three.utils.apps import get_api_url as api

router = DefaultRouter()
router.register(r'roles', RoleViewSet, 'roles')
router.register(r'users', UserViewSet, 'users')

urlpatterns = [
    path(api(app_name='account'), include(router.urls)),
    path(api(url_name='login'), LoginView.as_view(), name="login"),
]
