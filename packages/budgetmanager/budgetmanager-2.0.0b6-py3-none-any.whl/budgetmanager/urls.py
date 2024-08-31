'''
URL configuration for budgetmanager app
'''
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'budgetmanager'  # pylint: disable=invalid-name
router = DefaultRouter()
router.register(r'budget', views.BudgetViewSet)
router.register(r'share', views.BudgetShareViewSet)
router.register(r'payee', views.PayeeViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'code', views.ShareCodeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/total/', views.TotalView.as_view()),
    path('api/join/', views.JoinBudgetView.as_view()),
    path('api/export/', views.ExportView.as_view()),
    path('manifest.webmanifest', views.manifest_view),
    path('service-worker.js', views.service_worker_view),
    path('', views.index_view, name='index'),
    re_path(r'^.*/$', views.index_view),
]
