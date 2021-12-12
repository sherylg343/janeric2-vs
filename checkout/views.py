from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from fedex.config import FedexConfig
from fedex.tools.conversion import sobject_to_dict

from django.conf import settings

from .forms import USZipCodeField, USStateSelect, OrderForm, ShippingForm
from .models import (
    Order, OrderLineItem, ShipFromAddress, ProductShippingData
)

from products.models import Product
from profiles.models import UserProfile
from cart.contexts import cart_contents

import stripe
import json
import logging
import sys


CONFIG_OBJ = FedexConfig(
    key=settings.FEDEX_TEST_KEY, password=settings.FEDEX_TEST_PASSWORD,
    account_number=settings.FEDEX_TEST_ACCT_NUMBER, meter_number=settings.FEDEX_TEST_METER_NUMBER
)


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        ca = request.COOKIES.get('ca')
        print("---ca:", ca)
        current_cart = cart_contents(request)
        ca_tax = current_cart['ca_tax']
        grand_total_ca = current_cart['grand_total_ca']
        stripe_total_ca = round(grand_total_ca * 100)
        # if ship to ca true, modify payment intent for revised order total
        if ca == "true":
            stripe.PaymentIntent.modify(
                pid,
                amount=stripe_total_ca,
                currency=settings.STRIPE_CURRENCY,
                metadata={
                    'cart': json.dumps(request.session.get('cart', {})),
                    'save_info': request.POST.get('save_info'),
                    'username': request.user,
                    'marketing': request.POST.get('marketing'),
                    'ca_tax': ca_tax,
                }
            )
        # if ship anywhere but ca modify intent to include metadata
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'marketing': request.POST.get('marketing'),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout_shipping(request):

    if request.method == "POST":
        print("form posted")

        ship_to_state = request.POST['ship_state'],
        ship_to_zipcode = request.POST['ship_zipcode']
        print(ship_to_state, ship_to_zipcode)

        # fedex_python API set up
        #rate = FedexRateServiceRequest(CONFIG_OBJ)

        #rate.RequestedShipment.DropoffType = "REGULAR_PICKUP"
        #rate.RequestedShipment.ServiceType = 'FEDEX_GROUND'
        #rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

        # get Product Ids and ship data for each in cart

        for product_id in cart.items():
            # get shippers data for product
            product_shipping = get_object_or_404(ProductShippingData, pk=product_id)
            print(product_shipping.shipper_address.shipper_state)

            # Shipper Address
            #rate.RequestedShipment.Shipper.Address.StateOrProvinceCode = product_shipping.shipper_address.shipper_state
            #rate.RequestedShipment.Shipper.Address.PostalCode = product_shipping.shipper_address.postal_code
            #rate.RequestedShipment.Shipper.Address.CountryCode = 'US'

            # Recipient Address
            #rate.RequestedShipment.Recipient.Address.StateOrProvinceCode = ship_to_state
            #rate.RequestedShipment.Recipient.Address.PostalCode = ship_to_zipcode
            #rate.RequestedShipment.Recipient.Address.CountryCode = 'US'

            #rate.RequestedShipment.EdtRequestType = 'NONE'
            #rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

            # FedEx package info
            #package1_weight = rate.create_wsdl_object_of_type('Weight')
            #package1_weight.Value = product_shipping.product_pkg_weight_lb
            #package1_weight.Units = "LB"
            #package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
            #package1.Weight = package1_weight
            #package1.PhysicalPackaging = 'BOX'
            #package1.GroupPackageCount = 1
            #rate.add_package(package1)

            #rate.send_request()
            #request_response = rate.response
            #response_dict = sobject_to_dict(shipment.response)
            #print(response_dict)

            return redirect(reverse('checkout'))


    # Attempt to prefill the form with any info
    # the user maintains in their profile
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            marketing_value = profile.marketing
            full_name = profile.defaultship_full_name
            shipping_form = ShippingForm(initial={
                'ship_full_name': profile.defaultship_full_name,
                'email': profile.user.email,
                'ship_street_address1': profile.defaultship_street_address1,
                'ship_street_address2': profile.defaultship_street_address2,
                'ship_city': profile.defaultship_city,
                'ship_state': profile.defaultship_state,
                'ship_zipcode': profile.defaultship_zipcode,
                'ship_phone_number': profile.defaultship_phone_number,
            })
        except UserProfile.DoesNotExist:
            shipping_form = ShippingForm()
    else:
        shipping_form = ShippingForm()
        marketing_value = "false"
        full_name = ""

    ship_state = USStateSelect()
    ship_zipcode = USZipCodeField()

    template = 'checkout/checkout_shipping.html'
    context = {
        'shipping_form': shipping_form,
        'ship_state': ship_state,
        'ship_zipcode': ship_zipcode,
        'marketing': marketing_value,
        'full_name': full_name,
    }

    return render(request, template, context)







def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    # Obtain contents of cart.context.py
    current_cart = cart_contents(request)
    ca = request.COOKIES.get('ca')
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'ship_full_name': request.POST['ship_full_name'],
            'email': request.POST['email'],
            'ship_comp_name': request.POST['ship_comp_name'],
            'ship_phone_number': request.POST['ship_phone_number'],
            'ship_street_address1': request.POST['ship_street_address1'],
            'ship_street_address2': request.POST['ship_street_address2'],
            'ship_city': request.POST['ship_city'],
            'ship_state': request.POST['ship_state'],
            'ship_zipcode': request.POST['ship_zipcode'],
            'bill_full_name': request.POST['bill_full_name'],
            'bill_phone_number': request.POST['bill_phone_number'],
            'bill_street_address1': request.POST['bill_street_address1'],
            'bill_street_address2': request.POST['bill_street_address2'],
            'bill_city': request.POST['bill_city'],
            'bill_state': request.POST['bill_state'],
            'bill_zipcode': request.POST['bill_zipcode'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            if ca == "true":
                order.ca_sales_tax = current_cart['ca_tax']
                order.grand_total = current_cart['grand_total_ca']
            else:
                order.ca_sales_tax = 0
                order.grand_total = current_cart['grand_total']
            order.save()
            for product_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. \
                        Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            request.session['marketing'] = 'marketing' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    # Reset ca to default false when first load checkout page
    ca = request.COOKIES.get('ca')
    response = HttpResponse()
    response.set_cookie('ca', 'false')
    print("ca_set", request.COOKIES.get('ca'))
    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Attempt to prefill the form with any info
    # the user maintains in their profile
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            marketing_value = profile.marketing
            full_name = profile.defaultship_full_name
            order_form = OrderForm(initial={
                'ship_full_name': profile.defaultship_full_name,
                'email': profile.user.email,
                'ship_street_address1': profile.defaultship_street_address1,
                'ship_street_address2': profile.defaultship_street_address2,
                'ship_city': profile.defaultship_city,
                'ship_state': profile.defaultship_state,
                'ship_zipcode': profile.defaultship_zipcode,
                'ship_phone_number': profile.defaultship_phone_number,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()
        marketing_value = "false"
        full_name = ""

    ship_state = USStateSelect()
    bill_state = USStateSelect()
    ship_zipcode = USZipCodeField()
    bill_zipcode = USZipCodeField()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'ship_state': ship_state,
        'bill_state': bill_state,
        'ship_zipcode': ship_zipcode,
        'bill_zipcode': bill_zipcode,
        'marketing': marketing_value,
        'full_name': full_name,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    marketing_string = request.session.get('marketing')
    marketing = bool(marketing_string)

    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save marketing value if True
        if marketing:
            profile.marketing = marketing
            profile.save()

        # Save the user's info
        if save_info:
            profile.defaultship_full_name = order.ship_full_name
            profile.defaultship_comp_name = order.ship_comp_name
            profile.defaultship_street_address1 = order.ship_street_address1
            profile.defaultship_street_address2 = order.ship_street_address2
            profile.defaultship_city = order.ship_city
            profile.defaultship_state = order.ship_state
            profile.defaultship_zipcode = order.ship_zipcode
            profile.defaultship_phone_number = order.ship_phone_number
            profile.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
