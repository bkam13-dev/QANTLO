
from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.orders.models import Order, OrderItem, Invoice
from apps.products.models import Product, Category, Brand, Supplier, Customer
from apps.users.models import CustomUser


class OrderAPITestCase(TestCase):


    def setUp(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            username="staff",
            email="staff@test.com",
            password="password123",
            role=CustomUser.UserType.STAFF,
        )

        self.manager = CustomUser.objects.create_user(
            username="manager",
            email="manager@test.com",
            password="password123",
            role=CustomUser.UserType.MANAGER,
        )

        self.admin = CustomUser.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="password123",
            role=CustomUser.UserType.ADMIN,
        )


        self.category = Category.objects.create(
            name="Informatique",
        )

        self.brand = Brand.objects.create(
            name="Dell",
            description="Dell",
        )

        self.supplier = Supplier.objects.create(
            company_name="Tech Supplier",
            contact_name="Jean Supplier",
            email="supplier@test.com",
            phone="0102030405",
            address="Abidjan",
        )

        self.customer = Customer.objects.create(
            company_name="Client Company",
            contact_name="Client Contact",
            first_name="Jean",
            last_name="Client",
            email="customer@test.com",
            phone="0506070809",
            address="Abidjan",
        )

        self.product = Product.objects.create(
            name="Laptop Dell",
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            purchase_price=Decimal("500000.00"),
            selling_price=Decimal("650000.00"),
        )

 
        self.order = Order.objects.create(
            reference="CMD-001",
            order_type=Order.OrderType.SALE,
            status=Order.StatusChoice.PENDING,
            supplier=self.supplier,
            customer=self.customer,
            created_by=self.user,
        )


        self.list_url = "/orders/"

        self.detail_url = f"/orders/{self.order.id}/"


    def authenticate_as_user(self):

        self.client.force_authenticate(user=self.user)


    def test_get_order_list(self):

        self.authenticate_as_user()

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_get_order_detail(self):


        self.authenticate_as_user()

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["reference"],
            "CMD-001",
        )


    def test_create_order(self):

        self.authenticate_as_user()

        data = {
            "reference": "CMD-002",
            "order_type": Order.OrderType.SALE,
            "status": Order.StatusChoice.PENDING,
            "supplier": str(self.supplier.id),
            "customer": str(self.customer.id),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Order.objects.filter(reference="CMD-002").exists()
        )


    def test_create_order_with_duplicate_reference(self):

        self.authenticate_as_user()

        data = {
            "reference": "CMD-001",
            "order_type": Order.OrderType.SALE,
            "status": Order.StatusChoice.PENDING,
            "supplier": str(self.supplier.id),
            "customer": str(self.customer.id),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_create_order_with_invalid_order_type(self):

        self.authenticate_as_user()

        data = {
            "reference": "CMD-003",
            "order_type": "INVALID",
            "status": Order.StatusChoice.PENDING,
            "supplier": str(self.supplier.id),
            "customer": str(self.customer.id),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_create_order_with_invalid_status(self):

        self.authenticate_as_user()

        data = {
            "reference": "CMD-004",
            "order_type": Order.OrderType.SALE,
            "status": "INVALID",
            "supplier": str(self.supplier.id),
            "customer": str(self.customer.id),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_create_order_without_reference(self):

        self.authenticate_as_user()

        data = {
            "order_type": Order.OrderType.SALE,
            "status": Order.StatusChoice.PENDING,
            "supplier": str(self.supplier.id),
            "customer": str(self.customer.id),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_patch_order_status(self):

        self.authenticate_as_user()

        data = {
            "status": Order.StatusChoice.PROCESSING,
        }

        response = self.client.patch(
            self.detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.StatusChoice.PROCESSING,
        )


    def test_patch_order_to_completed(self):

        self.authenticate_as_user()

        data = {
            "status": Order.StatusChoice.COMPLETED,
        }

        response = self.client.patch(
            self.detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.StatusChoice.COMPLETED,
        )


    def test_update_order_with_put(self):

        self.authenticate_as_user()

        data = {
            "reference": "CMD-001-UPDATED",
            "order_type": Order.OrderType.SALE,
            "status": Order.StatusChoice.PROCESSING,
            "supplier": str(self.supplier.id),
            "customer": str(self.customer.id),
        }

        response = self.client.put(
            self.detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.reference,
            "CMD-001-UPDATED",
        )

        self.assertEqual(
            self.order.status,
            Order.StatusChoice.PROCESSING,
        )


    def test_delete_order(self):

        self.authenticate_as_user()

        order_id = self.order.id

        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Order.objects.filter(id=order_id).exists()
        )


    def test_get_nonexistent_order(self):

        self.authenticate_as_user()

        import uuid

        url = f"/orders/{uuid.uuid4()}/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_create_order_with_nonexistent_supplier(self):

        self.authenticate_as_user()

        import uuid

        data = {
            "reference": "CMD-005",
            "order_type": Order.OrderType.PURCHASE,
            "status": Order.StatusChoice.PENDING,
            "supplier": str(uuid.uuid4()),
            "customer": str(self.customer.id),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_create_order_with_nonexistent_customer(self):

        self.authenticate_as_user()

        import uuid

        data = {
            "reference": "CMD-006",
            "order_type": Order.OrderType.SALE,
            "status": Order.StatusChoice.PENDING,
            "supplier": str(self.supplier.id),
            "customer": str(uuid.uuid4()),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

