from decimal import Decimal
import uuid

from django.test import TestCase

from apps.products.models import (
    Category,
    Supplier,
    Customer,
    Brand,
    Product,
)

from apps.products.serializers import (
    CategorySerializer,
    SupplierSerializer,
    CustomerSerializer,
    BrandSerializer,
    ProductSerializer,
)


class CategorySerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
        )
        
        
    def test_valid_category_data(self):
        data = {
            "name": "Téléphones",
            "slug": "telephones",
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())
    
    
    def test_name_is_required(self):
        data = {
            "slug": "ordinateurs",
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


    def test_slug_is_required_by_serializer(self):
        data = {
            "name": "Téléphones",
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)


    def test_empty_data_is_invalid(self):
        serializer = CategorySerializer(data={})

        self.assertFalse(serializer.is_valid())

        self.assertIn("name", serializer.errors)
        self.assertIn("slug", serializer.errors)



    def test_empty_name_is_invalid(self):
        data = {
            "name": "",
            "slug": "test",
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


    def test_category_with_parent(self):
        data = {
            "name": "Ordinateurs portables",
            "slug": "ordinateurs-portables",
            "parent": self.category.id,
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["parent"],
            self.category,
        )


    def test_nonexistent_parent_is_invalid(self):
        data = {
            "name": "Ordinateurs",
            "slug": "ordinateurs-2",
            "parent": uuid.uuid4(),
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("parent", serializer.errors)


    def test_create_category(self):
        data = {
            "name": "Téléphones",
            "slug": "telephones",
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())

        category = serializer.save()

        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, "Téléphones")
        self.assertEqual(category.slug, "telephones")
    
    
    def test_update_category(self):
        data = {
            "name": "Ordinateurs portables",
            "slug": "ordinateurs-portables",
        }

        serializer = CategorySerializer(
            instance=self.category,
            data=data,
        )

        self.assertTrue(serializer.is_valid())

        category = serializer.save()

        self.assertEqual(
            category.name,
            "Ordinateurs portables"
        )

        self.assertEqual(
            category.slug,
            "ordinateurs-portables"
        )
    
    def test_partial_update_category(self):
        serializer = CategorySerializer(
            instance=self.category,
            data={
                "name": "Nouveaux ordinateurs"
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid())

        category = serializer.save()

        self.assertEqual(
            category.name,
            "Nouveaux ordinateurs"
        )
    
    
    def test_duplicate_slug_is_invalid(self):
        data = {
            "name": "PC",
            "slug": "ordinateurs",
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)

        
class BrandSerializerTest(TestCase):
    def test_valid_brand_data(self):
        data = {
            "name": "HP",
            "description": "Constructeur informatique",
        }

        serializer = BrandSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        
        
    def test_brand_description_is_required(self):
        data = {
            "name": "HP",
        }

        serializer = BrandSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)
        
    
    def test_create_brand(self):
        data = {
            "name": "HP",
            "description": "Constructeur informatique",
        }

        serializer = BrandSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        brand = serializer.save()

        self.assertEqual(brand.name, "HP")
    
    
class SupplierSerializerTest(TestCase):
    def test_valid_supplier_data(self):
        data = {
            "company_name": "ABC Distribution",
            "contact_name": "Jean Dupont",
            "email": "contact@abc.com",
            "phone": "0700000000",
            "address": "Abidjan",
        }

        serializer = SupplierSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        
        
def test_required_fields(self):
    serializer = SupplierSerializer(data={})

    self.assertFalse(serializer.is_valid())

    self.assertIn("company_name", serializer.errors)
    self.assertIn("contact_name", serializer.errors)
    self.assertIn("email", serializer.errors)
    self.assertIn("phone", serializer.errors)
    self.assertIn("address", serializer.errors)
    
    
def test_invalid_email(self):
    data = {
        "company_name": "ABC",
        "contact_name": "Jean",
        "email": "ceci-n-est-pas-un-email",
        "phone": "0700000000",
        "address": "Abidjan",
    }

    serializer = SupplierSerializer(data=data)

    self.assertTrue(serializer.is_valid())
    
    
class CustomerSerializerTest(TestCase):

    def test_valid_customer_data(self):
        data = {
            "company_name": "ABC SARL",
            "contact_name": "Jean",
            "first_name": "Jean",
            "last_name": "Kouassi",
            "email": "jean@example.com",
            "phone": "0700000000",
            "address": "Abidjan",
        }

        serializer = CustomerSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        
        
    def test_company_name_is_optional(self):
        data = {
            "contact_name": "Jean",
            "first_name": "Jean",
            "last_name": "Kouassi",
            "email": "jean@example.com",
            "phone": "0700000000",
            "address": "Abidjan",
        }

        serializer = CustomerSerializer(data=data)

        self.assertTrue(serializer.is_valid())
    
    
    def test_customer_required_fields(self):
        serializer = CustomerSerializer(data={})

        self.assertFalse(serializer.is_valid())

        self.assertIn("contact_name", serializer.errors)
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("phone", serializer.errors)
        self.assertIn("address", serializer.errors)
        
        
        
class ProductSerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
        )

        self.brand = Brand.objects.create(
            name="HP",
            description="Constructeur informatique",
        )

        self.supplier = Supplier.objects.create(
            company_name="ABC Distribution",
            contact_name="Jean",
            email="contact@abc.com",
            phone="0700000000",
            address="Abidjan",
        )
        
        
    def get_valid_data(self):
        return {
            "category": self.category.id,
            "brand": self.brand.id,
            "supplier": self.supplier.id,
            "name": "HP ProBook",
            "purchase_price": "250000.00",
            "selling_price": "300000.00",
            "min_stock_level": 5,
        }
        
        
    def test_valid_product_data(self):
        serializer = ProductSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(serializer.is_valid())
        
        
    def test_product_relations_are_resolved(self):
        serializer = ProductSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(serializer.is_valid())

        self.assertEqual(
            serializer.validated_data["category"],
            self.category
        )

        self.assertEqual(
            serializer.validated_data["brand"],
            self.brand
        )

        self.assertEqual(
            serializer.validated_data["supplier"],
            self.supplier
        )
        
        
    def test_product_required_fields(self):
        serializer = ProductSerializer(data={})

        self.assertFalse(serializer.is_valid())

        self.assertIn("category", serializer.errors)
        self.assertIn("brand", serializer.errors)
        self.assertIn("supplier", serializer.errors)
        self.assertIn("name", serializer.errors)
        self.assertIn("purchase_price", serializer.errors)
        self.assertIn("selling_price", serializer.errors)
        
        
    def test_nonexistent_category_is_invalid(self):
        data = self.get_valid_data()

        data["category"] = uuid.uuid4()

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)
        
        
    def test_nonexistent_brand_is_invalid(self):
        data = self.get_valid_data()

        data["brand"] = uuid.uuid4()

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("brand", serializer.errors)
        
            
    def test_nonexistent_supplier_is_invalid(self):
        data = self.get_valid_data()

        data["supplier"] = uuid.uuid4()

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("supplier", serializer.errors)
        
        
    def test_valid_prices(self):
        data = self.get_valid_data()

        data["purchase_price"] = "125000.50"
        data["selling_price"] = "175000.75"

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        self.assertEqual(
            serializer.validated_data["purchase_price"],
            Decimal("125000.50")
        )
        
        
    def test_negative_purchase_price_is_invalid(self):
        data = self.get_valid_data()

        data["purchase_price"] = "-100"

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "purchase_price",
            serializer.errors
        )
        
        
        
    def test_min_stock_level(self):
        data = self.get_valid_data()

        data["min_stock_level"] = 10

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        self.assertEqual(
            serializer.validated_data["min_stock_level"],
            10
        )
        
        
    def test_min_stock_level(self):
        data = self.get_valid_data()

        data["min_stock_level"] = 10

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        self.assertEqual(
            serializer.validated_data["min_stock_level"],
            10
        )
        
        
    def test_negative_min_stock_level_is_invalid(self):
        data = self.get_valid_data()

        data["min_stock_level"] = -1

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "min_stock_level",
            serializer.errors
        )
        
        
    def test_max_purchase_price(self):
        data = self.get_valid_data()

        data["purchase_price"] = "99999999.99"

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        
        
    def test_purchase_price_too_large(self):
        data = self.get_valid_data()

        data["purchase_price"] = "100000000.00"

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "purchase_price",
            serializer.errors
        )
        
        
    def test_decimal_min_stock_level_is_invalid(self):
        data = self.get_valid_data()

        data["min_stock_level"] = 5.5

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "min_stock_level",
            serializer.errors
        )
        
            
    def test_create_product(self):
        data = self.get_valid_data()

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        product = serializer.save()

        self.assertIsNotNone(product.id)

        self.assertEqual(
            product.name,
            "HP ProBook"
        )

        self.assertEqual(
            product.category,
            self.category
        )

        self.assertEqual(
            product.brand,
            self.brand
        )

        self.assertEqual(
            product.supplier,
            self.supplier
        )
        self.assertEqual(
            product.slug,
            "hp-probook"
        )
        
        
    def test_product_sku_is_generated(self):
        serializer = ProductSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(serializer.is_valid())

        product = serializer.save()

        self.assertIsNotNone(product.sku)
        self.assertEqual(
            product.sku,
            "ORD-HP-000001"
        )
        
        
    def test_update_product(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        data = self.get_valid_data()

        data["name"] = "HP EliteBook"
        data["purchase_price"] = "300000.00"

        serializer = ProductSerializer(
            instance=product,
            data=data,
        )

        self.assertTrue(serializer.is_valid())

        updated_product = serializer.save()

        self.assertEqual(
            updated_product.name,
            "HP EliteBook"
        )

        self.assertEqual(
            updated_product.purchase_price,
            Decimal("300000.00")
        )
        
        
    def test_partial_update_product(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        serializer = ProductSerializer(
            instance=product,
            data={
                "selling_price": "350000.00"
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid())

        product = serializer.save()

        self.assertEqual(
            product.selling_price,
            Decimal("350000.00")
        )
        
        
    def test_sku_fields_are_generated(self):
        serializer = ProductSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(serializer.is_valid())

        product = serializer.save()

        self.assertIsNotNone(product.sku)
        self.assertIsNotNone(product.sku_number)
        
        
    def test_sku_is_read_only(self):
        data = self.get_valid_data()

        data["sku"] = "FAKE-SKU"
        data["sku_number"] = 999999

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        self.assertNotIn(
            "sku",
            serializer.validated_data
        )

        self.assertNotIn(
            "sku_number",
            serializer.validated_data
        )
        
        
    def test_product_serializer_fields(self):
        serializer = ProductSerializer()

        expected_fields = {
            "id",
            "category",
            "brand",
            "supplier",
            "sku_number",
            "sku",
            "barcode",
            "name",
            "slug",
            "description",
            "purchase_price",
            "selling_price",
            "min_stock_level",
            "created_at",
            "updated_at",
        }

        self.assertEqual(
            set(serializer.fields.keys()),
            expected_fields
        )
        
        
