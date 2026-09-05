from decimal import Decimal

from django.test import TestCase

from apps.orders.models import (
    Order,
    OrderItem,
    Invoice,
)
from apps.products.models import Brand, Category, Product, Supplier
from apps.users.models import CustomUser


class InvoiceSignalTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="jean",
            password="Password123",
        )

        self.category = Category.objects.create(
            name="Electronique",
        )

        self.brand = Brand.objects.create(
            name="Samsung",
            description="Samsung brand",
        )

        self.supplier = Supplier.objects.create(
            company_name="Samsung CI",
            contact_name="Paul",
            email="supplier@example.com",
            phone="0700000000",
            address="Abidjan",
        )


        self.product = Product.objects.create(
            name="Galaxy S25",
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            purchase_price=Decimal("500000.00"),
            selling_price=Decimal("650000.00"),
        )



    def test_invoice_created_when_order_completed(self):

        order = Order.objects.create(
            reference="CMD001",
            created_by=self.user,
            status=Order.StatusChoice.COMPLETED
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("150000")
        )



