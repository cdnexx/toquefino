from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index_page),
    path('order', views.order_page),
    path('delivery', views.delivery_page),
    path('complaints', views.complaints_page),
    path('order/order_id=<int:order_id>', views.order_page),
    path('order/product=<str:barcode>', views.product_page),
    path('order/order_id=<int:order_id>/product=<str:barcode>', views.product_page),
    path('api/order/add', views.add_product, name='add_product'),
    path('order/order_id=<int:order_id>/confirm', views.confirm_order),
    path('order/order_id=<int:order_id>/cancel', views.cancel_order),
    path('order/order_id=<int:order>/voucher', views.gen_pdf),
    path('payment', views.payment, name='payment'),
    path('payment/proceder_pago/order_id=<int:order_id>', views.proceder_pago, name='proceder_pago'),


]

