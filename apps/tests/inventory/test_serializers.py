from decimal import Decimal

from django.test import TestCase

from apps.inventory.models import (
    WareHouse,
    StockItem,
    StockMovement,
)

from apps.inventory.serializers import (
    WareHouseSerializer,
    StockItemSerializer,
    DetailStockItemSerializer,
    StockMovementSerializer,
    DetailStockMovementSerializer,
)

from apps.products.models import (
    Category,
    Brand,
    Supplier,
    Product,
)

from apps.users.models import CustomUser
from apps.users.serializers import UserProfileSerializer



class InventorySerializerTest(TestCase):

    def setUp(self):

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

        self.user = CustomUser.objects.create_user(
            username="jean",
            password="password123",
            role=CustomUser.UserType.STAFF
        )

        self.stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=10
        )
        
        
    
    def test_warehouse_serializer_valid_data(self):

        data = {
            "name": "Nouvel entrepôt",
            "address": "Abidjan"
        }

        serializer = WareHouseSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        
        
    def test_warehouse_name_is_required(self):

        data = {
            "address": "Abidjan"
        }

        serializer = WareHouseSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "name",
            serializer.errors
        )
        
        
    def test_warehouse_address_is_optional(self):

        data = {
            "name": "Entrepôt sans adresse"
        }

        serializer = WareHouseSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        
        
    def test_warehouse_id_is_read_only(self):

        data = {
            "id": "12345678-1234-1234-1234-123456789012",
            "name": "Entrepôt",
            "address": "Abidjan"
        }

        serializer = WareHouseSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "id",
            serializer.validated_data
        )
        
        
        
    def test_warehouse_serializer_create(self):

        data = {
            "name": "Entrepôt secondaire",
            "address": "Yopougon"
        }

        serializer = WareHouseSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        warehouse = serializer.save()

        self.assertIsNotNone(warehouse.pk)

        self.assertEqual(
            warehouse.name,
            "Entrepôt secondaire"
        )

        self.assertEqual(
            warehouse.address,
            "Yopougon"
        )
        
        
    def test_stock_item_serializer_valid_data(self):

        data = {
            "warehouse": str(self.warehouse.pk),
            "product": str(self.product.pk),
            "quantity": 20
        }

        serializer = StockItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        
    def test_stock_item_warehouse_is_required(self):

        data = {
            "product": str(self.product.pk),
            "quantity": 10
        }

        serializer = StockItemSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "warehouse",
            serializer.errors
        )
        
        
        
    def test_stock_item_product_is_required(self):

        data = {
            "warehouse": str(self.warehouse.pk),
            "quantity": 10
        }

        serializer = StockItemSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "product",
            serializer.errors
        )
        
        

    def test_stock_item_quantity_defaults_to_zero(self):

        data = {
            "warehouse": str(self.warehouse.pk),
            "product": str(self.product.pk)
        }

        serializer = StockItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        stock_item = serializer.save()

        self.assertEqual(
            stock_item.quantity,
            0
        )
        
        
        
    def test_stock_item_negative_quantity_is_invalid(self):

        data = {
            "warehouse": str(self.warehouse.pk),
            "product": str(self.product.pk),
            "quantity": -10
        }

        serializer = StockItemSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "quantity",
            serializer.errors
        )
        
        
        
    def test_stock_item_zero_quantity_is_valid(self):

        data = {
            "warehouse": str(self.warehouse.pk),
            "product": str(self.product.pk),
            "quantity": 0
        }

        serializer = StockItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        
    def test_stock_item_invalid_warehouse(self):

        import uuid

        data = {
            "warehouse": str(uuid.uuid4()),
            "product": str(self.product.pk),
            "quantity": 10
        }

        serializer = StockItemSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "warehouse",
            serializer.errors
        )
        
        
    def test_stock_item_invalid_product(self):

        import uuid

        data = {
            "warehouse": str(self.warehouse.pk),
            "product": str(uuid.uuid4()),
            "quantity": 10
        }

        serializer = StockItemSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "product",
            serializer.errors
        )
        
        
    def test_stock_item_id_is_read_only(self):

        data = {
            "id": str(self.stock_item.pk),
            "warehouse": str(self.warehouse.pk),
            "product": str(self.product.pk),
            "quantity": 20
        }

        serializer = StockItemSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "id",
            serializer.validated_data
        )
        
        
        
    def test_detail_stock_item_serializer(self):

        serializer = DetailStockItemSerializer(
            self.stock_item
        )

        data = serializer.data

        self.assertEqual(
            data["id"],
            str(self.stock_item.id)
        )

        self.assertEqual(
            data["warehouse"],
            self.warehouse.name
        )

        self.assertEqual(
            data["product"]["name"],
            self.product.name
        )

        self.assertEqual(
            data["quantity"],
            10
        )
        
        
        
    def test_stock_movement_serializer_valid_data(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5,
            "reason": "Réapprovisionnement"
        }

        serializer = StockMovementSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        
    def test_stock_movement_item_is_required(self):

        data = {
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5,
            "reason": "Réapprovisionnement"
        }

        serializer = StockMovementSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "item",
            serializer.errors
        )
        
        
    def test_stock_movement_type_is_required(self):

        data = {
            "item": str(self.stock_item.pk),
            "quantity": 5
        }

        serializer = StockMovementSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "movement_type",
            serializer.errors
        )
        
        
    def test_stock_movement_quantity_is_required(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN
        }

        serializer = StockMovementSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "quantity",
            serializer.errors
        )
        
        
    def test_stock_movement_reason_is_optional(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5
        }

        serializer = StockMovementSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        

    def test_invalid_movement_type(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": "INVALID",
            "quantity": 5
        }

        serializer = StockMovementSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "movement_type",
            serializer.errors
        )
        
        
    def test_negative_movement_quantity_should_be_invalid(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": -5
        }

        serializer = StockMovementSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )
        
        
        
    def test_zero_movement_quantity(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 0
        }

        serializer = StockMovementSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
        
        

    def test_stock_movement_user_is_read_only(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5,
            "user": str(self.user.pk)
        }

        serializer = StockMovementSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "user",
            serializer.validated_data
        )
        
        
    def test_stock_movement_created_at_is_read_only(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5,
            "created_at": "2020-01-01T00:00:00Z"
        }

        serializer = StockMovementSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "created_at",
            serializer.validated_data
        )
        
        
    def test_stock_movement_invalid_item(self):

        import uuid

        data = {
            "item": str(uuid.uuid4()),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5
        }

        serializer = StockMovementSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "item",
            serializer.errors
        )
        
        
    def test_detail_stock_movement_serializer(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=5,
            user=self.user,
            reason="Réapprovisionnement"
        )

        serializer = DetailStockMovementSerializer(
            movement
        )

        data = serializer.data

        self.assertEqual(
            data["id"],
            str(movement.id)
        )

        self.assertEqual(
            data["item"],
            str(self.stock_item)
        )

        self.assertEqual(
            data["quantity"],
            5
        )

        self.assertEqual(
            data["reason"],
            "Réapprovisionnement"
        )
        
        
        
    def test_create_stock_movement_through_serializer(self):

        data = {
            "item": str(self.stock_item.pk),
            "movement_type": StockMovement.MovementType.IN,
            "quantity": 5,
            "reason": "Réapprovisionnement"
        }

        serializer = StockMovementSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        movement = serializer.save(
            user=self.user
        )

        self.assertIsNotNone(
            movement.pk
        )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            15
        )
        
        
    def test_valid_phone_is_returned(self):

        serializer = UserProfileSerializer(
            data={
                "phone": "0700000000"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["phone"],
            "0700000000"
        )