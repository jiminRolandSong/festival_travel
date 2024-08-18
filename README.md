## Project Title: Festival Travel E-Commerce Platform
- This is a Django-based e-commerce platform designed for selling and managing festival travel packages. 
The platform allows users to browse through various categories, festivals, packages, add packages to a cart, place orders and check completed orders. The project also includes a set of RESTful APIs for interacting with the backend.

## Features
- Browse Categories: View a list of festival categories.
- Browse Festivals: View festivals with detailed information on each festival.
- Browse Packages: View packages associated with specific festivals.
- Shopping Cart: Add packages to your cart and view your cart contents.
- Order Management: Place orders for packages in your cart, and manage your orders.


## URL Structure

# Web Views
- Home:
path('', views.home, name='home')

- Categories:
path('categories', views.categories, name='category')

- Festivals:
path('festivals', views.festivals, name='festivals')
path('festivals/<slug:slug>', views.show_festival, name='festival-item')

- Packages:
path('packages', views.packages, name='packages')
path('packages/<slug:slug>', views.show_package, name='package-item')

- Cart:
path('add-to-cart/<slug:slug>', views.add_to_cart, name='add-to-cart')
path('cart', views.cart, name='cart')

- Checkout & Orders:
path('checkout', views.checkout, name='checkout')
path('current-order/<int:id>', views.current_order, name='current-order')
path('orders', views.order_check, name='orders'),

# API Endpoints
- Categories API:
path('api/categories', views.CategoriesAPIView.as_view(), name='category-api')

- Festivals API:
path('api/festivals', views.FestivalsAPIView.as_view(), name='festivals-api')
path('api/festivals/<slug:slug>', views.SingleFestivalAPIView.as_view(), name='festival-detail-api')

- Packages API:
path('api/packages', views.PackagesAPIView.as_view(), name='packages-api')
path('api/packages/<slug:slug>', views.SinglePackageAPIView.as_view(), name='package-item-api')

- Cart API:
path('api/cart', views.CartAPIView.as_view(), name='cart-api')

- Orders API:
path('api/orders', views.OrderAPIView.as_view(), name='orders-api')
path('api/orders/<int:pk>', views.OrderItemAPIView.as_view(), name='orderitem-api')

## API Usage
- Authentication: Use token-based authentication for accessing the APIs.
- Filtering: Use query parameters for filtering results (e.g., /api/festivals?start_date=2025-03-28).
- CRUD Operations: Create, read, update, and delete resources through the API.
