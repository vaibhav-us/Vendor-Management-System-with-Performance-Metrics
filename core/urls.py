from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('vendors/',views.vendors_create_list),
    path('vendors/<str:id>/',views.vendors_retrieve_update_destroy),
    path('purchase_orders/',views.po_create_list),
    path('purchase_order/<str:id>/',views.po_retreive_update_delete),
    path('vendors/<str:id>/performance/',views.vendor_performance),
    path('purchase_orders/<str:id>/acknowledge/', views.acknowledge_orders),
]
