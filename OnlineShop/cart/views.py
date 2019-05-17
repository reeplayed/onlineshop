from django.shortcuts import render
from .models import Cart
from shop.models import Product


def cart(request):
    e = 34
    cart = Cart.objects.get_cart(request)
    products = cart.product.all()

    if request.method == 'POST':
        if 'foo' in request.POST:
            prod_id = request.POST.get('foo')
            prod = Product.objects.get(id=prod_id)
            cart.product.remove(prod)

    context = {
        'products': products,
        'cart': cart

    }

    return render(request, 'cart/cart.html', context)
