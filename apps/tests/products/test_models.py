
from decimal import Decimal
import uuid

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.products.models import (
    Category,
    Supplier,
    Customer,
    Brand,
    Product,
)



class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
        )

        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, "Ordinateurs")
        self.assertEqual(category.slug, "ordinateurs")
        
    def test_category_id_is_uuid(self):
        category = Category.objects.create(
            name="Téléphones",
            slug="telephones",
        )
        self.assertIsNotNone(category.id)
        

    def test_category_id_is_valid_uuid(self):
        category = Category.objects.create(
            name="Téléphones",
            slug="telephones",
        )

        self.assertIsInstance(category.id, uuid.UUID)
        
        
    def test_category_str(self):
        category = Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
        )

        self.assertEqual(str(category), "Ordinateurs")
        
        
    def test_slug_is_generated_automatically(self):
        category = Category.objects.create(
            name="Ordinateurs Portables",
        )

        self.assertEqual(
            category.slug,
            "ordinateurs-portables"
        )
        
        
    def test_slug_handles_accents(self):
        category = Category.objects.create(
            name="Électronique Générale",
        )

        self.assertEqual(
            category.slug,
            "electronique-generale"
        )
        
        
    def test_slug_handles_accents(self):
        category = Category.objects.create(
            name="Électronique Générale",
        )

        self.assertEqual(
            category.slug,
            "electronique-generale"
        )
        
        

    def test_category_children_relation(self):
        parent = Category.objects.create(
            name="Électronique",
            slug="electronique",
        )

        child = Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
            parent=parent,
        )

        self.assertIn(child, parent.children.all())
        
        
    def test_category_parent_is_optional(self):
        category = Category.objects.create(
            name="Électronique",
            slug="electronique",
        )
        self.assertIsNone(category.parent)
        
        
    def test_category_slug_must_be_unique(self):
        Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
        )

        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name="PC",
                slug="ordinateurs",
            )
            

    def test_category_name_is_required(self):
        category = Category(
            name="",
            slug="test",
        )

        with self.assertRaises(ValidationError):
            category.full_clean()
            
            
class BrandModelTest(TestCase):

    def test_create_brand(self):
        brand = Brand.objects.create(
            name="HP",
            description="Marque informatique",
        )

        self.assertIsNotNone(brand.id)
        self.assertEqual(brand.name, "HP")
        self.assertEqual(
            brand.description,
            "Marque informatique"
        )

    def test_brand_str(self):
        brand = Brand.objects.create(
            name="HP",
            description="Marque informatique",
        )

        self.assertEqual(str(brand), "HP")

    def test_brand_name_is_required(self):
        brand = Brand(
            name="",
            description="Test",
        )

        with self.assertRaises(ValidationError):
            brand.full_clean()
            
            
            
class SupplierModelTest(TestCase):

    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            company_name="ABC Distribution",
            contact_name="Jean Dupont",
            email="contact@abc.com",
            phone="0700000000",
            address="Abidjan",
        )

        self.assertIsNotNone(supplier.id)
        self.assertEqual(
            supplier.company_name,
            "ABC Distribution"
        )

    def test_supplier_str(self):
        supplier = Supplier.objects.create(
            company_name="ABC Distribution",
            contact_name="Jean Dupont",
            email="contact@abc.com",
            phone="0700000000",
            address="Abidjan",
        )

        self.assertEqual(
            str(supplier),
            "ABC Distribution"
        )

    def test_supplier_required_fields(self):
        supplier = Supplier(
            company_name="",
            contact_name="",
            email="",
            phone="",
            address="",
        )

        with self.assertRaises(ValidationError):
            supplier.full_clean()
            
            
class CustomerModelTest(TestCase):

    def test_create_company_customer(self):
        customer = Customer.objects.create(
            company_name="ABC SARL",
            contact_name="Jean",
            first_name="Paul",
            last_name="Kouassi",
            email="contact@abc.com",
            phone="0700000000",
            address="Abidjan",
        )

        self.assertEqual(str(customer), "ABC SARL")
        
    
    def test_create_individual_customer(self):
        customer = Customer.objects.create(
            company_name=None,
            contact_name="Paul",
            first_name="Paul",
            last_name="Kouassi",
            email="paul@example.com",
            phone="0700000000",
            address="Abidjan",
        )

        self.assertEqual(
            str(customer),
            "Paul Kouassi"
        )
        
        
    def test_create_individual_customer(self):
        customer = Customer.objects.create(
            company_name=None,
            contact_name="Paul",
            first_name="Paul",
            last_name="Kouassi",
            email="paul@example.com",
            phone="0700000000",
            address="Abidjan",
        )

        self.assertEqual(
            str(customer),
            "Paul Kouassi"
        )
        
        
        
    def test_company_name_is_optional(self):
        customer = Customer.objects.create(
            contact_name="Paul",
            first_name="Paul",
            last_name="Kouassi",
            email="paul@example.com",
            phone="0700000000",
            address="Abidjan",
        )
        self.assertIsNone(customer.company_name)
        
        
        
class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Ordinateurs",
            slug="ordinateurs",
        )

        self.brand = Brand.objects.create(
            name="HP",
            description="Marque informatique",
        )

        self.supplier = Supplier.objects.create(
            company_name="ABC Distribution",
            contact_name="Jean",
            email="contact@abc.com",
            phone="0700000000",
            address="Abidjan",
        )
        

    def test_create_product(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "HP ProBook")
        self.assertEqual(
            product.purchase_price,
            Decimal("250000.00")
        )
        self.assertEqual(
            product.selling_price,
            Decimal("300000.00")
        )
        
        
    def test_product_slug_is_generated(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook 450 G8",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(
            product.slug,
            "hp-probook-450-g8"
        )
        
        
    def test_min_stock_level_default(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(product.min_stock_level, 5)
        
            
    def test_product_category_relation(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(product.category, self.category)
        self.assertIn(product, self.category.products.all())
        
        
    def test_product_brand_relation(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(product.brand, self.brand)
        self.assertIn(
            product,
            self.brand.product_list.all()
        )
        
        
    def test_product_supplier_relation(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(product.supplier, self.supplier)
        self.assertIn(
            product,
            self.supplier.products_supplied.all()
        )
        
        
    def test_product_str(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(str(product), "HP ProBook")
        
        
    def test_generate_sku(self):
        product = Product(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        sku = product.generate_sku()

        self.assertEqual(
            sku,
            "ORD-HP-000001"
        )
        
        
    def test_sku_number_increments(self):
        product1 = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook 1",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        product2 = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook 2",
            purchase_price=Decimal("300000.00"),
            selling_price=Decimal("350000.00"),
        )

        self.assertEqual(product1.sku_number, 1)
        self.assertEqual(product2.sku_number, 2)
              
        self.assertEqual(
            product1.sku,
            "ORD-HP-000001"
        )

        self.assertEqual(
            product2.sku,
            "ORD-HP-000002"
        )
        
        
    def test_existing_sku_is_not_regenerated(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            sku="CUSTOM-SKU",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        self.assertEqual(product.sku, "CUSTOM-SKU")
        
        
    def test_purchase_price(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.50"),
            selling_price=Decimal("300000.75"),
        )

        self.assertEqual(
            product.purchase_price,
            Decimal("250000.50")
        )
        
        
    def test_selling_price(self):
        product = Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.50"),
            selling_price=Decimal("300000.75"),
        )

        self.assertEqual(
            product.selling_price,
            Decimal("300000.75")
        )
        
        
    def test_product_name_is_required(self):
        product = Product(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
        )

        with self.assertRaises(ValidationError):
            product.full_clean()
            
            

    def test_purchase_price_cannot_be_negative(self):
        product = Product(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("-250000.00"),
            selling_price=Decimal("300000.00"),
        )

        with self.assertRaises(ValidationError):
            product.full_clean()
        
        
    def test_min_stock_level_cannot_be_negative(self):
        product = Product(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            name="HP ProBook",
            purchase_price=Decimal("250000.00"),
            selling_price=Decimal("300000.00"),
            min_stock_level=-1,
        )

        with self.assertRaises(ValidationError):
            product.full_clean()
            
            

