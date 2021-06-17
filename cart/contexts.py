from decimal import Decimal
from django.conf import settings
from django .shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total += round(quantity * product.price, 2)
        product_count += quantity
        cart_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })

    shipping = round(
        total * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE/100), 2)

    ca_tax = round(total * Decimal(settings.CA_SALES_TAX/100), 2)

    grand_total = round(shipping + total, 2)
    grand_total_ca = round(shipping + ca_tax + total, 2)

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'shipping': shipping,
        'ca_tax': ca_tax,
        'grand_total': grand_total,
        'grand_total_ca': grand_total_ca,
    }

    return context
