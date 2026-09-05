from decimal import Decimal
import uuid

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.inventory.models import (
    WareHouse,
    StockItem,
    StockMovement,
)

from apps.products.models import (
    Category,
    Brand,
    Supplier,
    Product,
)

from apps.users.models import CustomUser




class InventoryPermissionTest(APITestCase):

    def setUp(self):

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

        self.category = Category.objects.create(
            name="Informatique",
            slug="informatique"
        )

        self.brand = Brand.objects.create(
            name="HP",
            description="Marque HP"
        )

        self.supplier = Supplier.objects.create(
            company_name="Tech Supplier",
            contact_name="Jean",
            email="supplier@test.com",
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
            min_stock_level=5
        )

        self.warehouse = WareHouse.objects.create(
            name="Entrepôt principal",
            address="Abidjan"
        )

        self.stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=10
        )
        
        
    
def test_anonymous_cannot_list_warehouses(self):

    response = self.client.get(
        reverse("warehouse-list")
    )

    self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    )
    
    

def test_anonymous_cannot_list_stock_items(self):

    response = self.client.get(
        reverse("stock-item-list")
    )

    self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    )
    
    
def test_anonymous_cannot_list_stock_movements(self):

    response = self.client.get(
        reverse("stock-movement-list")
    )

    self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    )
    
    
def test_anonymous_cannot_create_warehouse(self):

    response = self.client.post(
        reverse("warehouse-list"),
        {
            "name": "Entrepôt pirate",
            "address": "Abidjan"
        },
        format="json"
    )

    self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    )
    
    
def test_anonymous_cannot_create_stock_item(self):

    response = self.client.post(
        reverse("stock-item-list"),
        {
            "warehouse": str(self.warehouse.pk),
            "product": str(self.product.pk),
            "quantity": 10
        },
        format="json"
    )

    self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    )
    
    

def test_staff_can_list_warehouses(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.get(
        reverse("warehouse-list")
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    

def test_staff_can_list_stock_items(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.get(
        reverse("stock-item-list")
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
def test_staff_cannot_create_warehouse(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.post(
        reverse("warehouse-list"),
        {
            "name": "Nouvel entrepôt",
            "address": "Abidjan"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    
def test_staff_cannot_update_warehouse(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.patch(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        ),
        {
            "name": "Entrepôt modifié"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    
    
def test_staff_cannot_delete_warehouse(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.delete(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    

def test_manager_can_list_warehouses(self):

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.get(
        reverse("warehouse-list")
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    

def test_manager_can_create_warehouse(self):

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.post(
        reverse("warehouse-list"),
        {
            "name": "Entrepôt Manager",
            "address": "Cocody"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )
    
    
def test_manager_can_update_warehouse(self):

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.patch(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        ),
        {
            "name": "Entrepôt principal modifié"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    

def test_admin_can_create_warehouse(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.post(
        reverse("warehouse-list"),
        {
            "name": "Entrepôt Admin",
            "address": "Plateau"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )
    
    
def test_admin_can_update_warehouse(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.patch(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        ),
        {
            "name": "Entrepôt administré"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
    
def test_admin_can_delete_warehouse(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.delete(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_204_NO_CONTENT
    )
    
    
    
def test_staff_can_read_stock(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.get(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
    
def test_staff_cannot_update_stock(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.patch(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        ),
        {
            "quantity": 100
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    

def test_manager_can_update_stock_item(self):

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.patch(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        ),
        {
            "quantity": 50
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
    
def test_admin_can_update_stock_item(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.patch(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        ),
        {
            "quantity": 100
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
    
def test_staff_can_read_stock_movement(self):

    movement = StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.manager
    )

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.get(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": movement.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )
    
    
    
def test_staff_cannot_create_stock_movement(self):

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.post(
        reverse("stock-movement-list"),
        {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 10
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    
    
def test_manager_can_create_stock_movement(self):

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.post(
        reverse("stock-movement-list"),
        {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 10,
            "reason": "Réapprovisionnement"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )
    
    
    
def test_admin_can_create_stock_movement(self):

    self.client.force_authenticate(
        user=self.admin
    )

    response = self.client.post(
        reverse("stock-movement-list"),
        {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 10
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )
    
    
    
def test_staff_cannot_delete_stock_movement(self):

    movement = StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.manager
    )

    self.client.force_authenticate(
        user=self.staff
    )

    response = self.client.delete(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": movement.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    
    
def test_manager_cannot_delete_stock_movement(self):

    movement = StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.manager
    )

    self.client.force_authenticate(
        user=self.manager
    )

    response = self.client.delete(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": movement.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_403_FORBIDDEN
    )
    
    
    
