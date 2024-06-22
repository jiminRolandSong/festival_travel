from django.urls import path
from . import views

urlpatterns = [
 
    path('', views.home, name='home'),

    path('categories', views.categories, name='category'),
    path('api/categories', views.CategoriesAPIView.as_view(), name='category-api'),

    path('festivals', views.festivals, name='festivals'),
    path('festivals/<slug:slug>', views.show_festival, name='festival-item'),
    path('api/festivals', views.FestivalsAPIView.as_view(), name='festivals-api'),
    path('api/festivals/<slug:slug>', views.SingleFestivalAPIView.as_view(), name='festival-detail-api'),


    #path('packages', views.PackagesView.as_view(), name='packages'),
    #path('packages/<slug:slug>', views.SinglePackageView.as_view(), name='package-detail'),
    #path('api/packages', views.PackagesAPIView.as_view(), name='packages-api'),
    #path('api/packages/<slug:slug>', views.SinglePackageAPIView.as_view(), name='package-detail-api'),


    #path('cart', views.CartView.as_view(), name='cart'),
    #path('api/cart', views.CartAPIView.as_view(), name='cart-api'),

    #path('orders', views.OrdersView.as_view(), name='orders'),
    #path('orders/<int:pk>', views.OrderItemView.as_view(), name='orderitem'),
    #path('api/orders', views.OrdersAPIView.as_view(), name='orders-api'),
    #path('api/orders/<int:pk>', views.OrderItemAPIView.as_view(), name='orderitem-api'),
]
