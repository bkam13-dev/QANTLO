from django.test import TestCase

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



class StockMovementSignalTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Informatique",
            slug="informatique"
        )

        self.brand = Brand.objects.create(
            name="HP",
            description="Ordinateurs HP"
        )

        self.supplier = Supplier.objects.create(
            company_name="Tech Distribution",
            contact_name="Jean Paul",
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
            purchase_price=300000,
            selling_price=400000,
            min_stock_level=5
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
        
        
def test_signal_increases_stock(self):

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
    
    
def test_multiple_in_movements_accumulate(self):

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.user
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=10,
        user=self.user
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=20,
        user=self.user
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        45
    )
    
    
def test_signal_decreases_stock(self):

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
    
    
    
def test_in_then_out(self):

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=20,
        user=self.user
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.OUT,
        quantity=8,
        user=self.user
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        22
    )
    
    
def test_out_exactly_all_stock(self):

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.OUT,
        quantity=10,
        user=self.user
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        0
    )
    
    
    
def test_out_more_than_available_stock_fails(self):

    with self.assertRaises(ValueError):
        StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.OUT,
            quantity=11,
            user=self.user
        )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        10
    )
    
    
def test_failed_out_does_not_leave_stock_movement(self):

    initial_count = StockMovement.objects.count()

    with self.assertRaises(ValueError):
        StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.OUT,
            quantity=50,
            user=self.user
        )

    self.assertEqual(
        StockMovement.objects.count(),
        initial_count
    )
    
    
def test_updating_movement_does_not_modify_stock(self):

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

    movement.quantity = 20
    movement.save()

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        15
    )
    
    
    
def test_adjustment_currently_does_not_change_stock(self):

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
    
    
    
def test_zero_quantity_does_not_change_stock(self):

    StockMovement.objects.create(
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
    
    

def test_negative_quantity_is_rejected(self):

    movement = StockMovement(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=-5,
        user=self.user
    )

    from django.core.exceptions import ValidationError

    with self.assertRaises(ValidationError):
        movement.full_clean()
        
        
def test_stock_cannot_become_negative(self):

    with self.assertRaises(ValueError):

        StockMovement.objects.create(
            item=self.stock_item,
            movement_type=StockMovement.MovementType.OUT,
            quantity=11,
            user=self.user
        )

    self.stock_item.refresh_from_db()

    self.assertGreaterEqual(
        self.stock_item.quantity,
        0
    )
    
    
    
def test_realistic_stock_movement_sequence(self):

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=50,
        user=self.user
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.OUT,
        quantity=20,
        user=self.user
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=15,
        user=self.user
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.OUT,
        quantity=5,
        user=self.user
    )

    self.stock_item.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        50
    )
    
    
    
def test_movement_only_changes_related_stock_item(self):

    product2 = Product.objects.create(
        category=self.category,
        brand=self.brand,
        supplier=self.supplier,
        name="Dell Latitude",
        barcode="987654321",
        purchase_price=250000,
        selling_price=350000,
        min_stock_level=5
    )

    stock_item2 = StockItem.objects.create(
        warehouse=self.warehouse,
        product=product2,
        quantity=100
    )

    StockMovement.objects.create(
        item=self.stock_item,
        movement_type=StockMovement.MovementType.IN,
        quantity=5,
        user=self.user
    )

    self.stock_item.refresh_from_db()
    stock_item2.refresh_from_db()

    self.assertEqual(
        self.stock_item.quantity,
        15
    )

    self.assertEqual(
        stock_item2.quantity,
        100
    )
    
    
    
