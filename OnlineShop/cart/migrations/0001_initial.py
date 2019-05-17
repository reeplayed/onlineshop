# Generated by Django 2.2.1 on 2019-05-15 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ManyToManyField(blank=True, to='shop.Product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
