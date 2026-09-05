import uuid

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.inventory.models import (
    WareHouse,
    StockItem,
    StockMovement,
)

from apps.products.models import (
    Product,
    Category,
    Brand,
    Supplier,
)

from apps.users.models import CustomUser



class InventoryModelTestCase(TestCase):

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
            contact_name="Jean Paul",
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
            purchase_price=300000,
            selling_price=400000,
            min_stock_level=5,
        )

        self.warehouse = WareHouse.objects.create(
            name="Entrepôt principal",
            address="Abidjan"
        )

        self.user = CustomUser.objects.create_user(
            username="staff",
            password="password123",
            role=CustomUser.UserType.STAFF
        )

        self.stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=10
        )
        
        
            
    def test_warehouse_creation(self):

        warehouse = WareHouse.objects.create(
            name="Deuxième entrepôt",
            address="Cocody"
        )

        self.assertIsNotNone(warehouse)

        self.assertEqual(
            warehouse.name,
            "Deuxième entrepôt"
        )

        self.assertEqual(
            warehouse.address,
            "Cocody"
        )
        
        
    def test_warehouse_id_is_uuid(self):

        warehouse = WareHouse.objects.create(
            name="Entrepôt test"
        )

        self.assertIsInstance(
            warehouse.id,
            uuid.UUID
        )
        
        

    def test_warehouse_id_is_generated_automatically(self):

        warehouse = WareHouse.objects.create(
            name="Entrepôt test"
        )

        self.assertIsNotNone(
            warehouse.id
        )
        
        
        
    def test_warehouse_address_can_be_empty(self):

        warehouse = WareHouse.objects.create(
            name="Entrepôt sans adresse"
        )

        self.assertEqual(
            warehouse.address,
            ""
        )
        
        

    def test_warehouse_name_is_required(self):

        warehouse = WareHouse(
            address="Abidjan"
        )

        with self.assertRaises(Exception):
            warehouse.full_clean()
            
            
            
    def test_warehouse_name_is_required(self):

        warehouse = WareHouse(
            address="Abidjan"
        )

        with self.assertRaises(ValidationError):
            warehouse.full_clean()
            
            
            
    def test_warehouse_str(self):

        self.assertEqual(
            str(self.warehouse),
            "Entrepôt principal"
        )
        
        

    def test_stock_item_creation(self):

        self.assertIsNotNone(
            self.stock_item
        )

        self.assertEqual(
            self.stock_item.quantity,
            10
        )
        
        
        
    def test_stock_item_quantity_default(self):

        stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            product=self.product
        )

        self.assertEqual(
            stock_item.quantity,
            0
        )
        
        

    def test_stock_item_quantity_can_be_positive(self):

        stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=50
        )

        self.assertEqual(
            stock_item.quantity,
            50
        )
        
        

    def test_stock_item_quantity_cannot_be_negative(self):

        stock_item = StockItem(
            warehouse=self.warehouse,
            product=self.product,
            quantity=-1
        )

        with self.assertRaises(ValidationError):
            stock_item.full_clean()
            
            

    def test_stock_item_warehouse_is_required(self):

        stock_item = StockItem(
            product=self.product,
            quantity=10
        )

        with self.assertRaises(ValidationError):
            stock_item.full_clean()
            
            
            
    def test_stock_item_product_is_required(self):

        stock_item = StockItem(
            warehouse=self.warehouse,
            quantity=10
        )

        with self.assertRaises(ValidationError):
            stock_item.full_clean()
            
            
            
    def test_stock_item_belongs_to_warehouse(self):

        self.assertEqual(
            self.stock_item.warehouse,
            self.warehouse
        )
        
        

    def test_warehouse_related_stock_items(self):

        self.assertIn(
            self.stock_item,
            self.warehouse.stock_items.all()
        )
        
        
        
    def test_stock_item_belongs_to_product(self):

        self.assertEqual(
            self.stock_item.product,
            self.product
        )
        
        

    def test_product_related_stock_item(self):

        self.assertIn(
            self.stock_item,
            self.product.item.all()
        )
        
        
        
    def test_stock_item_str(self):

        self.assertEqual(
            str(self.stock_item),
            "HP EliteBook : 10"
        )
        
        
    def test_stock_movement_creation(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=5,
            user=self.user
        )

        self.assertIsNotNone(movement)
        
        
    def test_stock_movement_increases_stock(self):

        self.assertEqual(
            self.stock_item.quantity,
            10
        )

        StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=5,
            user=self.user
        )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            15
        )
        
        

    def test_stock_movement_out_decreases_stock(self):

        StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.OUT,
            quantity=4,
            user=self.user
        )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            6
        )
        
        

    def test_stock_movement_out_with_insufficient_stock(self):

        with self.assertRaises(ValueError):

            StockMovement.objects.create(
                item=self.stock_item,
                movement_type=StockMovement.MovementType.OUT,
                quantity=20,
                user=self.user
            )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            10
        )
        
        
        
    def test_stock_movement_zero_quantity(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=0,
            user=self.user
        )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            10
        )
        
        
        
    def test_stock_movement_quantity_cannot_be_negative(self):

        movement = StockMovement(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=-5,
            user=self.user
        )

        with self.assertRaises(ValidationError):
            movement.full_clean()
            
            
            
    def test_stock_movement_default_type(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            quantity=5,
            user=self.user
        )

        self.assertEqual(
            movement.movement_type,
            StockMovement.MovementType.IN
        )
        
        
    def test_invalid_movement_type(self):

        movement = StockMovement(
            item=self.stock_item,
            movement_type="INVALID",
            quantity=5,
            user=self.user
        )

        with self.assertRaises(ValidationError):
            movement.full_clean()
            
            
            
    def test_stock_movement_user_is_required(self):

        movement = StockMovement(
            item=self.stock_item,
            quantity=5
        )

        with self.assertRaises(ValidationError):
            movement.full_clean()
            
            
    def test_stock_movement_item_is_required(self):

        movement = StockMovement(
            quantity=5,
            user=self.user
        )

        with self.assertRaises(ValidationError):
            movement.full_clean()
            
            
    def test_stock_movement_reason_is_optional(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=5,
            user=self.user
        )

        self.assertEqual(
            movement.reason,
            ""
        )
        
        

    def test_stock_movement_created_at_is_generated(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            quantity=5,
            user=self.user
        )

        self.assertIsNotNone(
            movement.created_at
        )
        
        
    def test_stock_item_has_stock_movements(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            quantity=5,
            user=self.user
        )

        self.assertIn(
            movement,
            self.stock_item.stock_movements.all()
        )
        
        
    def test_user_has_movements(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            quantity=5,
            user=self.user
        )

        self.assertIn(
            movement,
            self.user.movements.all()
        )
        
        
    def test_updating_stock_movement_does_not_change_stock(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=5,
            user=self.user
        )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            15
        )

        movement.quantity = 8
        movement.save()

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            15
        )
        
        
        
    def test_adjustment_does_not_change_stock_currently(self):

        StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.ADJUSTMENT,
            quantity=5,
            user=self.user
        )

        self.stock_item.refresh_from_db()

        self.assertEqual(
            self.stock_item.quantity,
            10
        )
        
        
    def test_stock_movement_str(self):

        movement = StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.IN,
            quantity=5,
            user=self.user
        )

        self.assertEqual(
            str(movement),
            "IN - HP EliteBook : 5"
        )