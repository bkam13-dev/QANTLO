from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.orders.models import Order
from apps.products.models import Product, Category, Brand, Supplier, Customer
from apps.users.models import CustomUser


class OrderPermissionsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.staff = CustomUser.objects.create_user(
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
            contact_name="Supplier Contact",
            email="supplier@test.com",
            phone="0102030405",
            address="Abidjan",
        )

        self.customer = Customer.objects.create(
            company_name="Customer Company",
            contact_name="Customer Contact",
            first_name="Jean",
            last_name="Customer",
            email="customer@test.com",
            phone="0506070809",
            address="Abidjan",
        )

        self.product = Product.objects.create(
            name="Dell Laptop",
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            purchase_price=Decimal("500000.00"),
            selling_price=Decimal("650000.00"),
        )

        self.staff_order = Order.objects.create(
            reference="STAFF-ORDER-001",
            order_type=Order.OrderType.SALE,
            status=Order.StatusChoice.PENDING,
            supplier=self.supplier,
            customer=self.customer,
            created_by=self.staff,
        )

        self.manager_order = Order.objects.create(
            reference="MANAGER-ORDER-001",
            order_type=Order.OrderType.SALE,
            status=Order.StatusChoice.PENDING,
            supplier=self.supplier,
            customer=self.customer,
            created_by=self.manager,
        )

        self.list_url = "/orders/"

        self.staff_order_url = (
            f"/orders/{self.staff_order.id}/"
        )

        self.manager_order_url = (
            f"/orders/{self.manager_order.id}/"
        )


    def authenticate(self, user):

        self.client.force_authenticate(user=user)


    def test_staff_can_list_orders(self):

        self.authenticate(self.staff)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_manager_can_list_orders(self):

        self.authenticate(self.manager)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_admin_can_list_orders(self):

        self.authenticate(self.admin)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_staff_can_create_order(self):

        self.authenticate(self.staff)

        data = {
            "reference": "STAFF-NEW-ORDER",
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


    def test_manager_can_create_order(self):

        self.authenticate(self.manager)

        data = {
            "reference": "MANAGER-NEW-ORDER",
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


    def test_admin_can_create_order(self):

        self.authenticate(self.admin)

        data = {
            "reference": "ADMIN-NEW-ORDER",
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


    def test_admin_can_update_order(self):

        self.authenticate(self.admin)

        data = {
            "status": Order.StatusChoice.PROCESSING,
        }

        response = self.client.patch(
            self.staff_order_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.staff_order.refresh_from_db()

        self.assertEqual(
            self.staff_order.status,
            Order.StatusChoice.PROCESSING,
        )


    def test_manager_can_update_order(self):

        self.authenticate(self.manager)

        data = {
            "status": Order.StatusChoice.PROCESSING,
        }

        response = self.client.patch(
            self.staff_order_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_staff_cannot_update_order(self):

        self.authenticate(self.staff)

        data = {
            "status": Order.StatusChoice.PROCESSING,
        }

        response = self.client.patch(
            self.staff_order_url,
            data,
            format="json",
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            ],
        )


    def test_admin_can_delete_order(self):

        self.authenticate(self.admin)

        response = self.client.delete(
            self.staff_order_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Order.objects.filter(
                id=self.staff_order.id
            ).exists()
        )


    def test_staff_cannot_delete_order(self):

        self.authenticate(self.staff)

        response = self.client.delete(
            self.staff_order_url
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            ],
        )

        self.assertTrue(
            Order.objects.filter(
                id=self.staff_order.id
            ).exists()
        )


    def test_manager_cannot_delete_order(self):

        self.authenticate(self.manager)

        response = self.client.delete(
            self.manager_order_url
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            ],
        )

        self.assertTrue(
            Order.objects.filter(
                id=self.manager_order.id
            ).exists()
        )


    def test_anonymous_user_cannot_access_orders(self):

        self.client.force_authenticate(user=None)

        response = self.client.get(
            self.list_url
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )


    def test_anonymous_user_cannot_create_order(self):

        self.client.force_authenticate(user=None)

        data = {
            "reference": "ANONYMOUS-ORDER",
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

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

        self.assertFalse(
            Order.objects.filter(
                reference="ANONYMOUS-ORDER"
            ).exists()
        )