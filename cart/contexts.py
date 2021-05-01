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
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })

    shipping = total * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE/100)

    ca_tax = total * Decimal(settings.CA_SALES_TAX/100)

    grand_total = shipping + total
    grand_total_ca = shipping + ca_tax + total

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
