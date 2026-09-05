from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, ProtectedError
from django.test import TestCase

from apps.orders.models import Order, OrderItem, Invoice
from apps.products.models import Product, Category, Brand, Supplier, Customer
from apps.users.models import CustomUser


class OrderEdgeCaseTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="order_user",
            password="Password123!",
            role=CustomUser.UserType.STAFF,
        )

        self.category = Category.objects.create(
            name="Informatique"
        )

        self.brand = Brand.objects.create(
            name="Dell",
            description="Dell products"
        )

        self.supplier = Supplier.objects.create(
            company_name="Dell CI",
            contact_name="Jean Supplier",
            email="supplier@example.com",
            phone="0700000000",
            address="Abidjan"
        )

        self.customer = Customer.objects.create(
            company_name="Client CI",
            contact_name="Jean Client",
            first_name="Jean",
            last_name="Client",
            email="client@example.com",
            phone="0500000000",
            address="Abidjan"
        )

        self.product = Product.objects.create(
            name="Laptop Dell",
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            purchase_price=Decimal("500000.00"),
            selling_price=Decimal("650000.00"),
        )

    def create_order(
        self,
        reference="CMD-001",
        status=Order.StatusChoice.PENDING,
    ):
        return Order.objects.create(
            reference=reference,
            status=status,
            order_type=Order.OrderType.SALE,
            supplier=self.supplier,
            customer=self.customer,
            created_by=self.user,
        )

    def test_duplicate_reference_is_rejected(self):

        self.create_order(reference="CMD-001")

        with self.assertRaises(IntegrityError):
            self.create_order(reference="CMD-001")

    def test_reference_is_case_sensitive(self):

        self.create_order(reference="CMD-001")

        order = self.create_order(reference="cmd-001")

        self.assertEqual(order.reference, "cmd-001")


    def test_order_item_zero_quantity_fails_validation(self):

        order = self.create_order()

        item = OrderItem(
            order=order,
            product=self.product,
            quantity=0,
            unit_price=Decimal("650000.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_order_item_negative_quantity_fails_validation(self):

        order = self.create_order()

        item = OrderItem(
            order=order,
            product=self.product,
            quantity=-5,
            unit_price=Decimal("650000.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_order_item_positive_quantity_is_valid(self):

        order = self.create_order()

        item = OrderItem(
            order=order,
            product=self.product,
            quantity=5,
            unit_price=Decimal("650000.00"),
        )

        item.full_clean()

        self.assertEqual(item.quantity, 5)


    def test_order_item_total_with_large_quantity(self):

        order = self.create_order()

        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=100,
            unit_price=Decimal("650000.00"),
        )

        expected_total = Decimal("65000000.00")

        self.assertEqual(
            item.total_amount_item,
            expected_total
        )

    def test_order_item_total_with_decimal_price(self):

        order = self.create_order()

        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            unit_price=Decimal("1250.75"),
        )

        expected_total = Decimal("3752.25")

        self.assertEqual(
            item.total_amount_item,
            expected_total
        )


    def test_product_cannot_be_deleted_if_used_by_order_item(self):


        order = self.create_order()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        with self.assertRaises(ProtectedError):
            self.product.delete()


    def test_deleting_order_deletes_order_items(self):

        order = self.create_order()

        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        item_id = item.id

        order.delete()

        self.assertFalse(
            OrderItem.objects.filter(id=item_id).exists()
        )


    def test_pending_order_does_not_create_invoice(self):

        order = self.create_order(
            reference="CMD-PENDING",
            status=Order.StatusChoice.PENDING,
        )

        self.assertFalse(
            Invoice.objects.filter(order=order).exists()
        )

    def test_processing_order_does_not_create_invoice(self):

        order = self.create_order(
            reference="CMD-PROCESSING",
            status=Order.StatusChoice.PROCESSING,
        )

        self.assertFalse(
            Invoice.objects.filter(order=order).exists()
        )

    def test_cancelled_order_does_not_create_invoice(self):

        order = self.create_order(
            reference="CMD-CANCELLED",
            status=Order.StatusChoice.CANCELLED,
        )

        self.assertFalse(
            Invoice.objects.filter(order=order).exists()
        )

    def test_completed_order_creates_invoice(self):

        order = self.create_order(
            reference="CMD-COMPLETED"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("650000.00"),
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        self.assertTrue(
            Invoice.objects.filter(order=order).exists()
        )

    def test_completed_order_invoice_total_is_correct(self):

        order = self.create_order(
            reference="CMD-TOTAL"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("100000.00"),
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            unit_price=Decimal("50000.00"),
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        invoice = Invoice.objects.get(order=order)

        expected_total = (
            Decimal("2") * Decimal("100000.00")
            + Decimal("3") * Decimal("50000.00")
        )

        self.assertEqual(
            invoice.total_amount,
            expected_total
        )

    def test_completed_order_creates_only_one_invoice(self):


        order = self.create_order(
            reference="CMD-ONE-INVOICE"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("650000.00"),
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        order.save()

        order.save()

        self.assertEqual(
            Invoice.objects.filter(order=order).count(),
            1
        )

    def test_invoice_relationship_is_one_to_one(self):


        order = self.create_order(
            reference="CMD-INVOICE-ONE"
        )

        invoice = Invoice.objects.create(
            order=order,
            total_amount=Decimal("100000.00"),
        )

        self.assertEqual(
            invoice.order,
            order
        )

        with self.assertRaises(IntegrityError):
            Invoice.objects.create(
                order=order,
                total_amount=Decimal("200000.00"),
            )


    def test_completed_order_keeps_invoice_when_status_changes(self):


        order = self.create_order(
            reference="CMD-STATUS"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("650000.00"),
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        self.assertTrue(
            Invoice.objects.filter(order=order).exists()
        )

        order.status = Order.StatusChoice.PENDING
        order.save()

        self.assertTrue(
            Invoice.objects.filter(order=order).exists()
        )


    def test_saving_completed_order_again_does_not_duplicate_invoice(self):


        order = self.create_order(
            reference="CMD-RE-SAVE"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("100000.00"),
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        invoice_id = Invoice.objects.get(order=order).id

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        invoice = Invoice.objects.get(order=order)

        self.assertEqual(
            invoice.id,
            invoice_id
        )

        self.assertEqual(
            Invoice.objects.filter(order=order).count(),
            1
        )


    def test_completed_order_without_items_creates_zero_invoice(self):

        order = self.create_order(
            reference="CMD-NO-ITEM"
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        invoice = Invoice.objects.get(order=order)

        self.assertEqual(
            invoice.total_amount,
            Decimal("0")
        )


    def test_invoice_total_is_recalculated_when_completed_order_is_saved(self):

        order = self.create_order(
            reference="CMD-RECALCULATE"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("100000.00"),
        )

        order.status = Order.StatusChoice.COMPLETED
        order.save()

        invoice = Invoice.objects.get(order=order)

        self.assertEqual(
            invoice.total_amount,
            Decimal("100000.00")
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("50000.00"),
        )

        order.save()

        invoice.refresh_from_db()

        self.assertEqual(
            invoice.total_amount,
            Decimal("200000.00")
        )


    def test_order_without_supplier_is_valid(self):


        order = Order.objects.create(
            reference="CMD-NO-SUPPLIER",
            order_type=Order.OrderType.SALE,
            status=Order.StatusChoice.PENDING,
            customer=self.customer,
            created_by=self.user,
        )

        self.assertIsNone(order.supplier)


    def test_order_without_customer_is_valid(self):

        order = Order.objects.create(
            reference="CMD-NO-CUSTOMER",
            order_type=Order.OrderType.PURCHASE,
            status=Order.StatusChoice.PENDING,
            supplier=self.supplier,
            created_by=self.user,
        )

        self.assertIsNone(order.customer)