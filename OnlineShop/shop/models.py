from .utils import unique_slug_generator, upload_image_path
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from comments.models import Comment



BRAND = (
    ('Tommy Hilfiger', 'Tommy Hilfiger'),
    ("Levi's", 'Levis'),
    ("Calvin Klein", 'Calvin Klein'),
    ("Ralph Lauren", 'Ralph Lauren'),
)
CATEGORY =(
    ('Tshirt', 'Tshirt'),
    ('Shoes', 'Shoes'),
    ('Trousers', 'Trousers'),
    ('Jackets', 'Jackets'),
    ('Shirts', 'Shirts'),
)


class ProductQuerySet(models.query.QuerySet):
    pass


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def brand_filter(self, request):
        brand_query = Product.objects.none()
        if 'Calvin Klein' in request.GET:
            qs = Product.objects.filter(brand='Calvin Klein')
            brand_query |= qs
        if 'Tommy Hilfiger' in request.GET:
            qs = Product.objects.filter(brand='Tommy Hilfiger')
            brand_query |= qs
        if "Levi's" in request.GET:
            qs = Product.objects.filter(brand="Levi's")
            brand_query |= qs
        if 'Ralph Lauren' in request.GET:
            qs = Product.objects.filter(brand='Ralph Lauren')
            brand_query |= qs
        if brand_query.count() == 0:
            return Product.objects.all()
        else:
            return brand_query

    def sorting(self, request, query):
        checked = []
        if 'option' in request.GET:
            if request.GET.get('option') == '1':
                checked.append('1')
                return query.order_by('date_add'), checked
            elif request.GET.get('option') == '2':
                checked.append('2')
                return query.order_by('price'), checked
            elif request.GET['option'] == '3':
                checked.append('3')
                return query.order_by('-price'), checked
            elif request.GET['option'] == '4':
                checked.append('4')
                return query.order_by('-average_rating'), checked
        else:
            return query, checked


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True, unique=True)
    content = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=50, null=True, blank=True, choices=BRAND)
    image = models.ImageField(default='default.jpg', upload_to=upload_image_path)
    image_2 = models.ImageField(default='default.jpg', upload_to=upload_image_path)
    image_3 = models.ImageField(default='default.jpg', upload_to=upload_image_path)
    price = models.DecimalField(default=11.00, max_digits=9, decimal_places=2)
    category = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY)
    comments = models.ManyToManyField(Comment, blank=True)
    average_rating = models.DecimalField(default=0.00, max_digits=9, decimal_places=1)
    objects = ProductManager()

    def get_absolute_url(self):
        return f'product/{self.slug}'

    def __str__(self):
        return self.name


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.slug == None:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def average_rating_func(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        all_comments = instance.comments.all()
        total = 0
        for i in all_comments:
            total += i.rating
        instance.average_rating = total/all_comments.count()
        instance.save()


m2m_changed.connect(average_rating_func, sender=Product.comments.through)
