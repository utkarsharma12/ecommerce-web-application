from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem
from .cart import Cart, CART_SESSION_ID


class EcommerceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.product1 = Product.objects.create(
            name='Test Headphones',
            description='Noise cancelling headphones',
            price=Decimal('1500.00'),
            stock=10,
            category='Electronics'
        )
        self.product2 = Product.objects.create(
            name='Test T-Shirt',
            description='Cotton t-shirt',
            price=Decimal('500.00'),
            stock=5,
            category='Fashion'
        )

    def test_home_page_listing(self):
        """Test home page displays products and filters."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Headphones')
        self.assertContains(response, 'Test T-Shirt')

        # Test search query
        search_res = self.client.get(reverse('home') + '?q=Headphones')
        self.assertContains(search_res, 'Test Headphones')
        self.assertNotContains(search_res, 'Test T-Shirt')

        # Test category filter
        cat_res = self.client.get(reverse('home') + '?category=Fashion')
        self.assertContains(cat_res, 'Test T-Shirt')
        self.assertNotContains(cat_res, 'Test Headphones')

    def test_product_detail_view(self):
        """Test product detail view renders correctly."""
        response = self.client.get(reverse('product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, str(self.product1.price))

    def test_cart_operations(self):
        """Test adding, incrementing, decrementing, and removing from cart."""
        # Add product1 to cart
        response = self.client.post(reverse('cart_add', args=[self.product1.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 302) # Redirects to cart

        # Verify session cart
        session = self.client.session
        self.assertIn(CART_SESSION_ID, session)
        self.assertEqual(session[CART_SESSION_ID][str(self.product1.id)]['quantity'], 2)

        # Decrement quantity
        self.client.get(reverse('cart_decrement', args=[self.product1.id]))
        session = self.client.session
        self.assertEqual(session[CART_SESSION_ID][str(self.product1.id)]['quantity'], 1)

        # Remove from cart
        self.client.get(reverse('cart_remove', args=[self.product1.id]))
        session = self.client.session
        self.assertNotIn(str(self.product1.id), session[CART_SESSION_ID])

    def test_user_registration_and_login(self):
        """Test user registration and authentication."""
        # Register new user
        reg_response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'NewUserPass@2026',
            'password2': 'NewUserPass@2026',
        })
        self.assertEqual(reg_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Logout
        self.client.get(reverse('logout'))

        # Login
        login_response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'NewUserPass@2026',
        })
        self.assertEqual(login_response.status_code, 302)

    def test_checkout_and_order_creation(self):
        """Test complete checkout flow, order creation, and stock reduction."""
        # Log in user
        self.client.login(username='testuser', password='testpassword123')

        # Add items to cart
        self.client.post(reverse('cart_add', args=[self.product1.id]), {'quantity': 2})
        self.client.post(reverse('cart_add', args=[self.product2.id]), {'quantity': 1})

        # Submit checkout form
        checkout_response = self.client.post(reverse('checkout'), {
            'full_name': 'Test Customer',
            'email': 'customer@test.com',
            'phone': '9876543210',
            'shipping_address': '123 Test Street',
            'city': 'Metropolis',
            'postal_code': '123456',
        })

        # Verify redirect to order success
        self.assertEqual(checkout_response.status_code, 302)
        
        # Verify order exists in DB
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, 'Processing')
        # Total = 2 * 1500 + 1 * 500 = 3500
        self.assertEqual(order.total_amount, Decimal('3500.00'))
        self.assertEqual(order.items.count(), 2)

        # Verify product stock reduction
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 8) # 10 - 2 = 8
        self.assertEqual(self.product2.stock, 4) # 5 - 1 = 4

        # Verify cart was cleared
        session = self.client.session
        self.assertNotIn(CART_SESSION_ID, session)

    def test_order_history_view(self):
        """Test order history is accessible and lists user orders."""
        self.client.login(username='testuser', password='testpassword123')

        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('1500.00'),
            status='Delivered',
            full_name='Test Customer'
        )
        OrderItem.objects.create(order=order, product=self.product1, quantity=1, price=self.product1.price)

        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'#{order.id}')
        self.assertContains(response, 'Delivered')
