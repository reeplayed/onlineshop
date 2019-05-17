from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed


class CartManager(models.Manager):

    def get_cart(self, request):

        cart_id = request.session.get('cart_id', None)

        if cart_id is None:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
                return cart
            else:
                cart = Cart.objects.create(user=None)
                request.session['cart_id'] = cart.id
                return cart
        if cart_id is not None:
            if request.user.is_authenticated:
                old_cart = Cart.objects.filter(id=cart_id)
                if old_cart.count() == 1:
                    new_cart = Cart.objects.get(user=request.user)
                    for product in old_cart.first().product.all():
                        new_cart.product.add(product)
                    cart = new_cart
                    old_cart.delete()
                    return cart
                else:
                    cart = Cart.objects.get(user=request.user)
                    return cart
            else:
                cart = Cart.objects.get(id=cart_id)
                return cart


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, blank=True)
    updatetime = models.DateTimeField(auto_now=True)
    addtime = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    objects = CartManager()

    def __str__(self):
        return f'Card nr {self.id}'

    @property
    def count(self):
        return self.product.all().count()


def total_changed(sender, instance, action, *args, **kwargs):
    all_products = instance.product.all()
    total = 0
    for i in all_products:
        total += i.price
    instance.total = total
    instance.save()


m2m_changed.connect(total_changed, sender=Cart.product.through)


def cart_create(sender, instance, created, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)


post_save.connect(cart_create, sender=User)