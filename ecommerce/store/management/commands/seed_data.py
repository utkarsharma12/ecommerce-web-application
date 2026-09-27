from decimal import Decimal
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from store.models import Product, Order, OrderItem
from PIL import Image, ImageDraw, ImageFont


class Command(BaseCommand):
    help = 'Seeds database with admin user, test customer, and sample products with images'

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # 1. Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: admin (password: admin123)"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2. Demo Customer
        customer_user, created = User.objects.get_or_create(
            username='customer',
            defaults={
                'email': 'customer@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo customer: customer (password: customer123)"))
        else:
            self.stdout.write("Demo customer 'customer' already exists.")

        # 3. Create Media Directory
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)

        # Helper to create product placeholder images
        def generate_image(filename, text, bg_color):
            filepath = os.path.join(media_products_dir, filename)
            img = Image.new('RGB', (600, 450), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Simple decorative border
            draw.rectangle([15, 15, 585, 435], outline=(255, 255, 255, 120), width=3)
            
            # Text label
            draw.text((300, 225), text, fill=(255, 255, 255), anchor="mm")
            img.save(filepath, 'JPEG', quality=90)
            return f"products/{filename}"

        sample_products = [
            {
                'name': 'Wireless Noise-Canceling Headphones',
                'description': 'Premium over-ear wireless headphones with active noise cancellation, 30-hour battery life, and crystal-clear acoustic fidelity.',
                'price': Decimal('2499.00'),
                'stock': 20,
                'category': 'Electronics',
                'img_file': 'headphones.jpg',
                'img_label': 'Wireless Headphones 🎧',
                'bg_color': (49, 46, 129),
            },
            {
                'name': 'Smart Fitness Watch Series 5',
                'description': 'Track heart rate, sleep quality, daily steps, and workout sessions with an ultra-bright AMOLED display and 7-day battery endurance.',
                'price': Decimal('1999.00'),
                'stock': 25,
                'category': 'Electronics',
                'img_file': 'smartwatch.jpg',
                'img_label': 'Smart Fitness Watch ⌚',
                'bg_color': (14, 116, 144),
            },
            {
                'name': 'Ergonomic Aluminum Laptop Stand',
                'description': 'Adjustable height laptop riser engineered from lightweight anodized aluminum with heat ventilation and non-slip rubber pads.',
                'price': Decimal('799.00'),
                'stock': 35,
                'category': 'Electronics',
                'img_file': 'laptop_stand.jpg',
                'img_label': 'Laptop Stand 💻',
                'bg_color': (51, 65, 85),
            },
            {
                'name': 'Classic Cotton Crewneck T-Shirt',
                'description': '100% combed organic cotton everyday crewneck t-shirt. Breathable, durable, pre-shrunk, and tailored for maximum comfort.',
                'price': Decimal('499.00'),
                'stock': 50,
                'category': 'Fashion',
                'img_file': 'tshirt.jpg',
                'img_label': 'Classic Crewneck 👕',
                'bg_color': (30, 41, 59),
            },
            {
                'name': 'Premium Vintage Denim Jacket',
                'description': 'Timeless button-down trucker denim jacket crafted with heavy-gauge denim, dual chest pockets, and classic copper hardware.',
                'price': Decimal('1899.00'),
                'stock': 15,
                'category': 'Fashion',
                'img_file': 'denim_jacket.jpg',
                'img_label': 'Denim Jacket 🧥',
                'bg_color': (37, 99, 235),
            },
            {
                'name': 'Minimalist Urban Casual Sneakers',
                'description': 'Low-top lightweight street sneakers equipped with cushioned memory foam insoles, breathable canvas upper, and anti-slip rubber soles.',
                'price': Decimal('1499.00'),
                'stock': 18,
                'category': 'Footwear',
                'img_file': 'sneakers.jpg',
                'img_label': 'Urban Sneakers 👟',
                'bg_color': (16, 185, 129),
            },
            {
                'name': 'Double-Wall Insulated Steel Flask (750ml)',
                'description': 'Vacuum insulated food-grade 304 stainless steel bottle. Keeps cold beverages chilled for 24 hours and hot coffee hot for 12 hours.',
                'price': Decimal('649.00'),
                'stock': 40,
                'category': 'Home & Kitchen',
                'img_file': 'flask.jpg',
                'img_label': 'Thermal Flask 🍶',
                'bg_color': (217, 119, 6),
            },
            {
                'name': 'Dimmable Eye-Care LED Desk Lamp',
                'description': 'Modern folding architect desk lamp featuring 5 color modes, 10 brightness steps, touch controls, and a USB charging port.',
                'price': Decimal('1199.00'),
                'stock': 12,
                'category': 'Home & Kitchen',
                'img_file': 'desk_lamp.jpg',
                'img_label': 'LED Desk Lamp 💡',
                'bg_color': (79, 70, 229),
            },
            {
                'name': 'Handcrafted Executive Leather Journal',
                'description': '240 pages of bleed-resistant archival cream paper bound in full-grain genuine leather with a ribbon bookmark and pen holder loop.',
                'price': Decimal('399.00'),
                'stock': 60,
                'category': 'Stationery',
                'img_file': 'journal.jpg',
                'img_label': 'Leather Journal 📓',
                'bg_color': (120, 53, 15),
            },
        ]

        created_products = []
        for p_data in sample_products:
            img_rel_path = generate_image(p_data['img_file'], p_data['img_label'], p_data['bg_color'])
            prod, created = Product.objects.update_or_create(
                name=p_data['name'],
                defaults={
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'stock': p_data['stock'],
                    'category': p_data['category'],
                    'image': img_rel_path,
                }
            )
            created_products.append(prod)
            status_text = "Created" if created else "Updated"
            self.stdout.write(f"- {status_text} product: {prod.name} (Rs. {prod.price})")

        # 4. Create a Sample Past Order for Demo Customer
        if not Order.objects.filter(user=customer_user).exists() and len(created_products) >= 2:
            p1 = created_products[0]
            p2 = created_products[3]
            order = Order.objects.create(
                user=customer_user,
                total_amount=Decimal(p1.price * 1 + p2.price * 2),
                status='Delivered',
                full_name='John Doe',
                email='customer@example.com',
                phone='9876543210',
                shipping_address='Flat 402, Sunshine Apartments, MG Road',
                city='Bangalore',
                postal_code='560001'
            )
            OrderItem.objects.create(order=order, product=p1, quantity=1, price=p1.price)
            OrderItem.objects.create(order=order, product=p2, quantity=2, price=p2.price)
            self.stdout.write(self.style.SUCCESS(f"Created demo past order #{order.id} for customer."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
