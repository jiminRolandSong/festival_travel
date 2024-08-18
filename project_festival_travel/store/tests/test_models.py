from django.test import TestCase
from ..models import *
from django.contrib.auth.models import User
from datetime import date

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        #user
        self.user = User.objects.create(username = "jimbo", password = "1234")
        
        #category
        self.category = Category.objects.create(
            name = "City & Festival",
            slug = "ct"
        )
        
        #festival
        self.festival = Festival.objects.create(
            name = "Ultra Japan",
            slug = "ultra-jp",
            location = "Tokyo, Japan",
            start_date = "2024-09-16",
            end_date = "2024-09-18",
            description = "Largest EDM Festival in Japan"
        )
        
        #package
        self.package = Package.objects.create(
            category = self.category,
            festival = self.festival,
            name = "Ultra Japan Package",
            slug = "ujp",
            price = 2000,
            description = "Enjoy Tokyo and EDM",
            featured = False,
            availability = True
        )
        
        #cart
        self.cart = Cart.objects.create(
            user = self.user,
            package = self.package,
            quantity = 2,
            price = self.package.price * 2
        )
        
        #order
        self.order = Order.objects.create(
            user = self.user,
            total_quantity = 2,
            total_price = self.cart.price,
            status = True,
            date = date.today
        )
        
        self.orderItem = OrderItem.objects.create(
            user = self.user,
            order = self.order,
            package = self.package,
            quantity = 2,
            price = 4000
        )
        
    def test_category(self):
        self.assertEqual(self.category.name, "City & Festival")
        self.assertEqual(self.category.slug, "ct")
        
    def test_festival(self):
        self.assertEqual(self.festival.name, "Ultra Japan")
        self.assertEqual(self.festival.start_date, "2024-09-16")
        
    def test_package(self):
        self.assertEqual(self.package.category, self.category)
        self.assertEqual(self.package.festival, self.festival)
        self.assertEqual(self.package.price, 2000)
        self.assertFalse(self.package.featured)
        self.assertTrue(self.package.availability)
        
    def test_cart(self):
        self.assertEqual(self.cart.user.username, "jimbo")
        self.assertEqual(self.cart.quantity, 2)
        self.assertEqual(self.cart.price, 4000)
        
    def test_order(self):
        self.assertEqual(self.order.user.username, "jimbo")
        self.assertEqual(self.order.total_price, 4000)
        self.assertTrue(self.order.status)
        
    def test_orderItem(self):
        self.assertEqual(self.orderItem.user.username, "jimbo")
        self.assertEqual(self.orderItem.order, self.order)
        self.assertEqual(self.orderItem.package, self.package)
        
        
        
        