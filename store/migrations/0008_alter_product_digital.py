# Generated by Django 4.0.5 on 2022-06-20 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=True, null=True),
        ),
    ]