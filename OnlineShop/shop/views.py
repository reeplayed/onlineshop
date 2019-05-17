from django.shortcuts import render, get_object_or_404
from cart.models import Cart
from comments.models import Comment
from django.core.paginator import Paginator
from .utils import request_get_param, comment_is_access
from .models import Product


def shop(request):

    cart = Cart.objects.get_cart(request)
    qss = Product.objects.brand_filter(request)
    qss, checked = Product.objects.sorting(request, qss)

    paginator = Paginator(qss, 9)
    ret = request.GET.get('page')
    qs = paginator.get_page(ret)

    context = {
        'qs': qs,
        'cart': cart,
        'check': checked,
        'get_params': request_get_param(request)
    }

    return render(request, 'shop/shop.html',  context)


def detail_view(request, slug):
    cart = Cart.objects.get_cart(request)
    qery = get_object_or_404(Product, slug=slug)
    print(qery)
    com = qery.comments.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = request.POST.get('comment', None)
            rating = request.POST.get('option', None)
            if comment is not None and rating is not None:
                new_comment = Comment(content=comment, author=request.user, rating=rating)
                new_comment.save()
                qery.comments.add(new_comment)

        var = request.POST.get('foo')
        if var == 'remove':
            cart.product.remove(qery)
        if var == 'add':
            cart.product.add(qery)
    if qery in cart.product.all():
        change = 1
    else:
        change = 2

    print(request.POST)
    context = {
        'qs': qery,
        'com': com,
        'cart': cart,
        'change': change,
        'comm_access': comment_is_access(request, qery)


    }
    return render(request, 'shop/detail_view.html', context)
