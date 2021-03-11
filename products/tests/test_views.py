from django.test import TestCase, Client, RequestFactory
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django_libs.tests.mixins import ViewTestMixin

from .factories import (
    CategoryFactory,
    Product_FamilyFactory,
    ProductFactory,
)
from products.models import Category, Product_Family, Product
from django.contrib.auth.models import User
from products.forms import ProductForm, ProductFamilyForm

from django.contrib.messages import get_messages

client = Client()


class AllProductsViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def get_view_name(self):
        return 'products'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'products/products.html')

    def test_view_products(self):
        category = CategoryFactory()
        product_family = Product_FamilyFactory()
        self.product1 = ProductFactory(
            category=category, product_family=product_family)
        self.product2 = ProductFactory(
            category=category, product_family=product_family)

        response = self.client.get(self.get_url())

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.product_family)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, self.product2.product_family)

    def test_query_filter(self):
        category = CategoryFactory()
        product_family = Product_FamilyFactory()
        product1 = ProductFactory()
        product2 = ProductFactory()
        product3 = ProductFactory()
        product4 = ProductFactory()

        category1 = Category.objects.get(pk=1)
        category1.name = "gel"
        category1.save()
        product1.category.name = category1.name

        products = Product.objects.all()
        categories = []
        for p in products:
            if p.category == "category1.name":
                return
            else:
                categories.append(p.category)

        value_list = ["gel", ""]
        for v in value_list:
            if v:
                url = '{url}?{filter}={value}'.format(
                    url=reverse('products'), filter='q', value=v)
                # With string format finally we expect a url like;
                # '/products/?q=gel'
                response = self.client.get(url)
                self.assertContains(response, product1.category)
                self.assertNotContains(response, categories)
            else:
                url = '{url}?{filter}={value}'.format(
                    url=reverse('products'), filter='q', value="")
                response = self.client.get(url)
                messages = list(get_messages(response.wsgi_request))
                self.assertEqual(len(messages), 1)
                for m in messages:
                    self.assertEqual(
                    str(m), "You didn't enter any search criteria.")
                self.assertRedirects(
                    response, '/products/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_category_filter(self):
            category = CategoryFactory()
            product_family = Product_FamilyFactory()
            product1 = ProductFactory()
            product2 = ProductFactory()
            product3 = ProductFactory()
            product4 = ProductFactory()

            category2 = Category.objects.get(pk=1)
            category2.name = "gowns"
            category2.save()
            product2.category.name = category2.name

            products = Product.objects.all()
            categories_all = []
            for p in products:
                if p.category == "category2.name":
                    return
                else:
                    categories_all.append(p.category)

            value_list = ["gowns", ""]
            for v in value_list:
                if v:
                    url = '{url}?{filter}={value}'.format(
                        url=reverse('products'), filter='category', value=v)
                    # With string format finally we expect a url like;
                    # '/products/?q=gel'
                    response = self.client.get(url)
                    self.assertContains(response, product2.category)
                    self.assertNotContains(response, categories_all)
                else:
                    url = '{url}?{filter}={value}'.format(
                        url=reverse('products'), filter='category', value="")
                    response = self.client.get(url)
                    self.assertTemplateUsed(response, 'products/products.html')


class AddProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(AddProductViewTestCase, cls).setUpClass()

    def test_database_size(self):
        self.assertEqual(len(Product.objects.all()), 4)

    def get_view_name(self):
        return 'add_product'

    def test_view_uses_correct_template(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.response = self.client.get(reverse(self.get_view_name()))
        self.assertTemplateUsed(self.response, 'products/add_product.html')

    def test_add_product_view(self):
        # case 1 - Anonymous User
        self.is_not_callable()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, 'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/add/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable()
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_add_product_post_and_form_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        count1 = Product.objects.count()
        # Post and Form is Valid
        data1 = {
            'name': 'Test Product 111',
            'category': '3',
            'product_family': '5',
            'size': '8oz.'
        }
        form = ProductForm(data=data1)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('add_product'), data=data1)
        # Site redirects after posting data
        product_get = get_object_or_404(Product, name='Test Product 111')
        product_get_id = product_get.id
        self.assertRedirects(
            response, '/products/{product_id}/'.format(product_id=product_get_id), status_code=302, target_status_code=200, fetch_redirect_response=True)
        # Success message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(str(m), "Successfully added product!")
        # Confirm post added product to database
        count2 = Product.objects.count()
        calc2 = count1 + 1
        self.assertEqual(count2, calc2)

    def test_add_product_post_and_form_not_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        count1 = Product.objects.count()
        # Post and Form Not Valid With Message
        data2 = {
            'name': "",
            'category': '3',
            'product_family': '5',
        }
        # Form is not valid and try to post
        form = ProductForm(data=data2)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('add_product'), data=data2)
        # Error message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
            str(m), "Failed to add product. Please ensure the form is valid.")
        # Confirm post added product to database
        count2 = Product.objects.count()
        calc2 = count1 + 1
        self.assertNotEqual(count2, calc2)

    def test_database_add(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.product5 = ProductFactory()
        self.assertEqual(len(Product.objects.all()), 5)


class EditProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(EditProductViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'edit_product'

    def test_edit_product_view(self):
        Product.objects.get_or_create(pk=3)
        pk = 3
        # case 1 - Anonymous User
        self.is_not_callable(kwargs={'product_id': pk})
        response = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        self.assertRedirects(
            response, 'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/edit/3/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable(kwargs={'product_id': pk})
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_product_post_and_form_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        # Post and Form is Valid
        product = Product.objects.get_or_create(id=3)
        data5 = {
            'name': 'Test Change Product Name',
        }
        form = ProductForm(data=data5, instance=product)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('edit_product'), data=data5)
        # Site redirects after posting data
        product_get = get_object_or_404(Product, name='Test Change Product Name')
        product_get_id = product_get.id
        self.assertRedirects(
            response, '/products/{product_id}/'.format(product_id=product_get_id), status_code=302, target_status_code=200, fetch_redirect_response=True)
        # Success message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(str(m), "Successfully updated product!")

    def test_edit_product_post_and_form_not_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        # Post and Form Not Valid With Message
        product = Product.objects.get_or_create(pk=3)
        print(product)
        update_url = reverse('edit_product', kwargs={'product_id': '3'})
        # Get the form
        r = self.client.get(update_url)
        # retrieve form data as dict
        form = r.context['form']
        data = form.initial
        # manipulate some data
        data['name'] = ''
        # Post to form
        r = self.client.post(update_url, data)
        # Retrieve again and check for change
        r = self.client.get(update_url)
        self.assertNotEqual(r.context['form'].initial['name'], '')
        # Error message appears
        messages = list(get_messages(r.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
            str(m), "Failed to update product. Please ensure the form is valid.")

    def test_database_update(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.product4.name = 'Product Name Changed'
        self.product4.save()
        self.assertEqual(self.product4.name, 'Product Name Changed')


class DeleteProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(DeleteProductViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'delete_product'

    def test_delete_product_view(self):
        Product.objects.get_or_create(pk=3)
        pk = 3
        # case 1 - Anonymous User
        self.is_not_callable(kwargs={'product_id': pk})
        response = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        self.assertRedirects(
            response, 'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/delete/3/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable(kwargs={'product_id': pk})
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_database_delete(self):
        count = Product.objects.count()
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.product3.delete()
        length = count - 1
        self.assertEqual(len(Product.objects.all()), length)


class AllProductFamiliesViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def get_view_name(self):
        return 'product_families'

    def test_get(self):
        self.product_family1 = Product_FamilyFactory()
        self.product_family2 = Product_FamilyFactory()

        # case 1 - Anonymous User
        self.is_not_callable()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, 'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/product_families/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable()
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_view_uses_correct_template(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'products/product_families.html')

    def test_view_product_families(self):
        self.product_family1 = Product_FamilyFactory()
        self.product_family2 = Product_FamilyFactory()

        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        response = self.client.get(self.get_url())

        self.assertContains(response, self.product_family1.name)
        self.assertContains(response, self.product_family1.brand_name)
        self.assertContains(response, self.product_family2.name)
        self.assertContains(response, self.product_family2.brand_name)


class AddProductFamilyViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.product_family1 = Product_FamilyFactory()
        cls.product_family2 = Product_FamilyFactory()
        cls.product_family3 = Product_FamilyFactory()
        cls.product_family4 = Product_FamilyFactory()
        super(AddProductFamilyViewTestCase, cls).setUpClass()

    def test_database_size(self):
        self.assertEqual(len(Product_Family.objects.all()), 4)

    def get_view_name(self):
        return 'add_product_family'

    def test_view_uses_correct_template(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.response = self.client.get(reverse(self.get_view_name()))
        self.assertTemplateUsed(self.response, 'products/add_product_family.html')

    def test_add_product_family_view(self):
        # case 1 - Anonymous User
        self.is_not_callable()
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, 'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/add_pf/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable()
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_add_product_family_post_and_form_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        count1 = Product_Family.objects.count()
        # Post and Form is Valid
        data3 = {
            'name': 'Test Product Family 75',
            'brand_name': 'Test Brand '
        }
        form = ProductFamilyForm(data=data3)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('add_product_family'), data=data3)
        # Site redirects after posting data
        self.assertRedirects(
            response, '/products/product_families/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # Success message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(str(m), "Successfully added product family!")
        # Confirm post added product family to database
        count2 = Product_Family.objects.count()
        calc2 = count1 + 1
        self.assertEqual(count2, calc2)

    def test_add_product_family_post_and_form_not_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        count1 = Product_Family.objects.count()
        # Post and Form Not Valid With Message
        data4 = {
            'name': "",
        }
        # Form is not valid and try to post
        form = ProductFamilyForm(data=data4)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('add_product_family'), data=data4)
        # Error message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
            str(m), "Failed to add product family. Please ensure the form is valid.")
        # Confirm post added product to database
        count2 = Product_Family.objects.count()
        calc2 = count1 + 1
        self.assertNotEqual(count2, calc2)

    def test_database_add_product_family(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.product_family5 = Product_FamilyFactory()
        self.assertEqual(len(Product_Family.objects.all()), 5)


class EditProductFamilyViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        cls.product_family1 = Product_FamilyFactory()
        cls.product_family2 = Product_FamilyFactory()
        cls.product_family3 = Product_FamilyFactory()
        cls.product_family4 = Product_FamilyFactory()
        super(EditProductFamilyViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'edit_product_family'

    def test_edit_product_family_view(self):
        Product_Family.objects.get_or_create(pk=3)
        pk = 3
        # case 1 - Anonymous User
        self.is_not_callable(kwargs={'product_family_id': pk})
        response = self.client.get(
            self.get_url(view_kwargs={'product_family_id': pk}))
        self.assertRedirects(
            response, 'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/edit_pf/3/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable(kwargs={'product_family_id': pk})
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(
            self.get_url(view_kwargs={'product_family_id': pk}))
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_database_edit_product_family(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.product_family4.name = 'Product Family Name Changed'
        self.product_family4.save()
        self.assertEqual(
            self.product_family4.name, 'Product Family Name Changed')


class ProductDetailViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    def get_view_name(self):
        return 'product_detail'

    def test_get(self):
        pk = 2
        self.is_callable(kwargs={'product_id': pk})

    def test_view_products(self):
        category = CategoryFactory()
        product_family = Product_FamilyFactory()
        self.product99 = ProductFactory(
            pk=99, category=category, product_family=product_family)

        response = self.client.get(
            self.get_url(view_kwargs={'product_id': 99}))

        self.assertContains(response, self.product99.name)
        self.assertContains(response, self.product99.product_family)
