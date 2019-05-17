from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .utils import upload_image_path
from django.db.models.signals import pre_save, post_save
from shop.models import Product


class Profil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=upload_image_path)
    bought_products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profil, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profil.objects.create(user=instance)


post_save.connect(create_profile, sender=User)


def save_profile(sender, instance, **kwargs):
    instance.profil.save()


post_save.connect(save_profile, sender=User)