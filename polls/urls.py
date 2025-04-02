from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views
from .auth_views import RegisterView, LogoutView, CustomTokenObtainPairView
from .user_views import UserViewSet
from . import role_views
from .department_views import DepartmentViewSet
from .system_monitor import SystemMonitorView
from .operation_log_views import OperationLogViewSet

router = DefaultRouter()
router.register(r'polls', api_views.QuestionViewSet)
router.register(r'users', UserViewSet, basename='users')
router.register(r'roles', role_views.RoleViewSet)
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'operation-logs', OperationLogViewSet, basename='operation-logs')

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/system-monitor/', SystemMonitorView.as_view(), name='system_monitor'),
    path('api/', include(router.urls)),
]