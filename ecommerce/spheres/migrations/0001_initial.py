# Generated by Django 5.1.4 on 2024-12-07 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FName', models.CharField(max_length=50)),
                ('SName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order_Date', models.DateTimeField(auto_now_add=True)),
                ('Total_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Description', models.TextField()),
                ('Stock_Quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apiToken', models.CharField(max_length=255)),
                ('User_First_Name', models.CharField(max_length=50)),
                ('User_Last_Name', models.CharField(max_length=50)),
                ('User_Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Date_Joined', models.DateTimeField(auto_now_add=True)),
                ('Last_Modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Quantity', models.IntegerField()),
                ('Administrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spheres.administrator')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spheres.order')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spheres.product')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Payment_Date', models.DateTimeField(auto_now_add=True)),
                ('Status', models.CharField(max_length=50)),
                ('Subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spheres.subscriber')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spheres.subscriber'),
        ),
    ]
