import uuid
from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from apps.orders.models import Order, OrderItem, Invoice
from apps.products.models import (
    Product,
    Category,
    Brand,
    Supplier,
    Customer,
)
from apps.users.models import CustomUser


class OrderModelTest(TestCase):

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

        self.customer = Customer.objects.create(
            contact_name="Jean Paul",
            first_name="Jean",
            last_name="Paul",
            email="customer@example.com",
            phone="0500000000",
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

    def test_create_order(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertIsNotNone(order.id)
        self.assertEqual(order.reference, "ORD-001")
        self.assertEqual(order.created_by, self.user)

    def test_order_id_is_uuid(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertIsInstance(order.id, uuid.UUID)

    def test_order_reference_is_unique(self):
        Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        with self.assertRaises(IntegrityError):
            Order.objects.create(
                reference="ORD-001",
                created_by=self.user,
            )

    def test_default_order_type_is_purchase(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertEqual(
            order.order_type,
            Order.OrderType.PURCHASE,
        )

    def test_purchase_order(self):
        order = Order.objects.create(
            reference="ORD-001",
            order_type=Order.OrderType.PURCHASE,
            created_by=self.user,
        )

        self.assertEqual(
            order.order_type,
            Order.OrderType.PURCHASE,
        )

    def test_sale_order(self):
        order = Order.objects.create(
            reference="ORD-002",
            order_type=Order.OrderType.SALE,
            created_by=self.user,
        )

        self.assertEqual(
            order.order_type,
            Order.OrderType.SALE,
        )

    def test_default_status_is_pending(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertEqual(
            order.status,
            Order.StatusChoice.PENDING,
        )

    def test_processing_status(self):
        order = Order.objects.create(
            reference="ORD-001",
            status=Order.StatusChoice.PROCESSING,
            created_by=self.user,
        )

        self.assertEqual(
            order.status,
            Order.StatusChoice.PROCESSING,
        )

    def test_completed_status(self):
        order = Order.objects.create(
            reference="ORD-002",
            status=Order.StatusChoice.COMPLETED,
            created_by=self.user,
        )

        self.assertEqual(
            order.status,
            Order.StatusChoice.COMPLETED,
        )

    def test_cancelled_status(self):
        order = Order.objects.create(
            reference="ORD-003",
            status=Order.StatusChoice.CANCELLED,
            created_by=self.user,
        )

        self.assertEqual(
            order.status,
            Order.StatusChoice.CANCELLED,
        )

    def test_order_supplier_relationship(self):
        order = Order.objects.create(
            reference="ORD-001",
            supplier=self.supplier,
            created_by=self.user,
        )

        self.assertEqual(order.supplier, self.supplier)

    def test_order_can_exist_without_supplier(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertIsNone(order.supplier)

    def test_order_customer_relationship(self):
        order = Order.objects.create(
            reference="ORD-001",
            customer=self.customer,
            created_by=self.user,
        )

        self.assertEqual(order.customer, self.customer)

    def test_order_can_exist_without_customer(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertIsNone(order.customer)

    def test_order_created_by_relationship(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertEqual(order.created_by, self.user)

    def test_created_at_is_set_automatically(self):
        order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.assertIsNotNone(order.created_at)


class OrderItemModelTest(TestCase):

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

        self.order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

    def test_create_order_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        self.assertIsNotNone(item.id)
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(
            item.unit_price,
            Decimal("650000.00"),
        )

    def test_order_item_quantity(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,
            unit_price=Decimal("650000.00"),
        )

        self.assertEqual(item.quantity, 5)

    def test_order_item_unit_price(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.50"),
        )

        self.assertEqual(
            item.unit_price,
            Decimal("650000.50"),
        )

    def test_total_amount_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        self.assertEqual(
            item.total_amount_item,
            Decimal("1300000.00"),
        )

    def test_total_amount_with_quantity_one(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("650000.00"),
        )

        self.assertEqual(
            item.total_amount_item,
            Decimal("650000.00"),
        )

    def test_total_amount_with_decimal_price(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            unit_price=Decimal("1250.50"),
        )

        self.assertEqual(
            item.total_amount_item,
            Decimal("3751.50"),
        )

    def test_order_has_items_relationship(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        self.assertIn(
            item,
            self.order.items.all(),
        )

    def test_order_items_are_deleted_when_order_is_deleted(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        item_id = item.id

        self.order.delete()

        self.assertFalse(
            OrderItem.objects.filter(id=item_id).exists()
        )


class InvoiceModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="jean",
            password="Password123",
        )

        self.order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

    def test_create_invoice(self):
        invoice = Invoice.objects.create(
            order=self.order,
            total_amount=Decimal("1300000.00"),
        )

        self.assertIsNotNone(invoice.id)
        self.assertEqual(invoice.order, self.order)
        self.assertEqual(
            invoice.total_amount,
            Decimal("1300000.00"),
        )

    def test_invoice_is_unpaid_by_default(self):
        invoice = Invoice.objects.create(
            order=self.order,
            total_amount=Decimal("1300000.00"),
        )

        self.assertFalse(invoice.is_paid)

    def test_invoice_can_be_marked_as_paid(self):
        invoice = Invoice.objects.create(
            order=self.order,
            total_amount=Decimal("1300000.00"),
            is_paid=True,
        )

        self.assertTrue(invoice.is_paid)

    def test_invoice_issued_at_is_set(self):
        invoice = Invoice.objects.create(
            order=self.order,
            total_amount=Decimal("1300000.00"),
        )

        self.assertIsNotNone(invoice.issued_at)

    def test_order_can_have_only_one_invoice(self):
        Invoice.objects.create(
            order=self.order,
            total_amount=Decimal("1300000.00"),
        )

        with self.assertRaises(IntegrityError):
            Invoice.objects.create(
                order=self.order,
                total_amount=Decimal("1500000.00"),
            )