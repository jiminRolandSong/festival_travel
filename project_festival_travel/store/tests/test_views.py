from django.test import TestCase, Client
from ..models import *
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        
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
        
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_categories(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')
        
    def test_festivals(self):
        response = self.client.get(reverse('festivals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'festivals.html')
        self.assertContains(response, self.festival.name)
                    
    def test_show_festival(self):
        response = self.client.get(reverse('festival-item', args = ['ultra-jp']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'festival_item.html')
        self.assertContains(response, self.festival.name)
        
    def test_packages(self):
        response = self.client.get(reverse('packages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages.html')
        self.assertContains(response, self.festival.name)
                    
    def test_show_festival(self):
        response = self.client.get(reverse('package-item', args = ['ujp']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'package_item.html')
        self.assertContains(response, self.package.name)
        
    def test_purchase_process(self):
        self.user = User.objects.create_user(username='jimin', password='1234')
        self.client.login(username='jimin', password='1234')
        
        #add package to the cart two times
        response = self.client.get(reverse('add-to-cart', args = ['ujp']))
        response = self.client.get(reverse('add-to-cart', args = ['ujp']))
        
        #check the items are correctly added to the cart
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('cart.html')
        self.assertContains(response, self.package.name)
        self.assertContains(response, '2')
        
        #checkout the items in the cart
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user).latest('date')
        
        response = self.client.get(reverse('current-order', args=[order.id]))
        self.assertTemplateUsed('current_order.html')
        self.assertContains(response, order.id)
        
        #items in the cart should be deleted
        response = self.client.get(reverse('cart'))
        self.assertNotContains(response, self.package.name)
        
        #check the user can view the order
        response = self.client.get(reverse('orders'), {'order_number': order.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.package.name)
        
        