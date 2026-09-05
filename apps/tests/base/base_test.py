from django.test import TestCase
from apps.users.models import CustomUser
from apps.products.models import Category, Brand, Supplier, Product       


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="password123",
            role=CustomUser.UserType.STAFF
        )

        self.category = Category.objects.create(
            name="Informatique"
        )

        self.brand = Brand.objects.create(
            name="HP",
            description="Marque informatique"
        )

        self.supplier = Supplier.objects.create(
            company_name="HP CI",
            contact_name="Jean",
            email="hp@example.com",
            phone="0700000000",
            address="Abidjan"
        )

        self.product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP EliteBook",
            purchase_price=500000,
            selling_price=650000
        )
        
        product = Product(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="",
            purchase_price=500000,
            selling_price=650000
        )

        product.full_clean()
        


