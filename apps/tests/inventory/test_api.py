from decimal import Decimal
import uuid

from django.urls import reverse
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


class InventoryAPITest(APITestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="password123",
            role=CustomUser.UserType.STAFF
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
            address="Abidjan Cocody"
        )

        self.stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=10
        )
        
        
def test_warehouse_get_list(self):

    response = self.client.get(
        reverse("warehouse-list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        len(response.data),
        1
    )
    
    
def test_warehouse_get_list_multiple(self):

    WareHouse.objects.create(
        name="Entrepôt secondaire",
        address="Yopougon"
    )

    WareHouse.objects.create(
        name="Entrepôt 3",
        address="Marcory"
    )

    response = self.client.get(
        reverse("warehouse-list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        len(response.data),
        3
    )
    
    
def test_warehouse_get_detail(self):

    response = self.client.get(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        response.data["name"],
        "Entrepôt principal"
    )

    self.assertEqual(
        response.data["address"],
        "Abidjan Cocody"
    )
    
    
    
def test_warehouse_get_detail_not_found(self):

    response = self.client.get(
        reverse(
            "warehouse-detail",
            kwargs={"pk": uuid.uuid4()}
        )
    )

    self.assertEqual(
        response.status_code,
        404
    )
    
    
def test_warehouse_post(self):

    data = {
        "name": "Nouvel entrepôt",
        "address": "Abidjan Plateau"
    }

    response = self.client.post(
        reverse("warehouse-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )

    self.assertTrue(
        WareHouse.objects.filter(
            name="Nouvel entrepôt"
        ).exists()
    )
    
    
def test_warehouse_post_without_name(self):

    data = {
        "address": "Abidjan"
    }

    response = self.client.post(
        reverse("warehouse-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        400
    )

    self.assertIn(
        "name",
        response.data
    )
    
    
def test_warehouse_post_without_address(self):

    data = {
        "name": "Entrepôt sans adresse"
    }

    response = self.client.post(
        reverse("warehouse-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )
    
    
def test_warehouse_put(self):

    data = {
        "name": "Entrepôt modifié",
        "address": "Boulevard Latrille"
    }

    response = self.client.put(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        ),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.warehouse.refresh_from_db()

    self.assertEqual(
        self.warehouse.name,
        "Entrepôt modifié"
    )

    self.assertEqual(
        self.warehouse.address,
        "Boulevard Latrille"
    )
    
    
def test_warehouse_put_without_name(self):

    data = {
        "address": "Abidjan"
    }

    response = self.client.put(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        ),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        400
    )
    
    
def test_warehouse_patch(self):

    data = {
        "name": "Nom modifié uniquement"
    }

    response = self.client.patch(
        reverse(
            "warehouse-detail",
            kwargs={"pk": self.warehouse.pk}
        ),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.warehouse.refresh_from_db()

    self.assertEqual(
        self.warehouse.name,
        "Nom modifié uniquement"
    )

    self.assertEqual(
        self.warehouse.address,
        "Abidjan Cocody"
    )
    
    
def test_warehouse_delete(self):

    warehouse_id = self.warehouse.pk

    response = self.client.delete(
        reverse(
            "warehouse-detail",
            kwargs={"pk": warehouse_id}
        )
    )

    self.assertEqual(
        response.status_code,
        204
    )

    self.assertFalse(
        WareHouse.objects.filter(
            pk=warehouse_id
        ).exists()
    )
    
    

def test_stock_item_get_list(self):

    response = self.client.get(
        reverse("stock-item-list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        len(response.data),
        1
    )
    
    
def test_stock_item_get_detail(self):

    response = self.client.get(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        response.data["quantity"],
        10
    )

    self.assertEqual(
        response.data["warehouse"],
        self.warehouse.name
    )

    self.assertEqual(
        response.data["product"]["name"],
        self.product.name
    )
    
    
def test_stock_item_get_detail_not_found(self):

    response = self.client.get(
        reverse(
            "stock-item-detail",
            kwargs={"pk": uuid.uuid4()}
        )
    )

    self.assertEqual(
        response.status_code,
        404
    )
    
    
    
def test_stock_item_post(self):

    data = {
        "warehouse": str(self.warehouse.pk),
        "product": str(self.product.pk),
        "quantity": 20
    }

    response = self.client.post(
        reverse("stock-item-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )

    self.assertTrue(
        StockItem.objects.filter(
            warehouse=self.warehouse,
            product=self.product,
            quantity=20
        ).exists()
    )
    
    
def test_stock_item_post_without_warehouse(self):

    data = {
        "product": str(self.product.pk),
        "quantity": 10
    }

    response = self.client.post(
        reverse("stock-item-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        400
    )

    self.assertIn(
        "warehouse",
        response.data
    )
    
    
def test_stock_item_post_without_product(self):

    data = {
        "warehouse": str(self.warehouse.pk),
        "quantity": 10
    }

    response = self.client.post(
        reverse("stock-item-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        400
    )

    self.assertIn(
        "product",
        response.data
    )
    
    
def test_stock_item_post_negative_quantity(self):

    data = {
        "warehouse": str(self.warehouse.pk),
        "product": str(self.product.pk),
        "quantity": -5
    }

    response = self.client.post(
        reverse("stock-item-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        400
    )

    self.assertIn(
        "quantity",
        response.data
    )
    
    
def test_stock_item_post_invalid_warehouse(self):

    data = {
        "warehouse": str(uuid.uuid4()),
        "product": str(self.product.pk),
        "quantity": 10
    }

    response = self.client.post(
        reverse("stock-item-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        400
    )

    self.assertIn(
        "warehouse",
        response.data
    )
    
    
def test_stock_item_put(self):

    data = {
        "warehouse": str(self.warehouse.pk),
        "product": str(self.product.pk),
        "quantity": 50
    }

    response = self.client.put(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        ),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        50
    )
    
    
def test_stock_item_patch_quantity(self):

    response = self.client.patch(
        reverse(
            "stock-item-detail",
            kwargs={"pk": self.stock_item.pk}
        ),
        {
            "quantity": 30
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        30
    )
    
    
def test_stock_item_delete(self):

    stock_item_id = self.stock_item.pk

    response = self.client.delete(
        reverse(
            "stock-item-detail",
            kwargs={"pk": stock_item_id}
        )
    )

    self.assertEqual(
        response.status_code,
        204
    )

    self.assertFalse(
        StockItem.objects.filter(
            pk=stock_item_id
        ).exists()
    )
    
    
def test_stock_movement_post_in(self):

    self.client.force_authenticate(
        user=self.user
    )

    data = {
        "item": str(self.stock_item.pk),
        "movement_type": StockMovement.MovementType.IN,
        "quantity": 5,
        "reason": "Réapprovisionnement"
    }

    response = self.client.post(
        reverse("stock-movement-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )

    movement = StockMovement.objects.get(
        pk=response.data["id"]
    )

    self.assertEqual(
        movement.user,
        self.user
    )

    self.assertEqual(
        movement.quantity,
        5
    )
    
    
def test_stock_movement_post_in_updates_stock(self):

    self.client.force_authenticate(
        user=self.user
    )

    data = {
        "item": str(self.stock_item.pk),
        "movement_type": StockMovement.MovementType.IN,
        "quantity": 5
    }

    response = self.client.post(
        reverse("stock-movement-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        15
    )
    
    
def test_stock_movement_post_out(self):

    self.client.force_authenticate(
        user=self.user
    )

    data = {
        "item": str(self.stock_item.pk),
        "movement_type": StockMovement.MovementType.OUT,
        "quantity": 4,
        "reason": "Vente"
    }

    response = self.client.post(
        reverse("stock-movement-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        6
    )
    
    
def test_stock_movement_out_insufficient_stock(self):

    self.client.force_authenticate(
        user=self.user
    )

    data = {
        "item": str(self.stock_item.pk),
        "movement_type": StockMovement.MovementType.OUT,
        "quantity": 100
    }

    response = self.client.post(
        reverse("stock-movement-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        500
    )
    
    
def test_stock_movement_get_list(self):

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.user
    )

    response = self.client.get(
        reverse("stock-movement-list")
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        len(response.data),
        1
    )
    
    
def test_stock_movement_get_detail(self):

    movement = StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.user,
        reason="Test"
    )

    response = self.client.get(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": movement.pk}
        )
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertEqual(
        response.data["quantity"],
        5
    )

    self.assertEqual(
        response.data["reason"],
        "Test"
    )
    
    
def test_stock_movement_get_detail_not_found(self):

    response = self.client.get(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": uuid.uuid4()}
        )
    )

    self.assertEqual(
        response.status_code,
        404
    )
    
    
def test_stock_movement_patch(self):

    movement = StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.user
    )

    self.stock_item.refresh_from_db()

    initial_quantity = self.stock_item.quantity

    response = self.client.patch(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": movement.pk}
        ),
        {
            "reason": "Nouvelle raison"
        },
        format="json"
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        initial_quantity
    )
    
    
def test_stock_movement_delete(self):

    movement = StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.user
    )

    movement_id = movement.pk

    response = self.client.delete(
        reverse(
            "stock-movement-detail",
            kwargs={"pk": movement_id}
        )
    )

    self.assertEqual(
        response.status_code,
        204
    )

    self.assertFalse(
        StockMovement.objects.filter(
            pk=movement_id
        ).exists()
    )
    
    
def test_stock_movement_user_cannot_be_defined_by_client(self):

    another_user = CustomUser.objects.create_user(
        username="another",
        password="password123"
    )

    self.client.force_authenticate(
        user=self.user
    )

    data = {
        "item": str(self.stock_item.pk),
        "movement_type": StockMovement.MovementType.IN,
        "quantity": 5,
        "user": str(another_user.pk)
    }

    response = self.client.post(
        reverse("stock-movement-list"),
        data,
        format="json"
    )

    self.assertEqual(
        response.status_code,
        201
    )

    movement = StockMovement.objects.get(
        pk=response.data["id"]
    )

    self.assertEqual(
        movement.user,
        self.user
    )
    
    
def test_anonymous_cannot_create_stock_movement(self):

    data = {
        "item": str(self.stock_item.pk),
        "movement_type": StockMovement.MovementType.IN,
        "quantity": 5
    }

    response = self.client.post(
        reverse("stock-movement-list"),
        data,
        format="json"
    )

    self.assertIn(
        response.status_code,
        [401, 403]
    )
    
    
