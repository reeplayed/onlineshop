from django.shortcuts import render, redirect
from .forms import AddressForm
from cart.models import Cart
from billing.models import Billing
from profil.models import Profil
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def checkout(request):

    cart = Cart.objects.get_cart(request)
    if cart.product.all().count() == 0:
        return redirect('cart')

    form = AddressForm()
    profil = Profil.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            Billing.objects.create(user=request.user, address=form.instance, cart=cart)
            messages.success(request, f'Your order is realize')
            for prod in cart.product.all():
                profil.bought_products.add(prod)
            cart.product.clear()
            return redirect('shop')

    context = {
        'form': form,
        'cart': cart,
        'profil': profil
    }
    return render(request, 'billing/checkout_view.html', context)
