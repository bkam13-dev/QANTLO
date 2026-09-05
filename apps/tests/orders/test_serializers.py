import uuid
from decimal import Decimal

from django.test import TestCase

from apps.orders.models import Order, OrderItem, Invoice
from apps.orders.serializers import (
    OrderSerializer,
    OrderItemSerializer,
    InvoiceSerializer,
)

from apps.products.models import (
    Product,
    Category,
    Brand,
    Supplier,
    Customer,
)

from apps.users.models import CustomUser


class OrderSerializerTestCase(TestCase):

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

        self.order = Order.objects.create(
            reference="ORD-001",
            created_by=self.user,
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        self.invoice = Invoice.objects.create(
            order=self.order,
            total_amount=Decimal("1300000.00"),
        )


class OrderItemSerializerTest(OrderSerializerTestCase):

    def test_valid_data(self):
        data = {
            "order": self.order.id,
            "product": self.product.id,
            "quantity": 3,
            "unit_price": "650000.00",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_product_is_required(self):
        data = {
            "order": self.order.id,
            "quantity": 3,
            "unit_price": "650000.00",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_quantity_is_required(self):
        data = {
            "order": self.order.id,
            "product": self.product.id,
            "unit_price": "650000.00",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_negative_quantity_is_invalid(self):
        data = {
            "order": self.order.id,
            "product": self.product.id,
            "quantity": -5,
            "unit_price": "650000.00",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_zero_quantity_is_invalid(self):
        data = {
            "order": self.order.id,
            "product": self.product.id,
            "quantity": 0,
            "unit_price": "650000.00",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_unit_price_is_valid(self):
        data = {
            "order": self.order.id,
            "product": self.product.id,
            "quantity": 2,
            "unit_price": "1250.50",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["unit_price"],
            Decimal("1250.50"),
        )

    def test_create_order_item(self):
        data = {
            "order": self.order.id,
            "product": self.product.id,
            "quantity": 3,
            "unit_price": "650000.00",
        }

        serializer = OrderItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        item = serializer.save()

        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 3)

    def test_update_order_item(self):
        serializer = OrderItemSerializer(
            instance=self.order_item,
            data={
                "order": self.order.id,
                "product": self.product.id,
                "quantity": 5,
                "unit_price": "700000.00",
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        item = serializer.save()

        self.assertEqual(item.quantity, 5)
        self.assertEqual(
            item.unit_price,
            Decimal("700000.00"),
        )


class OrderSerializerTest(OrderSerializerTestCase):

    def test_valid_data(self):
        data = {
            "reference": "ORD-002",
            "order_type": Order.OrderType.PURCHASE,
            "status": Order.StatusChoice.PENDING,
            "supplier": self.supplier.id,
            "customer": self.customer.id,
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_reference_is_required(self):
        data = {
            "order_type": Order.OrderType.PURCHASE,
            "status": Order.StatusChoice.PENDING,
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("reference", serializer.errors)

    def test_invalid_order_type(self):
        data = {
            "reference": "ORD-002",
            "order_type": "INVALID",
            "status": Order.StatusChoice.PENDING,
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("order_type", serializer.errors)

    def test_invalid_status(self):
        data = {
            "reference": "ORD-002",
            "order_type": Order.OrderType.PURCHASE,
            "status": "INVALID",
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_nonexistent_supplier_is_invalid(self):
        data = {
            "reference": "ORD-002",
            "order_type": Order.OrderType.PURCHASE,
            "status": Order.StatusChoice.PENDING,
            "supplier": uuid.uuid4(),
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("supplier", serializer.errors)

    def test_nonexistent_customer_is_invalid(self):
        data = {
            "reference": "ORD-002",
            "order_type": Order.OrderType.SALE,
            "status": Order.StatusChoice.PENDING,
            "customer": uuid.uuid4(),
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)

    def test_duplicate_reference_is_invalid(self):
        data = {
            "reference": self.order.reference,
            "order_type": Order.OrderType.PURCHASE,
            "status": Order.StatusChoice.PENDING,
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("reference", serializer.errors)

    def test_create_order(self):
        data = {
            "reference": "ORD-002",
            "order_type": Order.OrderType.PURCHASE,
            "status": Order.StatusChoice.PENDING,
            "supplier": self.supplier.id,
            "created_by": self.user.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        order = serializer.save()

        self.assertEqual(order.reference, "ORD-002")
        self.assertEqual(
            order.order_type,
            Order.OrderType.PURCHASE,
        )

    def test_update_order(self):
        serializer = OrderSerializer(
            instance=self.order,
            data={
                "reference": "ORD-UPDATED",
                "order_type": Order.OrderType.SALE,
                "status": Order.StatusChoice.PROCESSING,
                "created_by": self.user.id,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        order = serializer.save()

        self.assertEqual(
            order.reference,
            "ORD-UPDATED",
        )

        self.assertEqual(
            order.order_type,
            Order.OrderType.SALE,
        )

        self.assertEqual(
            order.status,
            Order.StatusChoice.PROCESSING,
        )


class InvoiceSerializerTest(OrderSerializerTestCase):

    def test_valid_data(self):
        data = {
            "order": self.order.id,
            "total_amount": "1300000.00",
            "is_paid": False,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_total_amount_is_valid(self):
        data = {
            "order": self.order.id,
            "total_amount": "250000.50",
            "is_paid": False,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["total_amount"],
            Decimal("250000.50"),
        )

    def test_invalid_total_amount(self):
        data = {
            "order": self.order.id,
            "total_amount": "abc",
            "is_paid": False,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "total_amount",
            serializer.errors,
        )

    def test_is_paid_accepts_boolean(self):
        data = {
            "order": self.order.id,
            "total_amount": "1300000.00",
            "is_paid": True,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertTrue(
            serializer.validated_data["is_paid"]
        )

    def test_nonexistent_order_is_invalid(self):
        data = {
            "order": uuid.uuid4(),
            "total_amount": "1300000.00",
            "is_paid": False,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("order", serializer.errors)

    def test_invoice_for_order_that_already_has_invoice_is_invalid(self):
        data = {
            "order": self.order.id,
            "total_amount": "1500000.00",
            "is_paid": False,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("order", serializer.errors)

    def test_create_invoice(self):
        new_order = Order.objects.create(
            reference="ORD-002",
            created_by=self.user,
        )

        data = {
            "order": new_order.id,
            "total_amount": "1500000.00",
            "is_paid": False,
        }

        serializer = InvoiceSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        invoice = serializer.save()

        self.assertEqual(
            invoice.order,
            new_order,
        )

        self.assertEqual(
            invoice.total_amount,
            Decimal("1500000.00"),
        )

    def test_update_invoice(self):
        serializer = InvoiceSerializer(
            instance=self.invoice,
            data={
                "order": self.order.id,
                "total_amount": "1500000.00",
                "is_paid": True,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        invoice = serializer.save()

        self.assertEqual(
            invoice.total_amount,
            Decimal("1500000.00"),
        )

        self.assertTrue(invoice.is_paid)