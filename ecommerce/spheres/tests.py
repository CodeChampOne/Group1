from django.test import TestCase
from .models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(Name="Test Product", Price=50.00, Description="A test product", Stock_Quantity=10)

    def test_product_creation(self):
        """Products are created correctly."""
        product = Product.objects.get(Name="Test Product")
        self.assertEqual(product.Price, 50.00)
        self.assertEqual(product.Stock_Quantity, 10)

    def test_product_update(self):
        """Products are updated correctly."""
        product = Product.objects.get(Name="Test Product")
        product.Price = 60.00
        product.save()
        self.assertEqual(product.Price, 60.00)

    def test_product_deletion(self):
        """Products are deleted correctly."""
        product = Product.objects.get(Name="Test Product")
        product.delete()
        products = Product.objects.all()
        self.assertEqual(products.count(), 0)
