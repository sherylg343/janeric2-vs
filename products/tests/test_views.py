from django.test import TestCase, Client, RequestFactory
from django.shortcuts import render, redirect, reverse

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
    @classmethod
    def setUpClass(cls):
        multi_db = True
        cls.category1 = CategoryFactory()
        cls.category2 = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        cls.product5 = ProductFactory()
        super(AllProductsViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'products'

    def test_get(self):
        self.is_callable()

    def test_view_uses_correct_template(self):
        self.response = self.client.get(self.get_url())
        self.assertTemplateUsed(self.response, 'products/products.html')

    def test_view_products(self):
        product1 = self.product1
        product2 = self.product2

        response = self.client.get(self.get_url())

        self.assertContains(response, product1)
        self.assertContains(response, product2)

    def test_query_filter(self):
        category1 = self.category1
        product_family = self.product_family
        product1 = self.product1
        product2 = self.product2
        product3 = self.product3
        product5 = self.product5

        category1.name = "Gel"
        category1.save()
        product1.category.name = category1.name
        product1.save()
        product5.name = "Gel"
        product5.save()

        products_q = Product.objects.all()

        value_list = ["Gel", ""]
        for v in value_list:
            if v:
                query = v.strip('"')
                url = '{url}?{filter}={value}'.format(
                    url=reverse('products'), filter='q', value=query)
                # With string format finally we expect a url like;
                # '/products/?q=Gel'
                response_q = self.client.get(url)
                self.assertContains(response_q, product1 and product5)
                self.assertNotContains(response_q, product3)
            else:
                url = '{url}?{filter}={value}'.format(
                    url=reverse('products'), filter='q', value="")
                response_x = self.client.get(url)
                messages = list(get_messages(response_x.wsgi_request))
                self.assertEqual(len(messages), 1)
                for m in messages:
                    self.assertEqual(
                    str(m), "You didn't enter any search criteria.")
                self.assertRedirects(
                    response_x, '/products/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_category_filter(self):
            category2 = self.category2
            product1 = self.product1
            product2 = self.product2
            product3 = self.product3
            product4 = self.product4

            pk = category2.id
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
                    # '/products/?category=gowns'
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
        multi_db = True
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
            'name': 'Test Product 6b',
            'category': '3',
            'product_family': '5',
            'size': '8oz.'
        }
        form = ProductForm(data=data1)
        self.assertTrue(form.is_valid())
        add_url = reverse('add_product')
        response_add = self.client.post(add_url, data=data1, follow=True)
        # find product_details page for added product
        url_search = self.client.get(
            '/products/', {'name': 'Test Product 6b'}, HTTP_ACCEPT='application/json')
        self.assertTrue(url_search, 200)
        # Success message appears
        messages = list(get_messages(response_add.wsgi_request))
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
        multi_db = True
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

    def test_edit_product_post(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        product3 = self.product3
        pk = product3.id

        # Get the form
        r = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        form_product = r.context['form']
        data_product = form_product.initial
        name_orig = data_product['name']
        # Message appears when loading form
        messages = list(get_messages(r.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), 'You are editing {name}'.format(name=name_orig))
        # manipulate some data
        data4 = {
            'name': 'Test Change Product Name',
            'category': "10",
            'product_family': "5",
            'SKU': "HM145",
            #'image': "image.png",
            #'size': '16oz.',
            #'pack': '4',
            'price': "3",
            #'description': "the wall is white.",
            'active': True,
        }
    
        # Post edits
        post_product_form = ProductForm(instance=product3, data=data4)
        self.assertTrue(post_product_form.is_valid)
        # Post to form
        update_url_p = reverse('edit_product', kwargs={'product_id': pk})
        response_post_product = self.client.post(update_url_p, data=data4)
        # find product_details page for added product
        url_search_product = self.client.get(
            '/products/', {'name': 'Test Change Product Name'}, HTTP_ACCEPT='application/json')
        self.assertTrue(url_search_product, 200)
        # Test ProductForm saves
        response_updated_product = self.client.get(self.get_url(view_kwargs={'product_id': pk}))
        form2 = response_updated_product.context['form']
        data2 = form2.initial
        updated_product_name = data2['name']
        self.assertEqual(updated_product_name, 'Test Change Product Name')
        # Site redirects after posting data
        self.assertRedirects(
            response_post_product, '/products/{product_id}/'.format(product_id=pk), status_code=302, target_status_code=200, fetch_redirect_response=True)
        # Success message appears
        messages = list(get_messages(response_post_product.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(str(m), "Successfully updated product!")

    def test_edit_product_post_and_form_not_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        # Post and Form Not Valid With Message
        product = self.product4
        pk = product.id
        update_url = reverse('edit_product', kwargs={'product_id': pk})
        # Get the form
        r = self.client.get(update_url)
        # retrieve form data as dict
        form = r.context['form']
        data = form.initial
        name = data['name']
        # Message appears when loading form
        messages = list(get_messages(r.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), 'You are editing {name}'.format(name=name))
        # manipulate some data
        data2 = {
            'name': '',
            'category': '3',
            'product_family': '2',
            'id': pk,
            'SKU': 'XYZ',
            'image': 'gel.png',
            'size': '8oz.',
            'pack': '4',
            'price': '25',
            'description': "this is edit test",
        }
        # Post to form
        r_p = self.client.post(update_url, data2)
        # Form not valid
        post_form = ProductForm(data=data2)
        self.assertFalse(post_form.is_valid())
        # Error message appears
        messages = list(get_messages(r_p.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), 'Failed to update product. '
                'Please ensure the form is valid.')

    def test_database_update(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.product4.name = 'Product Name Changed'
        self.product4.save()
        self.assertEqual(self.product4.name, 'Product Name Changed')


class DeactivateProductViewTestCase(ViewTestMixin, TestCase):
    """ Test when products queried by keyword or category """
    @classmethod
    def setUpClass(cls):
        multi_db = True
        cls.category = CategoryFactory()
        cls.product_family = Product_FamilyFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()
        cls.product3 = ProductFactory()
        cls.product4 = ProductFactory()
        super(DeactivateProductViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'deactivate_product'

    def test_deactivate_product_view(self):
        product = self.product4
        product.active = False
        pk = product.id
        # case 1 - Anonymous User
        self.is_not_callable(kwargs={'product_id': pk})
        response = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        self.assertRedirects(
            response, f'https://janeric2.herokuapp.com/accounts/login/?next=http%3A//testserver/products/deactivate/{pk}/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # case 2 - superuser
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        self.is_callable(kwargs={'product_id': pk})
        self.assertEqual(product.active, False)
        # case 3 - User but not superuser
        user1 = User.objects.create_user(
            'testing', 'joe@testing.com', 'testingpassword')
        self.client.force_login(user=user1)
        response = self.client.get(
            self.get_url(view_kwargs={'product_id': pk}))
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)




class AllProductFamiliesViewTestCase(ViewTestMixin, TestCase):
    """ Tests for all_products view """
    @classmethod
    def setUpClass(cls):
        multi_db = True
        cls.product_family1 = Product_FamilyFactory()
        cls.product_family2 = Product_FamilyFactory()
        super(AllProductFamiliesViewTestCase, cls).setUpClass()

    def get_view_name(self):
        return 'product_families'

    def test_get(self):
        product_family1 = self.product_family1
        product_family2 = self.product_family2

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
        product_family1 = self.product_family1
        product_family2 = self.product_family2

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
        multi_db = True
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
        multi_db = True
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

    def test_edit_product_family_post_and_form_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        product_family = self.product_family2
        pk = product_family.id
        update_url = reverse(
            'edit_product_family', kwargs={'product_family_id': pk})
        # manipulate some data
        data8 = {
            'name': 'Test Change Product Family Name',
            'brand_name': 'Test Brand Name',
        }
        # Form is valid
        post_pf_form = ProductFamilyForm(instance=product_family, data=data8)
        self.assertTrue(post_pf_form.is_valid())
        self.assertEquals(
            product_family.name, "Test Change Product Family Name")
        # Test ProductFamilyForm saves
        # Post to form
        response_pf = self.client.post(update_url, data=data8)
        response_updated = self.client.get(update_url)
        form = response_updated.context['form']
        data = form.initial
        updated_name = data['name']
        self.assertEqual(updated_name, 'Test Change Product Family Name')
        # Site redirects after posting data
        self.assertRedirects(
            response_pf, '/products/product_families/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        # Success message appears
        messages = list(get_messages(response_pf.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(str(m), 'Successfully updated product family!')

    def test_edit_product_post_and_form_not_valid(self):
        user = User.objects.create_superuser(username='admin')
        self.client.force_login(user=user)
        # Post and Form Not Valid With Message
        product_family = self.product_family4
        pk = product_family.id
        update_url = reverse(
            'edit_product_family', kwargs={'product_family_id': pk})
        # manipulate some data
        data2 = {
            'name': '',
            'brand_name': 'Test Brand Name',
        }
        # Post to form
        r_p = self.client.post(update_url, data2)
        # Form not valid
        post_form = ProductFamilyForm(data=data2)
        self.assertFalse(post_form.is_valid())
        # Error message appears
        messages = list(get_messages(r_p.wsgi_request))
        self.assertEqual(len(messages), 1)
        for m in messages:
            self.assertEqual(
                str(m), 'Failed to update product family. '
                'Please ensure the form is valid.')

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
