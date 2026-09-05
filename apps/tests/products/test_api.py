from decimal import Decimal
import uuid

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import (
    Category,
    Supplier,
    Customer,
    Brand,
    Product,
)



class CategoryAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Informatique",
            slug="informatique"
        )

    def get_list_url(self):
        return reverse("category-list")

    def get_detail_url(self, pk):
        return reverse("category-detail", kwargs={"pk": pk})
    
    
    def test_get_category_list(self):
        response = self.client.get(self.get_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
    def test_get_category_list(self):
        response = self.client.get(self.get_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["name"],
            "Informatique"
        )
        
        

    def test_get_category_detail(self):
        url = self.get_detail_url(self.category.id)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["name"],
            "Informatique"
        )

        self.assertEqual(
            response.data["slug"],
            "informatique"
        )
        
        
        
    def test_get_category_detail_not_found(self):
        fake_id = uuid.uuid4()

        url = self.get_detail_url(fake_id)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        
        
    def test_create_category(self):
        data = {
            "name": "Téléphones",
            "slug": "telephones"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Category.objects.count(),
            2
        )
        
        category = Category.objects.get(
            name="Téléphones"
        )

        self.assertEqual(
            category.slug,
            "telephones"
        )
        
        
    def test_create_category_without_name(self):
        data = {
            "slug": "telephones"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Category.objects.count(),
            1
        )
        
            
    def test_create_category_with_duplicate_slug(self):
        data = {
            "name": "Autre catégorie",
            "slug": "informatique"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        
    def test_update_category_with_put(self):
        data = {
            "name": "Électronique",
            "slug": "electronique"
        }

        url = self.get_detail_url(self.category.id)

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
        self.category.refresh_from_db()

        self.assertEqual(
            self.category.name,
            "Électronique"
        )

        self.assertEqual(
            self.category.slug,
            "electronique"
        )
        
        
    def test_update_category_with_patch(self):
        data = {
            "name": "Nouveaux ordinateurs"
        }

        url = self.get_detail_url(self.category.id)

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.category.refresh_from_db()

        self.assertEqual(
            self.category.name,
            "Nouveaux ordinateurs"
        )

        self.assertEqual(
            self.category.slug,
            "informatique"
        )
        
        
        
    def test_delete_category(self):
        url = self.get_detail_url(self.category.id)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Category.objects.filter(
                id=self.category.id
            ).exists()
        )
        
            
    def test_create_category_generates_slug(self):
        data = {
            "name": "Ordinateurs portables",
            "slug": ""
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        category = Category.objects.get(
            name="Ordinateurs portables"
        )

        self.assertEqual(
            category.slug,
            "ordinateurs-portables"
        )
        


class BrandAPITest(APITestCase):

    def setUp(self):
        self.brand = Brand.objects.create(
            name="HP",
            description="Marque informatique"
        )

    def get_list_url(self):
        return reverse("brand-list")

    def get_detail_url(self, pk):
        return reverse(
            "brand-detail",
            kwargs={"pk": pk}
        )

   
    def test_get_brand_list(self):
        response = self.client.get(
            self.get_list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["name"],
            "HP"
        )



    def test_get_brand_detail(self):
        response = self.client.get(
            self.get_detail_url(self.brand.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["name"],
            "HP"
        )

        self.assertEqual(
            response.data["description"],
            "Marque informatique"
        )



    def test_get_brand_detail_not_found(self):
        fake_id = uuid.uuid4()

        response = self.client.get(
            self.get_detail_url(fake_id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )



    def test_create_brand(self):
        data = {
            "name": "Dell",
            "description": "Fabricant informatique"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Brand.objects.count(),
            2
        )

        brand = Brand.objects.get(
            name="Dell"
        )

        self.assertEqual(
            brand.description,
            "Fabricant informatique"
        )


    def test_create_brand_without_name(self):
        data = {
            "description": "Fabricant informatique"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Brand.objects.count(),
            1
        )



    def test_update_brand_with_put(self):
        data = {
            "name": "HP Inc.",
            "description": "Nouvelle description"
        }

        response = self.client.put(
            self.get_detail_url(self.brand.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.brand.refresh_from_db()

        self.assertEqual(
            self.brand.name,
            "HP Inc."
        )

        self.assertEqual(
            self.brand.description,
            "Nouvelle description"
        )



    def test_update_brand_with_patch(self):
        data = {
            "name": "HP Enterprise"
        }

        response = self.client.patch(
            self.get_detail_url(self.brand.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.brand.refresh_from_db()

        self.assertEqual(
            self.brand.name,
            "HP Enterprise"
        )

        self.assertEqual(
            self.brand.description,
            "Marque informatique"
        )


    def test_delete_brand(self):
        response = self.client.delete(
            self.get_detail_url(self.brand.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Brand.objects.filter(
                id=self.brand.id
            ).exists()
        )
        

class SupplierAPITest(APITestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(
            company_name="Tech Distribution",
            contact_name="Jean Dupont",
            email="contact@tech.com",
            phone="0700000000",
            address="Abidjan, Cocody"
        )

    def get_list_url(self):
        return reverse("supplier-list")

    def get_detail_url(self, pk):
        return reverse(
            "supplier-detail",
            kwargs={"pk": pk}
        )


    def test_get_supplier_list(self):
        response = self.client.get(
            self.get_list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["company_name"],
            "Tech Distribution"
        )


    def test_get_supplier_detail(self):
        response = self.client.get(
            self.get_detail_url(self.supplier.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["company_name"],
            "Tech Distribution"
        )

        self.assertEqual(
            response.data["contact_name"],
            "Jean Dupont"
        )

        self.assertEqual(
            response.data["email"],
            "contact@tech.com"
        )

        self.assertEqual(
            response.data["phone"],
            "0700000000"
        )

        self.assertEqual(
            response.data["address"],
            "Abidjan, Cocody"
        )


    def test_get_supplier_not_found(self):
        response = self.client.get(
            self.get_detail_url(uuid.uuid4())
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


    def test_create_supplier(self):
        data = {
            "company_name": "Global Computer",
            "contact_name": "Paul Martin",
            "email": "paul@global.com",
            "phone": "0500000000",
            "address": "Abidjan, Plateau"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Supplier.objects.count(),
            2
        )

        supplier = Supplier.objects.get(
            company_name="Global Computer"
        )

        self.assertEqual(
            supplier.email,
            "paul@global.com"
        )


    def test_create_supplier_without_company_name(self):
        data = {
            "contact_name": "Paul Martin",
            "email": "paul@global.com",
            "phone": "0500000000",
            "address": "Abidjan"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Supplier.objects.count(),
            1
        )


    def test_update_supplier_with_put(self):
        data = {
            "company_name": "Tech Distribution CI",
            "contact_name": "Nouveau contact",
            "email": "new@tech.com",
            "phone": "0100000000",
            "address": "Cocody Riviera"
        }

        response = self.client.put(
            self.get_detail_url(self.supplier.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.supplier.refresh_from_db()

        self.assertEqual(
            self.supplier.company_name,
            "Tech Distribution CI"
        )

        self.assertEqual(
            self.supplier.email,
            "new@tech.com"
        )


    def test_update_supplier_with_patch(self):
        data = {
            "phone": "0123456789"
        }

        response = self.client.patch(
            self.get_detail_url(self.supplier.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.supplier.refresh_from_db()

        self.assertEqual(
            self.supplier.phone,
            "0123456789"
        )

        self.assertEqual(
            self.supplier.company_name,
            "Tech Distribution"
        )


    def test_delete_supplier(self):
        response = self.client.delete(
            self.get_detail_url(self.supplier.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Supplier.objects.filter(
                id=self.supplier.id
            ).exists()
        )
        

class CustomerAPITest(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            company_name="ABC SARL",
            contact_name="Koffi Jean",
            first_name="Jean",
            last_name="Koffi",
            email="jean@abc.com",
            phone="0700000000",
            address="Abidjan, Cocody"
        )

    def get_list_url(self):
        return reverse("customer-list")

    def get_detail_url(self, pk):
        return reverse(
            "customer-detail",
            kwargs={"pk": pk}
        )


    def test_get_customer_list(self):
        response = self.client.get(
            self.get_list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["company_name"],
            "ABC SARL"
        )


    def test_get_customer_detail(self):
        response = self.client.get(
            self.get_detail_url(self.customer.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["first_name"],
            "Jean"
        )

        self.assertEqual(
            response.data["last_name"],
            "Koffi"
        )


    def test_get_customer_not_found(self):
        response = self.client.get(
            self.get_detail_url(uuid.uuid4())
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


    def test_create_customer(self):
        data = {
            "company_name": "XYZ SARL",
            "contact_name": "Marie Kouassi",
            "first_name": "Marie",
            "last_name": "Kouassi",
            "email": "marie@xyz.com",
            "phone": "0500000000",
            "address": "Abidjan, Plateau"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Customer.objects.count(),
            2
        )

        customer = Customer.objects.get(
            email="marie@xyz.com"
        )

        self.assertEqual(
            customer.first_name,
            "Marie"
        )


    def test_create_customer_without_company_name(self):
        data = {
            "contact_name": "Marie Kouassi",
            "first_name": "Marie",
            "last_name": "Kouassi",
            "email": "marie@xyz.com",
            "phone": "0500000000",
            "address": "Abidjan"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        customer = Customer.objects.get(
            email="marie@xyz.com"
        )

        self.assertIsNone(
            customer.company_name
        )


    def test_create_customer_without_first_name(self):
        data = {
            "contact_name": "Marie Kouassi",
            "last_name": "Kouassi",
            "email": "marie@xyz.com",
            "phone": "0500000000",
            "address": "Abidjan"
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


    def test_update_customer_with_put(self):
        data = {
            "company_name": "ABC CI",
            "contact_name": "Nouveau contact",
            "first_name": "Paul",
            "last_name": "Koffi",
            "email": "paul@abc.com",
            "phone": "0100000000",
            "address": "Abidjan, Marcory"
        }

        response = self.client.put(
            self.get_detail_url(self.customer.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.customer.refresh_from_db()

        self.assertEqual(
            self.customer.first_name,
            "Paul"
        )

        self.assertEqual(
            self.customer.address,
            "Abidjan, Marcory"
        )


    def test_update_customer_with_patch(self):
        data = {
            "phone": "0123456789"
        }

        response = self.client.patch(
            self.get_detail_url(self.customer.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.customer.refresh_from_db()

        self.assertEqual(
            self.customer.phone,
            "0123456789"
        )

        self.assertEqual(
            self.customer.first_name,
            "Jean"
        )


    def test_delete_customer(self):
        response = self.client.delete(
            self.get_detail_url(self.customer.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Customer.objects.filter(
                id=self.customer.id
            ).exists()
        )


class ProductAPITest(APITestCase):

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
            contact_name="Jean Dupont",
            email="contact@tech.com",
            phone="0700000000",
            address="Abidjan, Cocody"
        )

    def get_list_url(self):
        return reverse("product-list")

    def get_detail_url(self, pk):
        return reverse(
            "product-detail",
            kwargs={"pk": pk}
        )
        
        
    def create_product(self, **kwargs):
        data = {
            "category": self.category.id,
            "brand": self.brand.id,
            "supplier": self.supplier.id,
            "sku": "",
            "barcode": "123456789",
            "name": "HP EliteBook",
            "slug": "",
            "description": "Ordinateur portable professionnel",
            "purchase_price": "300000.00",
            "selling_price": "400000.00",
            "min_stock_level": 5,
        }

        data.update(kwargs)

        return Product.objects.create(
            category=self.category,
            brand=self.brand,
            supplier=self.supplier,
            barcode=data["barcode"],
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
            purchase_price=Decimal(data["purchase_price"]),
            selling_price=Decimal(data["selling_price"]),
            min_stock_level=data["min_stock_level"],
        )
    
    
    def test_get_product_list(self):
        product = self.create_product()

        response = self.client.get(
            self.get_list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )
        self.assertEqual(
            response.data[0]["name"],
            "HP EliteBook"
        )
    
    
    def test_get_product_detail(self):
        product = self.create_product()

        response = self.client.get(
            self.get_detail_url(product.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["name"],
            "HP EliteBook"
        )

        self.assertEqual(
            response.data["category"],
            str(self.category.id)
        )
    
    
    def test_get_product_not_found(self):
        fake_id = uuid.uuid4()

        response = self.client.get(
            self.get_detail_url(fake_id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
    
    
    def test_get_product_not_found(self):
        fake_id = uuid.uuid4()
        
        product = self.create_product()

        response = self.client.get(
            self.get_detail_url(fake_id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        
        self.assertEqual(
            product.sku,
            "INF-HP-000001"
        )
        
        
    def test_product_sku_number_increments(self):
        product1 = self.create_product(
            name="Produit 1",
            barcode="111111"
        )

        product2 = self.create_product(
            name="Produit 2",
            barcode="222222"
        )

        self.assertEqual(
            product1.sku_number,
            1
        )

        self.assertEqual(
            product2.sku_number,
            2
        )
    
    
    def test_create_product_without_name(self):
        data = {
            "category": str(self.category.id),
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "111111",
            "description": "Produit sans nom",
            "purchase_price": "300000.00",
            "selling_price": "400000.00",
            "min_stock_level": 5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    
    def test_create_product_without_category(self):
        data = {
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "111111",
            "name": "Produit test",
            "description": "Produit",
            "purchase_price": "300000.00",
            "selling_price": "400000.00",
            "min_stock_level": 5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_create_product_without_brand(self):
        data = {
            "category": str(self.category.id),
            "supplier": str(self.supplier.id),
            "barcode": "222222",
            "name": "Produit test",
            "description": "Produit",
            "purchase_price": "300000.00",
            "selling_price": "400000.00",
            "min_stock_level": 5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    
    def test_create_product_with_nonexistent_category(self):
        data = {
            "category": str(uuid.uuid4()),
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "333333",
            "name": "Produit test",
            "description": "Produit",
            "purchase_price": "300000.00",
            "selling_price": "400000.00",
            "min_stock_level": 5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_create_product_with_duplicate_barcode(self):
        self.create_product(
            barcode="123456"
        )

        data = {
            "category": str(self.category.id),
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "123456",
            "name": "Deuxième produit",
            "description": "Produit",
            "purchase_price": "300000.00",
            "selling_price": "400000.00",
            "min_stock_level": 5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    
    def test_create_product_prices(self):
        data = {
            "category": str(self.category.id),
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "444444",
            "name": "Produit prix",
            "description": "Produit",
            "purchase_price": "125000.50",
            "selling_price": "175000.75",
            "min_stock_level": 5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        product = Product.objects.get(
            name="Produit prix"
        )

        self.assertEqual(
            product.purchase_price,
            Decimal("125000.50")
        )

        self.assertEqual(
            product.selling_price,
            Decimal("175000.75")
        )
    
    
    def test_create_product_with_negative_min_stock_level(self):
        data = {
            "category": str(self.category.id),
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "555555",
            "name": "Produit négatif",
            "description": "Produit",
            "purchase_price": "100000.00",
            "selling_price": "150000.00",
            "min_stock_level": -5,
        }

        response = self.client.post(
            self.get_list_url(),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    
    def test_update_product_with_put(self):
        product = self.create_product(
            name="Ancien produit",
            barcode="666666"
        )

        data = {
            "category": str(self.category.id),
            "brand": str(self.brand.id),
            "supplier": str(self.supplier.id),
            "barcode": "777777",
            "name": "Nouveau produit",
            "description": "Nouvelle description",
            "purchase_price": "350000.00",
            "selling_price": "500000.00",
            "min_stock_level": 10,
        }

        response = self.client.put(
            self.get_detail_url(product.id),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        product.refresh_from_db()

        self.assertEqual(
            product.name,
            "Nouveau produit"
        )

        self.assertEqual(
            product.purchase_price,
            Decimal("350000.00")
        )

        self.assertEqual(
            product.selling_price,
            Decimal("500000.00")
        )
    
    
    def test_update_product_with_patch(self):
        product = self.create_product(
            name="HP EliteBook",
            barcode="888888"
        )

        response = self.client.patch(
            self.get_detail_url(product.id),
            {
                "selling_price": "450000.00"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        product.refresh_from_db()

        self.assertEqual(
            product.selling_price,
            Decimal("450000.00")
        )

        self.assertEqual(
            product.name,
            "HP EliteBook"
        )
    
    
    def test_delete_product(self):
        product = self.create_product(
            name="Produit à supprimer",
            barcode="999999"
        )

        response = self.client.delete(
            self.get_detail_url(product.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Product.objects.filter(
                id=product.id
            ).exists()
        )
    
    
    def test_update_product_category(self):
        product = self.create_product(
            barcode="101010"
        )

        new_category = Category.objects.create(
            name="Bureautique",
            slug="bureautique"
        )

        response = self.client.patch(
            self.get_detail_url(product.id),
            {
                "category": str(new_category.id)
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        product.refresh_from_db()

        self.assertEqual(
            product.category,
            new_category
        )
    
    

    

    