import uuid
from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import (
    Product,
    Category,
    Brand,
    Supplier,
)
from apps.users.models import CustomUser



class ProductPermissionTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Informatique",
            slug="informatique"
        )

        self.brand = Brand.objects.create(
            name="HP",
            description="Marque informatique"
        )

        self.supplier = Supplier.objects.create(
            company_name="Tech Distribution",
            contact_name="Jean",
            email="tech@test.com",
            phone="0700000000",
            address="Abidjan"
        )

        self.product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP EliteBook",
            barcode="123456789",
            purchase_price=Decimal("300000.00"),
            selling_price=Decimal("400000.00"),
            min_stock_level=5,
        )

        self.staff = CustomUser.objects.create_user(
            username="staff",
            password="password123",
            role=CustomUser.UserType.STAFF
        )

        self.manager = CustomUser.objects.create_user(
            username="manager",
            password="password123",
            role=CustomUser.UserType.MANAGER
        )

        self.admin = CustomUser.objects.create_user(
            username="admin",
            password="password123",
            role=CustomUser.UserType.ADMIN
        )

    def list_url(self):
        return reverse("product-list")

    def detail_url(self):
        return reverse(
            "product-detail",
            kwargs={"pk": self.product.id}
        )
        
        
def test_anonymous_cannot_create_product(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "999999",
        "name": "Produit test",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertIn(
        response.status_code,
        [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ]
    )
    
    
def test_staff_can_list_products(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.get(
        self.list_url()
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
def test_staff_can_retrieve_product(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.get(
        self.detail_url()
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
def test_staff_cannot_delete_product(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.delete(
        self.detail_url()
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    
    
def test_manager_can_create_product(self):

    self.client.force_authenticate(
        user=self.manager
    )

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "777777",
        "name": "Nouveau produit",
        "description": "Produit créé par manager",
        "purchase_price": "200000.00",
        "selling_price": "300000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )
    
    
    
def test_manager_can_update_product(self):

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.patch(
        self.detail_url(),
        {
            "selling_price": "450000.00"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
def test_admin_can_list_products(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.get(
        self.list_url()
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
def test_admin_can_create_product(self):

    self.client.force_authenticate(
        user=self.admin
    )

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "888888",
        "name": "Produit admin",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )
    
    
def test_admin_can_delete_product(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.delete(
        self.detail_url()
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_204_NO_CONTENT
    )
    
    
def test_create_product_with_empty_data(self):

    response = self.client.post(
        self.list_url(),
        {},
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    self.assertIn("name", response.data)
    self.assertIn("category", response.data)
    self.assertIn("brand", response.data)
    self.assertIn("supplier", response.data)
    
    
def test_retrieve_nonexistent_product(self):

    fake_id = uuid.uuid4()

    url = reverse(
        "product-detail",
        kwargs={"pk": fake_id}
    )

    response = self.client.get(url)

    self.assertEqual(
        response.status_code,
        status.HTTP_404_NOT_FOUND
    )
    
    
    
def test_create_product_with_nonexistent_category(self):

    data = {
        "category": str(uuid.uuid4()),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "111111",
        "name": "Produit test",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )

    self.assertIn(
        "category",
        response.data
    )
    
    
def test_create_product_with_nonexistent_brand(self):

    data = {
        "category": str(self.category.id),
        "brand": str(uuid.uuid4()),
        "supplier": str(self.supplier.id),
        "barcode": "222222",
        "name": "Produit test",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )

    self.assertIn(
        "brand",
        response.data
    )
    
    

def test_create_product_with_nonexistent_supplier(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(uuid.uuid4()),
        "barcode": "333333",
        "name": "Produit test",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )

    self.assertIn(
        "supplier",
        response.data
    )
    
    
def test_product_with_negative_purchase_price(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "444444",
        "name": "Produit négatif",
        "description": "Test",
        "purchase_price": "-1000.00",
        "selling_price": "2000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    

def test_selling_price_cannot_be_lower_than_purchase_price(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "555555",
        "name": "Produit test",
        "description": "Test",
        "purchase_price": "300000.00",
        "selling_price": "200000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    
def test_product_name_too_long(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "666666",
        "name": "A" * 256,
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    
def test_duplicate_barcode(self):

    Product.objects.create(
        category=self.category,
        brand=self.brand,
        supplier=self.supplier,
        name="Premier produit",
        barcode="777777",
        purchase_price=Decimal("100000.00"),
        selling_price=Decimal("150000.00"),
        min_stock_level=5,
    )

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "777777",
        "name": "Deuxième produit",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    
def test_duplicate_sku(self):

    product = self.product

    other = Product(
        category=self.category,
        brand=self.brand,
        supplier=self.supplier,
        sku=product.sku,
        name="Autre produit",
        barcode="888888",
        purchase_price=Decimal("100000.00"),
        selling_price=Decimal("150000.00"),
        min_stock_level=5,
    )

    with self.assertRaises(Exception):
        other.save()
        
        
def test_negative_min_stock_level(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "999999",
        "name": "Produit test",
        "description": "Test",
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": -1,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    
    
def test_patch_with_empty_data(self):

    response = self.client.patch(
        self.detail_url(),
        {},
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
    
def test_patch_with_unknown_field(self):

    response = self.client.patch(
        self.detail_url(),
        {
            "unknown_field": "test"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST
    )
    
    
    
def test_product_description_too_long(self):

    data = {
        "category": str(self.category.id),
        "brand": str(self.brand.id),
        "supplier": str(self.supplier.id),
        "barcode": "123123",
        "name": "Produit test",
        "description": "A" * 100000,
        "purchase_price": "100000.00",
        "selling_price": "150000.00",
        "min_stock_level": 5,
    }

    response = self.client.post(
        self.list_url(),
        data,
        format="json"
    )

    # TextField n'a pas de max_length dans ton modèle.
    # Donc cette donnée peut être acceptée.
    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )