# Generated by Django 3.2.7 on 2021-10-12 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_collection'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='MainImage',
        ),
        migrations.AlterField(
            model_name='product',
            name='fit',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='length',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterModelTable(
            name='mainimage',
            table='main_images',
        ),
        migrations.CreateModel(
            name='SubImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'sub_images',
            },
        ),
    ]
