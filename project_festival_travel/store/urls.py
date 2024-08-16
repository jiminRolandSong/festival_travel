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


    path('packages', views.packages, name='packages'),
    path('packages/<slug:slug>', views.show_package, name='package-item'),
    path('api/packages', views.PackagesAPIView.as_view(), name='packages-api'),
    path('api/packages/<slug:slug>', views.SinglePackageAPIView.as_view(), name='package-item-api'),

    path('add-to-cart/<slug:slug>', views.add_to_cart, name='add-to-cart'),
    path('cart', views.cart, name='cart'),
    path('api/cart', views.CartAPIView.as_view(), name='cart-api'),
    
    path('checkout', views.checkout, name='checkout'),
    path('current-order/<int:id>', views.current_order, name='current-order'),
    path('orders', views.order_check, name='orders'),
    #path('orders/<int:pk>', views.OrderItemView.as_view(), name='orderitem'),
    path('api/orders', views.OrderAPIView.as_view(), name='orders-api'),
    path('api/orders/<int:pk>', views.OrderItemAPIView.as_view(), name='orderitem-api'),
]
