# Generated by Django 4.2.2 on 2023-06-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='recently_viewed_products',
            field=models.ManyToManyField(blank=True, related_name='viewed_users', to='product.product'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_liked_products',
            field=models.ManyToManyField(blank=True, related_name='liked_users', to='product.product'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
